"""Run target-free ACRF-v3.5 on the five-year April GMN panel."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from pipeline.pr57_novel import run_novel_search as base
from pipeline.unified_v2.application import _feature_panel, _prepare

from .config import V3Config
from .method import build_multiscale_catalogue


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return [_jsonable(item) for item in value.tolist()]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def run(
    years: tuple[int, ...] = (2022, 2023, 2024, 2025, 2026),
    month: int = 4,
    seed_years: tuple[int, ...] = (2025, 2026),
    expansion_limit: int = 100,
    config: V3Config | None = None,
) -> dict[str, Any]:
    config = config or V3Config()
    if len(years) < 2 or any(year not in years for year in seed_years):
        raise ValueError("seed_years must be observed years")
    matrices = []
    orbit_panels = []
    solar_panels = []
    year_panels = []
    ids: list[str] = []
    metadata: dict[str, Any] = {}
    for year in years:
        prepared = _prepare(base.load_month(int(year), int(month)), int(year), int(month))
        data = prepared["data"]
        matrix = _feature_panel(data, config)
        event_ids = data["unique_trajectory_identifier"].astype(str).to_numpy()
        if len(set(event_ids.tolist())) != len(event_ids):
            raise RuntimeError(f"duplicate trajectory identifiers in {year}-{month:02d}")
        matrices.append(matrix)
        orbit_panels.append(data[base.ORBIT_COLUMNS].to_numpy(float))
        solar_panels.append(data["sol_lon_deg"].to_numpy(float))
        year_panels.append(np.full(len(data), int(year), dtype=np.int64))
        ids.extend(event_ids.tolist())
        metadata[str(year)] = {
            "rows": int(len(data)),
            "quality_rows_before_sampling": int(prepared["quality_rows"]),
            "solar_center": float(prepared["center_sol"]),
            "catalogue_labels_used_only_for_known_shower_exclusion": True,
            "orbittrace_target_membership_accessed": False,
        }
        print(f"{year}-{month:02d}: prepared {len(data):,} sporadic rows", flush=True)
    matrix = np.vstack(matrices)
    orbit_matrix = np.vstack(orbit_panels)
    solar = np.concatenate(solar_panels)
    year_array = np.concatenate(year_panels)
    event_ids = np.asarray(ids, dtype=str)
    if len(set(event_ids.tolist())) != len(event_ids):
        raise RuntimeError("trajectory identifiers must be unique across the application panel")
    candidates, diagnostics = build_multiscale_catalogue(
        matrix,
        year_array,
        event_ids,
        solar,
        orbit_matrix,
        config,
        expansion_limit=int(expansion_limit),
        seed_years=seed_years,
    )
    result = {
        "stage": "acrf_v3_5_target_free_orbittrace_application",
        "method": "ACRF-v3.5",
        "years": list(years),
        "seed_years": list(seed_years),
        "month": int(month),
        "config": asdict(config),
        "input": metadata,
        "diagnostics": diagnostics,
        "target_accessed_during_generation_ranking_or_membership": False,
        "candidate_count": int(len(candidates)),
        "materialized_final_memberships": int(
            sum("final_event_ids" in candidate for candidate in candidates)
        ),
        "candidate_seed_order_sha256": hashlib.sha256(
            "\n".join("|".join(candidate["event_ids"]) for candidate in candidates).encode()
        ).hexdigest(),
        "materialized_final_order_sha256": hashlib.sha256(
            "\n".join(
                "|".join(candidate.get("final_event_ids", ()))
                for candidate in candidates
                if "final_event_ids" in candidate
            ).encode()
        ).hexdigest(),
        "candidates": candidates,
    }
    return _jsonable(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--years", default="2022,2023,2024,2025,2026")
    parser.add_argument("--seed-years", default="2025,2026")
    parser.add_argument("--month", type=int, default=4)
    parser.add_argument("--expansion-limit", type=int, default=100)
    args = parser.parse_args()
    result = run(
        tuple(int(value) for value in args.years.split(",") if value),
        int(args.month),
        tuple(int(value) for value in args.seed_years.split(",") if value),
        int(args.expansion_limit),
    )
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "application_v3_5.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "out": str(path),
                "candidates": result["candidate_count"],
                "materialized": result["materialized_final_memberships"],
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
