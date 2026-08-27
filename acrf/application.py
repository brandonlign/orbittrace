"""Apply ACRF to a prepared, label-free trajectory panel."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .config import ACRFConfig
from .features import circular_center_deg, circular_difference_deg, periodic_physical6_from_raw
from .method import build_multiscale_catalogue


REQUIRED_COLUMNS = (
    "event_id", "year", "sol_lon_deg", "lamgeo_deg", "betgeo_deg", "vgeo_km_s",
    "e", "q", "inc", "peri", "node",
)
NUMERIC_COLUMNS = REQUIRED_COLUMNS[1:]


def feature_panel(data: pd.DataFrame, config: ACRFConfig) -> np.ndarray:
    solar = data["sol_lon_deg"].to_numpy(float)
    raw = np.column_stack(
        (
            circular_difference_deg(data["lamgeo_deg"].to_numpy(float), solar),
            data["betgeo_deg"].to_numpy(float),
            data["vgeo_km_s"].to_numpy(float),
            circular_difference_deg(solar, circular_center_deg(solar)),
        )
    )
    return periodic_physical6_from_raw(raw, config.feature_scales)


def load_panel(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ValueError(f"prepared panel is missing columns: {missing}")

    data = data.loc[:, REQUIRED_COLUMNS].copy()
    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="raise")

    numeric = data.loc[:, NUMERIC_COLUMNS].to_numpy(float)
    if not np.isfinite(numeric).all():
        bad_columns = [
            column
            for index, column in enumerate(NUMERIC_COLUMNS)
            if not np.isfinite(numeric[:, index]).all()
        ]
        raise ValueError(f"prepared panel contains non-finite values in: {bad_columns}")

    years = data["year"].to_numpy(float)
    if not np.equal(years, np.floor(years)).all():
        raise ValueError("year values must be whole numbers")
    data["year"] = years.astype(np.int64)

    data["event_id"] = data["event_id"].astype(str).str.strip()
    if (data["event_id"] == "").any():
        raise ValueError("event_id cannot be empty")
    if data["event_id"].duplicated().any():
        raise ValueError("event_id must be unique in the prepared panel")
    if data["year"].nunique() < 2:
        raise ValueError("at least two observing years are required")
    if ((data["vgeo_km_s"] <= 0.0) | (data["q"] <= 0.0) | (data["e"] < 0.0)).any():
        raise ValueError("speed and perihelion distance must be positive, and eccentricity cannot be negative")

    return data.reset_index(drop=True)


def run(
    data: pd.DataFrame,
    *,
    config: ACRFConfig | None = None,
    seed_years: tuple[int, ...] = (2025, 2026),
    expansion_limit: int = 100,
) -> dict[str, Any]:
    config = config or ACRFConfig()
    years = data["year"].astype(int).to_numpy()
    observed_years = set(years.tolist())
    if len(seed_years) < 2 or any(year not in observed_years for year in seed_years):
        raise ValueError("seed_years must contain at least two years present in the panel")
    if len(set(seed_years)) != len(seed_years):
        raise ValueError("seed_years must not contain duplicates")
    if expansion_limit < 1:
        raise ValueError("expansion_limit must be positive")

    matrix = feature_panel(data, config)
    event_ids = data["event_id"].astype(str).to_numpy()
    solar = data["sol_lon_deg"].to_numpy(float)
    orbit = data[["e", "q", "inc", "peri", "node"]].to_numpy(float)
    candidates, diagnostics = build_multiscale_catalogue(
        matrix, years, event_ids, solar, orbit, config,
        expansion_limit=int(expansion_limit), seed_years=seed_years,
    )
    return {
        "stage": "acrf_target_free_application",
        "method": "ACRF",
        "years": sorted(set(int(year) for year in years)),
        "seed_years": list(seed_years),
        "config": asdict(config),
        "input_rows": int(len(data)),
        "target_accessed_during_generation_or_ranking": False,
        "diagnostics": diagnostics,
        "candidate_count": int(len(candidates)),
        "candidate_seed_order_sha256": hashlib.sha256(
            "\n".join("|".join(candidate["event_ids"]) for candidate in candidates).encode()
        ).hexdigest(),
        "candidates": candidates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed-years", default="2025,2026")
    args = parser.parse_args()
    result = run(
        load_panel(args.panel),
        seed_years=tuple(int(value) for value in args.seed_years.split(",") if value),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(args.out), "candidates": result["candidate_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
