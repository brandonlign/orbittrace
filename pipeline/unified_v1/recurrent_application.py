"""Apply the frozen recurrent-EOM paper method to target-containing GMN data."""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import hdbscan
import hdbscan.hdbscan_ as hdbscan_internal
from hdbscan._hdbscan_tree import compute_stability
from sklearn.utils import check_array as sklearn_check_array

from pipeline.pr57_novel import run_novel_search as base

from .method import UnifiedConfig, jsonable, strict_iau_match
from .recurrent_eom import eom_labels, leaf_labels, recurrent_stability, selected_eom_nodes

MIN_CLUSTER_SIZE = 10
MIN_SAMPLES = 10


def install_hdbscan_compatibility() -> None:
    """Bridge HDBSCAN and scikit-learn check-array keyword renames."""

    accepted = set(inspect.signature(sklearn_check_array).parameters)

    def compatible_check_array(*args: Any, **kwargs: Any) -> np.ndarray:
        if "ensure_all_finite" in kwargs and "ensure_all_finite" not in accepted:
            kwargs["force_all_finite"] = kwargs.pop("ensure_all_finite")
        if "force_all_finite" in kwargs and "force_all_finite" not in accepted:
            kwargs["ensure_all_finite"] = kwargs.pop("force_all_finite")
        return sklearn_check_array(*args, **kwargs)

    hdbscan_internal.check_array = compatible_check_array


def geo6(data: pd.DataFrame) -> np.ndarray:
    """Return the exact six-component geocentric representation."""

    solar = np.radians(data["sol_lon_deg"].to_numpy(float))
    longitude = np.radians(
        base.circ_diff(
            data["lamgeo_deg"].to_numpy(float),
            data["sol_lon_deg"].to_numpy(float),
        )
    )
    latitude = np.radians(data["betgeo_deg"].to_numpy(float))
    speed = data["vgeo_km_s"].to_numpy(float)
    return np.column_stack(
        (
            np.cos(solar),
            np.sin(solar),
            np.sin(longitude) * np.cos(latitude),
            np.cos(longitude) * np.cos(latitude),
            np.sin(latitude),
            speed / 72.0,
        )
    )


def periodic_physical6(data: pd.DataFrame, config: UnifiedConfig | None = None) -> np.ndarray:
    """Periodic full-year form of the successful local physical4 geometry."""

    config = config or UnifiedConfig()
    solar = np.radians(data["sol_lon_deg"].to_numpy(float))
    longitude = np.radians(
        base.circ_diff(
            data["lamgeo_deg"].to_numpy(float),
            data["sol_lon_deg"].to_numpy(float),
        )
    )
    latitude = data["betgeo_deg"].to_numpy(float)
    speed = data["vgeo_km_s"].to_numpy(float)
    solar_scale = 180.0 / (np.pi * config.feature_scales[3])
    longitude_scale = 180.0 / (np.pi * config.feature_scales[0])
    return np.column_stack(
        (
            np.cos(solar) * solar_scale,
            np.sin(solar) * solar_scale,
            np.cos(longitude) * longitude_scale,
            np.sin(longitude) * longitude_scale,
            latitude / config.feature_scales[1],
            speed / config.feature_scales[2],
        )
    )


def periodic_physical6_from_raw(
    raw: np.ndarray,
    config: UnifiedConfig | None = None,
) -> np.ndarray:
    """Transform local ``(sun_lon, latitude, speed, solar_offset)`` rows."""

    config = config or UnifiedConfig()
    values = np.asarray(raw, dtype=float)
    if values.ndim != 2 or values.shape[1] != 4:
        raise ValueError("physical4 input must have shape (n, 4)")
    longitude = np.radians(values[:, 0])
    solar = np.radians(values[:, 3])
    longitude_scale = 180.0 / (np.pi * config.feature_scales[0])
    solar_scale = 180.0 / (np.pi * config.feature_scales[3])
    return np.column_stack(
        (
            np.cos(solar) * solar_scale,
            np.sin(solar) * solar_scale,
            np.cos(longitude) * longitude_scale,
            np.sin(longitude) * longitude_scale,
            values[:, 1] / config.feature_scales[1],
            values[:, 2] / config.feature_scales[2],
        )
    )


