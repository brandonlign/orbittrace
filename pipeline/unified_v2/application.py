"""Run the v2 detector on a multi-year GMN month without target access."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from pipeline.pr57_novel import run_novel_search as base

from .config import V2Config
from .features import periodic_physical6_from_raw
from .full_pipeline import (
    apply_orbit_gate,
    build_full_catalogue,
    compact_expanded_candidate,
    seed_score,
)
from .partitioned_hierarchy import fit_partitioned_recurrent_hierarchy
from .recurrent_tree import fit_recurrent_hierarchy


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return [_jsonable(item) for item in value.tolist()]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    return value


def _timestamp_key(value: Any) -> str:
    digits = "".join(character for character in str(value) if character.isdigit())
    return digits[:14]


def _target_keys(target: Path, years: tuple[int, ...]) -> set[str]:
    frame = pd.read_csv(target)
    timestamps = pd.to_datetime(frame["Tobs"], format="%Y-%m-%d-%H:%M:%S", errors="coerce")
    return {
        value.strftime("%Y%m%d%H%M%S")
        for value in timestamps.dropna()
        if int(value.year) in years
    }


def _target_reveal(
    candidates: list[dict[str, Any]],
    target: Path,
    years: tuple[int, ...],
) -> dict[str, Any]:
    target_keys = _target_keys(target, years)
    matches: list[dict[str, Any]] = []
    for candidate in candidates:
        reported_ids = candidate.get(
            "final_event_ids",
            candidate.get("expanded_event_ids", candidate.get("event_ids", [])),
        )
        member_keys = {_timestamp_key(value) for value in reported_ids}
        overlap = len(member_keys & target_keys)
        if not overlap:
            continue
        precision = overlap / max(1, len(member_keys))
        recall = overlap / max(1, len(target_keys))
        f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
        matches.append(
            {
                "rank": int(candidate.get("global_rank", candidate.get("rank", 0))),
                "family_id": candidate["family_id"],
                "hierarchy_method": candidate.get("hierarchy_method", "inherited_leaf_seed"),
                "core_member_count": int(candidate["member_count"]),
                "expanded_member_count": int(len(member_keys)),
                "target_overlap": int(overlap),
                "target_count": int(len(target_keys)),
                "precision": float(precision),
                "recall": float(recall),
                "f1": float(f1),
                "members_by_year": candidate.get("members_by_year", {}),
                "expanded_members_by_year": {
                    str(year): int(
                        sum(_timestamp_key(value).startswith(str(year)) for value in member_keys)
                    )
                    for year in years
                },
            }
        )
    matches.sort(key=lambda item: (-item["f1"], -item["target_overlap"], item["rank"]))
    return {
        "target_count": int(len(target_keys)),
        "years": list(years),
        "best": matches[0] if matches else None,
        "matches": matches,
    }


def _feature_panel(data: pd.DataFrame, config: V2Config) -> np.ndarray:
    solar = data["sol_lon_deg"].to_numpy(float)
    raw = np.column_stack(
        (
            base.circ_diff(data["lamgeo_deg"].to_numpy(float), solar),
            data["betgeo_deg"].to_numpy(float),
            data["vgeo_km_s"].to_numpy(float),
            base.circ_diff(solar, base.circ_center(solar)),
        )
    )
    return periodic_physical6_from_raw(raw, config.feature_scales)


def _seed_score(candidate: dict[str, Any], quantile: float) -> float:
    return seed_score(candidate, quantile)


def _prepare(frame: pd.DataFrame, year: int, month: int) -> dict[str, Any]:
    """Prepare the v1 quality/sporadic panel without pandas-2-only APIs."""

    missing = [column for column in base.BASE_COLUMNS if column not in frame.columns]
    if missing:
        raise RuntimeError(f"Missing GMN columns: {missing}")
    data = frame[base.BASE_COLUMNS].copy()
    data["label"] = data["iau_code"].map(base.shower_label)
    numeric_cols = [
        "sol_lon_deg",
        "lamgeo_deg",
        "betgeo_deg",
        "vgeo_km_s",
        *base.ORBIT_COLUMNS,
        *base.SIGMA_COLUMNS,
        "medianfiterr_arcsec",
        "num_stat",
    ]
    for column in numeric_cols:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    valid = np.isfinite(data[["sol_lon_deg", "lamgeo_deg", "betgeo_deg", "vgeo_km_s"]]).all(axis=1)
    valid &= data["sol_lon_deg"].between(0, 360) & data["lamgeo_deg"].between(0, 360)
    valid &= data["betgeo_deg"].between(-90, 90) & data["vgeo_km_s"].between(5, 75)
    valid &= data["num_stat"].fillna(0) >= 2
    valid &= data["medianfiterr_arcsec"].fillna(9999) <= 180
    data = data.loc[valid & (data["label"] == "SPORADIC")].reset_index(drop=True)
    quality_rows = len(data)
    if len(data) > base.MAX_MONTH_ROWS:
        data = data.sample(
            base.MAX_MONTH_ROWS,
            random_state=base.SEED + int(year) * 100 + int(month),
        ).sort_index().reset_index(drop=True)
    solar = data["sol_lon_deg"].to_numpy(float)
    center = base.circ_center(solar)
    raw = np.column_stack(
        (
            base.circ_diff(data["lamgeo_deg"].to_numpy(float), solar),
            data["betgeo_deg"].to_numpy(float),
            data["vgeo_km_s"].to_numpy(float),
            base.circ_diff(solar, center),
        )
    )
    return {
        "data": data,
        "raw": raw,
        "center_sol": center,
        "quality_rows": int(quality_rows),
    }


def _apply_orbit_gate(
    candidate: dict[str, Any],
    orbit_matrix: np.ndarray,
    event_ids: np.ndarray,
    config: V2Config,
) -> dict[str, Any]:
    """Compatibility wrapper for the shared full-catalogue implementation."""

    return apply_orbit_gate(candidate, orbit_matrix, event_ids, config)


def _compact_expanded_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    """Compatibility wrapper for the shared full-catalogue implementation."""

    return compact_expanded_candidate(candidate)


def run(
    years: tuple[int, ...] = (2022, 2023, 2024, 2025, 2026),
    month: int = 4,
    config: V2Config | None = None,
    target: Path | None = None,
    seed_years: tuple[int, ...] | None = None,
    seed_candidates_path: Path | None = None,
    hierarchy_mode: str = "partitioned",
    seed_only: bool = False,
) -> dict[str, Any]:
    """Generate and cross-fit candidates; reveal target only after ranking."""

    config = config or V2Config()
    if len(years) < 2 or len(set(years)) != len(years):
        raise ValueError("at least two distinct years are required")
    seed_years = tuple(seed_years or years[-2:])
    if len(seed_years) < 2 or any(year not in years for year in seed_years):
        raise ValueError("seed_years must contain at least two years from years")
    if hierarchy_mode not in {"partitioned", "global"}:
        raise ValueError("hierarchy_mode must be 'partitioned' or 'global'")
    if seed_only and target is not None:
        raise ValueError("seed-only generation cannot receive a target path")
    frames: list[pd.DataFrame] = []
    matrices: list[np.ndarray] = []
    orbit_panels: list[np.ndarray] = []
    solar_panels: list[np.ndarray] = []
    year_vectors: list[np.ndarray] = []
    ids: list[str] = []
    metadata: dict[str, Any] = {}
    for year in years:
        prepared = _prepare(base.load_month(int(year), int(month)), int(year), int(month))
        data = prepared["data"]
        matrix = _feature_panel(data, config)
        event_ids = data["unique_trajectory_identifier"].astype(str).to_numpy()
        if len(set(event_ids.tolist())) != len(event_ids):
            raise RuntimeError(f"duplicate trajectory identifiers in {year}-{month:02d}")
        frames.append(data)
        matrices.append(matrix)
        orbit_panels.append(data[base.ORBIT_COLUMNS].to_numpy(float))
        solar_panels.append(data["sol_lon_deg"].to_numpy(float))
        year_vectors.append(np.full(len(data), int(year), dtype=np.int64))
        ids.extend(event_ids.tolist())
        metadata[str(year)] = {
            "rows": int(len(data)),
            "quality_rows_before_sampling": int(prepared["quality_rows"]),
            "solar_center": float(prepared["center_sol"]),
            "catalog_labels_used_for_known_shower_exclusion": True,
            "orbittrace_target_membership_accessed": False,
        }
        print(f"{year}-{month:02d}: prepared {len(data):,} sporadic rows", flush=True)

    matrix = np.vstack(matrices)
    orbit_matrix = np.vstack(orbit_panels)
    solar_longitude = np.concatenate(solar_panels)
    year_array = np.concatenate(year_vectors)
    event_ids = np.asarray(ids, dtype=str)
    seed_indices_parts: list[np.ndarray] = []
    sample_rng = np.random.default_rng(int(config.hierarchy_sample_seed))
    for year in seed_years:
        year_indices = np.flatnonzero(year_array == int(year))
        if hierarchy_mode == "global":
            limit = int(config.hierarchy_max_rows_per_year)
            if len(year_indices) > limit:
                year_indices = np.sort(sample_rng.choice(year_indices, size=limit, replace=False))
        seed_indices_parts.append(year_indices)
    seed_indices = np.concatenate(seed_indices_parts) if seed_indices_parts else np.asarray([], dtype=int)
    if seed_candidates_path is None:
        if hierarchy_mode == "partitioned":
            parents, leaves, diagnostics = fit_partitioned_recurrent_hierarchy(
                matrix[seed_indices],
                year_array[seed_indices],
                event_ids[seed_indices],
                solar_longitude[seed_indices],
                config,
                include_leaves=True,
            )
        else:
            parents, leaves, diagnostics = fit_recurrent_hierarchy(
                matrix[seed_indices],
                year_array[seed_indices],
                event_ids[seed_indices],
                config,
                include_leaves=True,
            )
        seed_source = {
            "mode": f"fresh_v2_{hierarchy_mode}_hierarchy",
            "path": None,
            "sha256": None,
        }
    else:
        seed_source_bytes = seed_candidates_path.read_bytes()
        seed_payload = json.loads(seed_source_bytes.decode("utf-8"))
        # A frozen v2 seed catalogue is replayed exactly; legacy v1 artifacts
        # expose their target-free candidates under ``leaf_candidates``.
        parents = []
        leaves = list(
            seed_payload.get("candidates", seed_payload.get("leaf_candidates", []))
        )
        diagnostics = {
            "mode": "replayed_seed_artifact",
            "source_stage": seed_payload.get("stage"),
            "source_target_accessed_during_clustering": seed_payload.get(
                "target_accessed_during_clustering",
                seed_payload.get("target_accessed_during_generation"),
            ),
            "seed_candidates": int(len(parents) + len(leaves)),
        }
        seed_source = {
            "mode": "replayed_target_free_seed_artifact",
            "path": str(seed_candidates_path),
            "sha256": hashlib.sha256(seed_source_bytes).hexdigest(),
        }
    raw_candidates = [dict(candidate) for branch in (parents, leaves) for candidate in branch]
    full_index_by_id = {event_id: index for index, event_id in enumerate(event_ids.tolist())}
    if seed_only:
        for candidate in raw_candidates:
            candidate["seed_score"] = _seed_score(candidate, config.recurrence_quantile)
        eligible_candidates = [
            candidate
            for candidate in raw_candidates
            if float(candidate["seed_score"]) > 0.0
            and int(candidate["member_count"]) <= int(config.hierarchy_max_candidate_members)
        ]
        eligible_candidates.sort(
            key=lambda item: (
                -float(item["seed_score"]),
                -int(item["member_count"]),
                item["family_id"],
            )
        )
        for rank, candidate in enumerate(eligible_candidates, start=1):
            candidate["seed_rank"] = rank
        selection_diagnostics = {
            "raw_candidates": int(len(raw_candidates)),
            "eligible_candidates": int(len(eligible_candidates)),
            "excluded_nonrecurrent": int(
                sum(float(item["seed_score"]) <= 0.0 for item in raw_candidates)
            ),
            "excluded_too_large": int(
                sum(
                    int(item["member_count"]) > config.hierarchy_max_candidate_members
                    for item in raw_candidates
                )
            ),
            "maximum_seed_members": int(config.hierarchy_max_candidate_members),
            "eligibility_rule": "positive lower-tail annual support and seed members <= fixed maximum",
        }
        candidates = []
        for candidate in eligible_candidates:
            compact = dict(candidate)
            compact.pop("members", None)
            compact["global_rank"] = int(candidate["seed_rank"])
            candidates.append(compact)
    else:
        for candidate in raw_candidates:
            candidate["members"] = [
                full_index_by_id[event_id] for event_id in candidate["event_ids"]
            ]
        candidates, selection_diagnostics = build_full_catalogue(
            raw_candidates,
            matrix,
            year_array,
            event_ids,
            orbit_matrix,
            config,
        )
    candidates.sort(
        key=lambda item: (
            -_seed_score(item, config.recurrence_quantile),
            int(item.get("seed_rank", 0)),
            -int(item.get("final_member_count", item.get("expanded_member_count", 0))),
            item["family_id"],
        )
    )
    for rank, candidate in enumerate(candidates, start=1):
        candidate["global_rank"] = rank
    result: dict[str, Any] = {
        "stage": "unified_v2_target_free_seed_catalogue"
        if seed_only
        else "unified_v2_target_free_application",
        "method": (
            "partitioned exposure-normalized recurrent HDBSCAN seed catalogue"
            if seed_only and hierarchy_mode == "partitioned"
            else "exposure-normalized recurrent HDBSCAN seed catalogue"
            if seed_only
            else "partitioned exposure-normalized recurrent HDBSCAN tree plus cross-fitted robust conformal halo"
            if hierarchy_mode == "partitioned"
            else "exposure-normalized recurrent HDBSCAN tree plus cross-fitted robust conformal halo"
        ),
        "representation": "periodic_physical6",
        "years": list(years),
        "seed_years": list(seed_years),
        "month": int(month),
        "config": _jsonable(config.__dict__),
        "input": metadata,
        "diagnostics": diagnostics,
        "candidate_selection": selection_diagnostics,
        "diagnostics_application": {
            "full_events": int(len(matrix)),
            "seed_events": int(len(seed_indices)),
            "seed_years": list(seed_years),
            "hierarchy_mode": hierarchy_mode,
            "hierarchy_max_rows_per_year": int(config.hierarchy_max_rows_per_year),
            "hierarchy_sample_seed": int(config.hierarchy_sample_seed),
            "seed_source": seed_source,
            "orbit_gate_applied_after_halo": not seed_only,
            "seed_only": bool(seed_only),
        },
        "target_accessed_during_generation": False,
        "candidate_count": int(len(candidates)),
        "candidates": candidates,
    }
    if target is not None:
        result["posthoc_target_reveal"] = _target_reveal(candidates, target, years)
        result["target_accessed_during_generation"] = False
    return _jsonable(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--years", default="2022,2023,2024,2025,2026")
    parser.add_argument("--month", type=int, default=4)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--min-cluster-size", type=int, default=8)
    parser.add_argument("--min-samples", type=int, default=4)
    parser.add_argument("--halo-tail-alpha", type=float, default=0.01)
    parser.add_argument("--halo-iterations", type=int, default=2)
    parser.add_argument("--halo-orbit-distance-max", type=float, default=0.15)
    parser.add_argument("--seed-years")
    parser.add_argument("--seed-candidates", type=Path)
    parser.add_argument("--hierarchy-mode", choices=("partitioned", "global"), default="partitioned")
    parser.add_argument("--hierarchy-window-width-deg", type=float, default=10.0)
    parser.add_argument("--hierarchy-window-stride-deg", type=float, default=5.0)
    parser.add_argument("--hierarchy-max-rows-per-year", type=int, default=30000)
    parser.add_argument("--hierarchy-max-candidate-members", type=int, default=300)
    parser.add_argument("--seed-only", action="store_true")
    args = parser.parse_args()
    years = tuple(int(value) for value in args.years.split(",") if value)
    config = V2Config(
        min_cluster_size=args.min_cluster_size,
        min_samples=args.min_samples,
        halo_core_tail_alpha=args.halo_tail_alpha,
        halo_iterations=args.halo_iterations,
        halo_orbit_distance_max=args.halo_orbit_distance_max,
        hierarchy_window_width_deg=args.hierarchy_window_width_deg,
        hierarchy_window_stride_deg=args.hierarchy_window_stride_deg,
        hierarchy_max_rows_per_year=args.hierarchy_max_rows_per_year,
        hierarchy_max_candidate_members=args.hierarchy_max_candidate_members,
    )
    seed_years = None if args.seed_years is None else tuple(int(value) for value in args.seed_years.split(",") if value)
    result = run(
        years,
        args.month,
        config,
        args.target,
        seed_years,
        args.seed_candidates,
        args.hierarchy_mode,
        args.seed_only,
    )
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "v2_application.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "out": str(path),
                "candidates": result["candidate_count"],
                "best_target": result.get("posthoc_target_reveal", {}).get("best"),
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