def canonical_partition(labels: np.ndarray) -> tuple[tuple[int, ...], ...]:
    groups = []
    for label in sorted(int(value) for value in np.unique(labels) if int(value) >= 0):
        groups.append(tuple(np.flatnonzero(labels == label).tolist()))
    return tuple(sorted(groups))


def recurrent_candidates(
    matrix: np.ndarray,
    years: np.ndarray,
    event_ids: np.ndarray,
    include_leaf: bool = False,
    min_cluster_size: int = MIN_CLUSTER_SIZE,
    min_samples: int = MIN_SAMPLES,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Fit one hierarchy and emit the frozen recurrent-EOM ranking."""

    install_hdbscan_compatibility()
    model = hdbscan.HDBSCAN(
        min_cluster_size=int(min_cluster_size),
        min_samples=int(min_samples),
        metric="euclidean",
        cluster_selection_method="eom",
        cluster_selection_epsilon=0.0,
        allow_single_cluster=False,
        prediction_data=False,
    ).fit(np.asarray(matrix, dtype=float))
    tree = model.condensed_tree_._raw_tree
    ordinary = compute_stability(tree)
    ordinary_labels = eom_labels(tree, ordinary)
    if canonical_partition(model.labels_) != canonical_partition(ordinary_labels):
        raise RuntimeError("custom ordinary-EOM path diverged from HDBSCAN")

    recurrent, annual = recurrent_stability(tree, years)
    labels = eom_labels(tree, recurrent)
    nodes = selected_eom_nodes(tree, recurrent)
    positive = sorted(int(value) for value in np.unique(labels) if int(value) >= 0)
    if positive != list(range(len(nodes))):
        raise RuntimeError("compact labels no longer align with selected EOM nodes")

    candidates = []
    for label, node in enumerate(nodes):
        members = np.flatnonzero(labels == label)
        ids = tuple(sorted(str(event_ids[index]) for index in members))
        family_id = "REOM1" + hashlib.sha256(("|".join(ids)).encode()).hexdigest()[:20]
        annual_counts = {
            str(year): int(np.sum(years[members] == year))
            for year in sorted(int(value) for value in np.unique(years))
        }
        candidates.append(
            {
                "family_id": family_id,
                "node_id": int(node),
                "event_ids": list(ids),
                "member_count": int(len(ids)),
                "members_by_year": annual_counts,
                "recurrent_stability": float(recurrent[float(node)]),
                "ordinary_stability": float(ordinary[float(node)]),
                "annual_normalized_stability": list(annual[int(node)]),
            }
        )
    candidates.sort(
        key=lambda item: (
            -item["recurrent_stability"],
            -item["ordinary_stability"],
            -item["member_count"],
            item["family_id"],
        )
    )
    for rank, candidate in enumerate(candidates, start=1):
        candidate["rank"] = rank
    diagnostics: dict[str, Any] = {
        "events": int(len(matrix)),
        "min_cluster_size": int(min_cluster_size),
        "min_samples": int(min_samples),
        "ordinary_candidates": int(len(set(int(value) for value in ordinary_labels if int(value) >= 0))),
        "recurrent_candidates": int(len(candidates)),
        "mechanism_active": canonical_partition(ordinary_labels) != canonical_partition(labels),
    }
    if include_leaf:
        labels_leaf, probabilities = leaf_labels(tree, ordinary)
        leaves = []
        year_values = sorted(int(value) for value in np.unique(years))
        year_totals = {year: int(np.sum(years == year)) for year in year_values}
        for label in sorted(int(value) for value in np.unique(labels_leaf) if int(value) >= 0):
            members = np.flatnonzero(labels_leaf == label)
            ids = tuple(sorted(str(event_ids[index]) for index in members))
            family_id = "LEAF1" + hashlib.sha256(("|".join(ids)).encode()).hexdigest()[:20]
            counts = {str(year): int(np.sum(years[members] == year)) for year in year_values}
            normalized = [counts[str(year)] / year_totals[year] for year in year_values]
            leaves.append(
                {
                    "family_id": family_id,
                    "event_ids": list(ids),
                    "member_count": int(len(ids)),
                    "members_by_year": counts,
                    "minimum_annual_support": int(min(counts.values())),
                    "minimum_normalized_annual_support": float(min(normalized)),
                    "mean_membership_probability": float(np.mean(probabilities[members])),
                }
            )
        leaves.sort(
            key=lambda item: (
                -item["minimum_normalized_annual_support"],
                -item["mean_membership_probability"],
                -item["member_count"],
                item["family_id"],
            )
        )
        for rank, candidate in enumerate(leaves, start=1):
            candidate["rank"] = rank
        diagnostics["leaf_candidates"] = leaves
        diagnostics["leaf_candidate_count"] = len(leaves)
    return candidates, diagnostics


def _timestamp_key(value: str) -> str:
    digits = "".join(character for character in str(value) if character.isdigit())
    return digits[:14]


def reveal_target(candidates: list[dict[str, Any]], target_path: Path, years: tuple[int, int]) -> dict[str, Any]:
    target = pd.read_csv(target_path)
    timestamps = pd.to_datetime(target["Tobs"], utc=True, errors="coerce")
    target_keys = {
        value.strftime("%Y%m%d%H%M%S")
        for value in timestamps.dropna()
        if int(value.year) in years
    }
    rows = []
    for candidate in candidates:
        candidate_keys = {_timestamp_key(value) for value in candidate["event_ids"]}
        overlap = len(candidate_keys & target_keys)
        if not overlap:
            continue
        unique_time_precision = overlap / max(1, len(candidate_keys))
        precision = overlap / max(1, int(candidate["member_count"]))
        recall = overlap / max(1, len(target_keys))
        f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
        rows.append(
            {
                "rank": int(candidate["rank"]),
                "family_id": candidate["family_id"],
                "member_count": candidate["member_count"],
                "unique_member_times": int(len(candidate_keys)),
                "members_by_year": candidate["members_by_year"],
                "target_overlap": int(overlap),
                "target_count": int(len(target_keys)),
                "precision": float(precision),
                "unique_time_precision": float(unique_time_precision),
                "recall": float(recall),
                "f1": float(f1),
            }
        )
    rows.sort(key=lambda item: (-item["f1"], item["rank"]))
    return {"years": list(years), "target_count": len(target_keys), "best": rows[0] if rows else None, "matches": rows}


def reveal_full_history(
    candidates: list[dict[str, Any]],
    target_path: Path,
    discovery_years: tuple[int, int],
) -> list[dict[str, Any]]:
    """Reveal exact target overlap across discovery and validation years."""

    target = pd.read_csv(target_path)
    timestamps = pd.to_datetime(target["Tobs"], utc=True, errors="coerce")
    target_by_year: dict[int, set[str]] = {}
    for value in timestamps.dropna():
        target_by_year.setdefault(int(value.year), set()).add(value.strftime("%Y%m%d%H%M%S"))

    output = []
    for candidate in candidates:
        annual = {}
        total_overlap = 0
        total_target = 0
        total_unique_members = 0
        for year in sorted(target_by_year):
            if year in discovery_years:
                ids = [value for value in candidate.get("event_ids", []) if str(value).startswith(str(year))]
            else:
                ids = candidate.get("validation", {}).get(str(year), {}).get("member_ids", [])
            member_times = {_timestamp_key(value) for value in ids}
            overlap = len(member_times & target_by_year[year])
            target_count = len(target_by_year[year])
            annual[str(year)] = {
                "unique_member_times": len(member_times),
                "target_count": target_count,
                "overlap": overlap,
                "precision": float(overlap / len(member_times)) if member_times else 0.0,
                "recall": float(overlap / target_count) if target_count else 0.0,
            }
            total_overlap += overlap
            total_target += target_count
            total_unique_members += len(member_times)
        precision = total_overlap / total_unique_members if total_unique_members else 0.0
        recall = total_overlap / total_target if total_target else 0.0
        output.append(
            {
                "family_id": candidate["family_id"],
                "screened_rank": candidate.get("screened_rank"),
                "unique_member_times": total_unique_members,
                "target_count": total_target,
                "target_overlap": total_overlap,
                "precision": float(precision),
                "recall": float(recall),
                "f1": float(2 * precision * recall / (precision + recall)) if precision + recall else 0.0,
                "annual": annual,
            }
        )
    return output


def screen_leaf_candidates(
    data: pd.DataFrame,
    row_years: np.ndarray,
    leaves: list[dict[str, Any]],
    month: int,
    catalog: list[dict[str, Any]],
    config: UnifiedConfig | None = None,
) -> list[dict[str, Any]]:
    """Apply fixed label-free recurrence, orbit, source, and novelty gates."""

    config = config or UnifiedConfig()
    solar = data["sol_lon_deg"].to_numpy(float)
    center_solar = base.circ_center(solar)
    raw = np.column_stack(
        (
            base.circ_diff(data["lamgeo_deg"].to_numpy(float), solar),
            data["betgeo_deg"].to_numpy(float),
            data["vgeo_km_s"].to_numpy(float),
            base.circ_diff(solar, center_solar),
        )
    )
    scaled = raw / np.asarray(config.feature_scales, dtype=float)[None, :]
    ids = data["unique_trajectory_identifier"].astype(str).to_numpy()
    index_by_id = {event_id: index for index, event_id in enumerate(ids)}
    nights = pd.to_datetime(data["beginning_utc_time"], utc=True, errors="coerce").dt.floor("D").astype("int64").to_numpy()
    screened = []
    for leaf in leaves:
        members = np.asarray([index_by_id[event_id] for event_id in leaf["event_ids"]], dtype=int)
        if not config.min_cluster_size <= len(members) <= config.max_novel_members:
            continue
        member_years = row_years[members]
        if any(int(np.sum(member_years == year)) < 4 for year in np.unique(row_years)):
            continue
        points = scaled[members]
        center_scaled = np.median(points, axis=0)
        scaled_rms = float(np.sqrt(np.mean(np.sum((points - center_scaled[None, :]) ** 2, axis=1))))
        sigma_raw = base.robust_sigma(raw[members], np.asarray([0.3, 0.3, 0.3, 0.3]))
        solar_sigma = float(sigma_raw[3])
        if scaled_rms > config.max_scaled_rms or solar_sigma > config.max_solar_sigma_deg:
            continue
        if float(leaf["mean_membership_probability"]) < config.min_membership_probability:
            continue

        member_nights = nights[members]
        unique_nights, night_counts = np.unique(member_nights, return_counts=True)
        if len(unique_nights) < config.min_nights or night_counts.max() / len(members) > config.max_one_night_fraction:
            continue
        station_sets = data.iloc[members]["participating_stations"].fillna("").astype(str)
        stations = set().union(*(base.station_tokens(value) for value in station_sets))
        station_set_fraction = float(station_sets.value_counts(normalize=True).iloc[0])
        if len(stations) < config.min_stations or station_set_fraction > config.max_one_station_set_fraction:
            continue

        member_frame = data.iloc[members].reset_index(drop=True)
        orbit_mask = base.valid_orbits(member_frame)
        if int(orbit_mask.sum()) < config.min_cluster_size or float(orbit_mask.mean()) < config.min_orbit_fraction:
            continue
        member_orbits = member_frame.loc[orbit_mask, base.ORBIT_COLUMNS].to_numpy(float)
        orbit = base.orbit_summary(member_orbits)
        if orbit["median_d"] > config.max_orbit_median_d or orbit["q90_d"] > config.max_orbit_q90_d:
            continue

        rng = np.random.default_rng(base.SEED + month * 10000 + int(leaf["rank"]))
        annual_tests = {}
        year_values = sorted(int(value) for value in np.unique(row_years))
        for train_year, test_year in ((year_values[0], year_values[1]), (year_values[1], year_values[0])):
            train = members[member_years == train_year]
            test = np.flatnonzero(row_years == test_year)
            annual_tests[f"{train_year}_to_{test_year}"] = base.density_test(scaled[train], scaled[test], rng)
        if min(item["observed"] for item in annual_tests.values()) < config.min_split_observed:
            continue
        if max(item["p"] for item in annual_tests.values()) > config.max_split_p:
            continue

        center_raw = center_scaled * np.asarray(config.feature_scales, dtype=float)
        center = np.asarray(
            [center_raw[0], center_raw[1], center_raw[2], (center_solar + center_raw[3]) % 360.0]
        )
        if base.source_region(float(center[0]), float(center[1]), float(center[2])) is not None:
            continue
        orbit_null = base.orbit_null(data, member_orbits, float(center[3]), max(3 * solar_sigma, 1.5), rng)
        if orbit_null["p"] > config.max_orbit_null_p:
            continue
        nearest = strict_iau_match(center, orbit["medoid"], catalog, config)
        if nearest.get("matched"):
            continue

        score = (
            float(np.log1p(len(members)))
            + float(leaf["mean_membership_probability"])
            - scaled_rms
            - solar_sigma / 4.0
            - float(orbit["median_d"]) * 5.0
            - max(item["p"] for item in annual_tests.values()) * 10.0
        )
        screened.append(
            {
                **{key: value for key, value in leaf.items() if key != "event_ids"},
                "month": int(month),
                "cluster": int(leaf["rank"]),
                "hierarchy_method": "same_hierarchy_leaf",
                "member_count": int(len(members)),
                "event_ids": leaf["event_ids"],
                "members_discovery": int(len(members)),
                "center": center.tolist(),
                "sigma_raw": sigma_raw.tolist(),
                "scaled_rms": scaled_rms,
                "solar_sigma_deg": solar_sigma,
                "nights": int(len(unique_nights)),
                "stations": int(len(stations)),
                "orbit_medoid": orbit["medoid"].tolist(),
                "orbit_median_d": orbit["median_d"],
                "orbit_q90_d": orbit["q90_d"],
                "orbit_null": orbit_null,
                "annual_density_tests": annual_tests,
                "nearest_iau": nearest,
                "score": score,
                "member_rows_2025": member_frame,
            }
        )
    screened.sort(key=lambda item: (-item["score"], item["family_id"]))
    for rank, candidate in enumerate(screened, start=1):
        candidate["screened_rank"] = rank
    return screened


def run(
    years: tuple[int, int],
    month: int,
    target: Path | None = None,
    representation: str = "geo6",
    min_cluster_size: int = MIN_CLUSTER_SIZE,
    min_samples: int = MIN_SAMPLES,
) -> dict[str, Any]:
    config = UnifiedConfig(min_cluster_size=min_cluster_size, min_samples=min_samples)
    frames = []
    matrices = []
    year_vectors = []
    ids = []
    metadata = {}
    for year in years:
        prepared = base.prepare(base.load_month(year, month), year, month)
        data = prepared["data"]
        frames.append(data)
        if representation == "geo6":
            matrices.append(geo6(data))
        elif representation == "periodic_physical6":
            matrices.append(periodic_physical6(data, config))
        else:
            raise ValueError(f"unknown representation: {representation}")
        year_vectors.append(np.full(len(data), year, dtype=np.int64))
        ids.extend(data["unique_trajectory_identifier"].astype(str).tolist())
        metadata[str(year)] = {"quality_sporadics": int(len(data))}
    candidates, diagnostics = recurrent_candidates(
        np.vstack(matrices),
        np.concatenate(year_vectors),
        np.asarray(ids, dtype=str),
        include_leaf=True,
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
    )
    leaf_candidates = diagnostics.pop("leaf_candidates")
    combined_data = pd.concat(frames, ignore_index=True)
    combined_years = np.concatenate(year_vectors)
    screened_leaves = screen_leaf_candidates(
        combined_data,
        combined_years,
        leaf_candidates,
        month,
        base.parse_iau(),
        config,
    )
    validation_cache: dict[tuple[int, int], dict[str, Any]] = {}
    final_leaves = []
    for candidate in screened_leaves:
        candidate["validation"] = {
            str(year): base.validate(candidate, year, validation_cache)
            for year in (2024, 2023, 2022)
        }
        replicated = all(item["passed"] for item in candidate["validation"].values())
        candidate["clone_stability"] = base.clone_stability(candidate) if replicated else {"passed": False, "not_run": True}
        candidate["novel_discovery_gate_passed"] = bool(replicated and candidate["clone_stability"]["passed"])
        if candidate["novel_discovery_gate_passed"]:
            final_leaves.append(candidate)
    result: dict[str, Any] = {
        "stage": "frozen_recurrent_eom_target_application",
        "method": "periodic physical recurrent hierarchy" if representation == "periodic_physical6" else "recurrent-EOM HDBSCAN v1",
        "representation": representation,
        "min_cluster_size": int(min_cluster_size),
        "min_samples": int(min_samples),
        "years": list(years),
        "month": int(month),
        "input": metadata,
        "diagnostics": diagnostics,
        "target_accessed_during_clustering": False,
        "candidates": candidates,
        "leaf_candidates": leaf_candidates,
        "screened_leaf_candidates": [
            {key: value for key, value in candidate.items() if key != "member_rows_2025"}
            for candidate in screened_leaves
        ],
        "final_leaf_candidates": [
            {key: value for key, value in candidate.items() if key != "member_rows_2025"}
            for candidate in final_leaves
        ],
    }
    if target is not None:
        result["posthoc_target_reveal"] = reveal_target(candidates, target, years)
        result["posthoc_leaf_target_reveal"] = reveal_target(leaf_candidates, target, years)
        result["posthoc_screened_leaf_target_reveal"] = reveal_target(screened_leaves, target, years)
        result["posthoc_final_leaf_target_reveal"] = reveal_target(final_leaves, target, years)
        result["posthoc_full_history_reveal"] = reveal_full_history(final_leaves, target, years)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--years", default="2025,2026")
    parser.add_argument("--month", type=int, default=4)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--representation", choices=("geo6", "periodic_physical6"), default="geo6")
    parser.add_argument("--min-cluster-size", type=int, default=MIN_CLUSTER_SIZE)
    parser.add_argument("--min-samples", type=int, default=MIN_SAMPLES)
    args = parser.parse_args()
    years = tuple(int(value) for value in args.years.split(",") if value)
    if len(years) != 2:
        parser.error("--years must contain exactly two years")
    result = run(
        (years[0], years[1]),
        args.month,
        args.target,
        args.representation,
        args.min_cluster_size,
        args.min_samples,
    )
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "recurrent_application.json"
    path.write_text(json.dumps(jsonable(result), indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "out": str(path),
                "recurrent_candidates": result["diagnostics"]["recurrent_candidates"],
                "best_target": result.get("posthoc_target_reveal", {}).get("best"),
                "best_leaf_target": result.get("posthoc_leaf_target_reveal", {}).get("best"),
                "best_final_leaf_target": result.get("posthoc_final_leaf_target_reveal", {}).get("best"),
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
