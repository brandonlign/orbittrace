#!/usr/bin/env python3
"""Run the frozen post-hoc ACRF-v3.5 core-hyperparameter robustness grid.

This is a robustness analysis, not a method-selection lane. Candidate generation
and ranking are target-free for every cell. The fixed OrbitTrace table is opened
only after ranking to track the corresponding family across parameter settings.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, replace
import itertools
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np
import pandas as pd

# Direct script execution starts with this file's directory on ``sys.path``.
# Add the repository root so the frozen package imports work identically from
# a checkout, GitHub Actions, and a module-oriented local runner.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.pr57_novel import run_novel_search as base
from pipeline.unified_v2.application import _feature_panel, _prepare
from pipeline.unified_v3.config import V3Config
from pipeline.unified_v3.membership import expand_candidate
from pipeline.unified_v3.method import _apply_orbit_gate, generate_multiscale_candidates

YEARS = (2022, 2023, 2024, 2025, 2026)
SEED_YEARS = (2025, 2026)
MONTH = 4
TARGET = Path("candidate/mdc/OrbitTrace_April_95_GMN_lookup.csv")

BASE_SCALES = (3.5, 3.0, 2.5, 2.5)
LON_SCALES = (2.5, 3.5, 4.5)
LAT_SCALES = (2.0, 3.0, 4.0)
SPEED_SCALES = (1.5, 2.5, 3.5)
SOLAR_SCALES = (1.5, 2.5, 3.5)
MCS_LEVELS = (6, 8, 12)
MS_LEVELS = (2, 4, 6)
HDBSCAN_CORNERS = ((6, 2), (6, 6), (12, 2), (12, 6))
RAW_DESIGN_CELLS = 154
UNIQUE_PARAMETER_SETTINGS = 153

BASELINE_EXPECTED = {
    "rank": 7,
    "final_member_count": 123,
    "final_overlap": 95,
    "target_count": 95,
    "final_precision": 0.7723577235772358,
    "final_recall": 1.0,
    "final_f1": 0.8715596330275228,
}


def timestamp_key(value: Any) -> str:
    digits = "".join(character for character in str(value) if character.isdigit())
    return digits[:14]


def target_keys(years: tuple[int, ...]) -> set[str]:
    frame = pd.read_csv(TARGET)
    timestamps = pd.to_datetime(frame["Tobs"], format="%Y-%m-%d-%H:%M:%S", errors="coerce")
    return {
        value.strftime("%Y%m%d%H%M%S")
        for value in timestamps.dropna()
        if int(value.year) in years
    }


def build_grid() -> list[dict[str, Any]]:
    """Return the preregistered 154-cell union with provenance labels."""
    settings: dict[tuple[float, float, float, float, int, int], set[str]] = {}

    def add(scales: tuple[float, float, float, float], mcs: int, ms: int, source: str) -> None:
        key = (*map(float, scales), int(mcs), int(ms))
        settings.setdefault(key, set()).add(source)

    for scales in itertools.product(LON_SCALES, LAT_SCALES, SPEED_SCALES, SOLAR_SCALES):
        add(tuple(map(float, scales)), 8, 4, "scale_factorial")

    for mcs, ms in itertools.product(MCS_LEVELS, MS_LEVELS):
        add(BASE_SCALES, int(mcs), int(ms), "hdbscan_factorial")

    for scales in itertools.product(
        (LON_SCALES[0], LON_SCALES[-1]),
        (LAT_SCALES[0], LAT_SCALES[-1]),
        (SPEED_SCALES[0], SPEED_SCALES[-1]),
        (SOLAR_SCALES[0], SOLAR_SCALES[-1]),
    ):
        for mcs, ms in HDBSCAN_CORNERS:
            add(tuple(map(float, scales)), int(mcs), int(ms), "joint_extreme_interactions")

    rows = []
    for key in sorted(settings):
        lon, lat, speed, solar, mcs, ms = key
        rows.append(
            {
                "feature_scales": [lon, lat, speed, solar],
                "min_cluster_size": mcs,
                "min_samples": ms,
                "grid_sources": sorted(settings[key]),
            }
        )
    if len(rows) != UNIQUE_PARAMETER_SETTINGS:
        raise RuntimeError(
            "Frozen grid should contain "
            f"{UNIQUE_PARAMETER_SETTINGS} unique settings from {RAW_DESIGN_CELLS} raw cells, "
            f"found {len(rows)}"
        )
    return rows


def load_panel() -> dict[str, Any]:
    data_frames = []
    year_arrays = []
    ids: list[str] = []
    metadata = {}
    for year in YEARS:
        prepared = _prepare(base.load_month(year, MONTH), year, MONTH)
        data = prepared["data"].copy()
        event_ids = data["unique_trajectory_identifier"].astype(str).to_numpy()
        if len(set(event_ids.tolist())) != len(event_ids):
            raise RuntimeError(f"Duplicate event IDs in {year}-{MONTH:02d}")
        data_frames.append(data)
        year_arrays.append(np.full(len(data), year, dtype=np.int64))
        ids.extend(event_ids.tolist())
        metadata[str(year)] = {
            "rows": int(len(data)),
            "quality_rows_before_sampling": int(prepared["quality_rows"]),
        }
    all_data = pd.concat(data_frames, ignore_index=True, sort=False)
    years = np.concatenate(year_arrays)
    event_ids = np.asarray(ids, dtype=str)
    if len(set(event_ids.tolist())) != len(event_ids):
        raise RuntimeError("Event IDs must be unique across the five-year panel")
    return {
        "frames": data_frames,
        "data": all_data,
        "years": years,
        "event_ids": event_ids,
        "orbit_matrix": all_data[base.ORBIT_COLUMNS].to_numpy(float),
        "solar": all_data["sol_lon_deg"].to_numpy(float),
        "metadata": metadata,
    }


def matrix_for_config(frames: list[pd.DataFrame], config: V3Config) -> np.ndarray:
    return np.vstack([_feature_panel(frame, config) for frame in frames])


def score_ids(ids: list[str] | tuple[str, ...], target: set[str]) -> dict[str, float | int]:
    reported = {timestamp_key(value) for value in ids}
    overlap = len(reported & target)
    precision = overlap / len(reported) if reported else 0.0
    recall = overlap / len(target) if target else 0.0
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "reported": int(len(reported)),
        "overlap": int(overlap),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
    }


def evaluate_setting(
    setting_index: int,
    setting: dict[str, Any],
    panel: dict[str, Any],
    all_target: set[str],
    seed_target: set[str],
) -> dict[str, Any]:
    scales = tuple(float(value) for value in setting["feature_scales"])
    config = replace(
        V3Config(),
        feature_scales=scales,
        min_cluster_size=int(setting["min_cluster_size"]),
        min_samples=int(setting["min_samples"]),
    )
    matrix = matrix_for_config(panel["frames"], config)
    years = panel["years"]
    event_ids = panel["event_ids"]
    seed_mask = np.isin(years, np.asarray(SEED_YEARS, dtype=np.int64))

    candidates, diagnostics = generate_multiscale_candidates(
        matrix[seed_mask],
        years[seed_mask],
        event_ids[seed_mask],
        panel["solar"][seed_mask],
        config,
    )

    tracked: list[tuple[float, int, int, dict[str, Any], dict[str, float | int]]] = []
    for candidate in candidates:
        seed_metrics = score_ids(candidate.get("event_ids", []), seed_target)
        if int(seed_metrics["overlap"]) == 0:
            continue
        tracked.append(
            (
                float(seed_metrics["f1"]),
                int(seed_metrics["overlap"]),
                -int(candidate["global_rank"]),
                candidate,
                seed_metrics,
            )
        )

    base_row: dict[str, Any] = {
        "setting_index": int(setting_index),
        "grid_sources": "+".join(setting["grid_sources"]),
        "lon_scale_deg": scales[0],
        "lat_scale_deg": scales[1],
        "speed_scale_km_s": scales[2],
        "solar_scale_deg": scales[3],
        "min_cluster_size": int(config.min_cluster_size),
        "min_samples": int(config.min_samples),
        "ranked_candidate_count": int(len(candidates)),
        "raw_candidate_count": int(diagnostics.get("raw_candidates", 0)),
        "target_opened_only_after_ranking": True,
        "materialization_budget": 100,
        "tracked": False,
        "rank": None,
        "family_id": None,
        "hierarchy_method": None,
        "membership_mode": None,
        "seed_reported": 0,
        "seed_overlap": 0,
        "seed_precision": 0.0,
        "seed_recall": 0.0,
        "seed_f1": 0.0,
        "within_top100": False,
        "final_member_count": 0,
        "final_overlap": 0,
        "target_count": int(len(all_target)),
        "final_precision": 0.0,
        "final_recall": 0.0,
        "final_f1": 0.0,
        "overlap_2022": 0,
        "overlap_2023": 0,
        "overlap_2024": 0,
        "overlap_2025": 0,
        "overlap_2026": 0,
    }
    if not tracked:
        return base_row

    tracked.sort(key=lambda item: (-item[0], -item[1], -item[2]))
    _f1, _overlap, _negative_rank, candidate, seed_metrics = tracked[0]
    rank = int(candidate["global_rank"])
    base_row.update(
        {
            "tracked": True,
            "rank": rank,
            "family_id": str(candidate["family_id"]),
            "hierarchy_method": str(candidate.get("hierarchy_method")),
            "membership_mode": str(candidate.get("membership_mode")),
            "seed_reported": int(seed_metrics["reported"]),
            "seed_overlap": int(seed_metrics["overlap"]),
            "seed_precision": float(seed_metrics["precision"]),
            "seed_recall": float(seed_metrics["recall"]),
            "seed_f1": float(seed_metrics["f1"]),
            "within_top100": rank <= 100,
        }
    )
    if rank > 100:
        return base_row

    if candidate.get("membership_mode") == "hierarchy_core":
        final_ids = sorted(map(str, candidate.get("event_ids", [])))
    else:
        full_index = {event_id: index for index, event_id in enumerate(event_ids.tolist())}
        expanded_input = dict(candidate)
        expanded_input["members"] = [full_index[str(value)] for value in candidate["event_ids"]]
        expanded = expand_candidate(expanded_input, matrix, years, event_ids, config)
        gated = _apply_orbit_gate(expanded, panel["orbit_matrix"], event_ids, config)
        final_ids = sorted(map(str, gated["final_event_ids"]))

    final_metrics = score_ids(final_ids, all_target)
    final_keys = {timestamp_key(value) for value in final_ids}
    overlap_keys = final_keys & all_target
    base_row.update(
        {
            "final_member_count": int(final_metrics["reported"]),
            "final_overlap": int(final_metrics["overlap"]),
            "final_precision": float(final_metrics["precision"]),
            "final_recall": float(final_metrics["recall"]),
            "final_f1": float(final_metrics["f1"]),
        }
    )
    for year in YEARS:
        base_row[f"overlap_{year}"] = int(sum(value.startswith(str(year)) for value in overlap_keys))
    return base_row


def baseline_match(row: dict[str, Any]) -> bool:
    return (
        row["lon_scale_deg"] == 3.5
        and row["lat_scale_deg"] == 3.0
        and row["speed_scale_km_s"] == 2.5
        and row["solar_scale_deg"] == 2.5
        and row["min_cluster_size"] == 8
        and row["min_samples"] == 4
    )


def assert_baseline(row: dict[str, Any]) -> None:
    exact = {
        "rank": int(row["rank"]) if row["rank"] is not None else None,
        "final_member_count": int(row["final_member_count"]),
        "final_overlap": int(row["final_overlap"]),
        "target_count": int(row["target_count"]),
    }
    for key, expected in BASELINE_EXPECTED.items():
        observed = row[key]
        if isinstance(expected, float):
            if not np.isclose(float(observed), expected, atol=1e-12, rtol=1e-12):
                raise RuntimeError(f"Baseline mismatch for {key}: observed {observed}, expected {expected}")
        elif exact.get(key, observed) != expected:
            raise RuntimeError(f"Baseline mismatch for {key}: observed {observed}, expected {expected}")


def write_rows(rows: list[dict[str, Any]], out: Path, metadata: dict[str, Any], shard: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows).sort_values("setting_index")
    frame.to_csv(out / f"hyperparameter_cells_{shard}.csv", index=False)
    payload = {
        "stage": "acrf_v3_5_frozen_core_hyperparameter_robustness_shard",
        "shard": shard,
        "grid_cell_count": int(len(rows)),
        "input": metadata,
        "rows": rows,
    }
    (out / f"hyperparameter_cells_{shard}.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def run_shard(out: Path, shard_index: int, shard_count: int) -> int:
    grid = build_grid()
    selected = [(index, row) for index, row in enumerate(grid) if index % shard_count == shard_index]
    print(f"Shard {shard_index}/{shard_count}: {len(selected)} of {len(grid)} settings", flush=True)
    panel = load_panel()
    all_target = target_keys(YEARS)
    seed_target = target_keys(SEED_YEARS)
    if len(all_target) != 95 or len(seed_target) != 63:
        raise RuntimeError(f"Unexpected target counts: all={len(all_target)}, seed={len(seed_target)}")
    rows = []
    for position, (index, setting) in enumerate(selected, start=1):
        print(
            f"[{position}/{len(selected)}] cell={index} scales={setting['feature_scales']} "
            f"mcs={setting['min_cluster_size']} ms={setting['min_samples']}",
            flush=True,
        )
        row = evaluate_setting(index, setting, panel, all_target, seed_target)
        rows.append(row)
        print(
            f"  rank={row['rank']} seed={row['seed_overlap']}/63 final={row['final_overlap']}/95 "
            f"N={row['final_member_count']} F1={row['final_f1']:.4f}",
            flush=True,
        )
    write_rows(rows, out, panel["metadata"], f"shard{shard_index}")
    return 0


def aggregate(inputs: list[Path], out: Path) -> int:
    csv_paths = []
    for path in inputs:
        if path.is_dir():
            csv_paths.extend(sorted(path.rglob("hyperparameter_cells_shard*.csv")))
        elif path.suffix.lower() == ".csv":
            csv_paths.append(path)
    if not csv_paths:
        raise RuntimeError("No shard CSV files found")
    frame = pd.concat([pd.read_csv(path) for path in csv_paths], ignore_index=True)
    frame = frame.drop_duplicates(subset=["setting_index"], keep=False).sort_values("setting_index")
    if len(frame) != UNIQUE_PARAMETER_SETTINGS or set(frame["setting_index"].astype(int)) != set(
        range(UNIQUE_PARAMETER_SETTINGS)
    ):
        raise RuntimeError(
            "Expected exactly "
            f"{UNIQUE_PARAMETER_SETTINGS} unique settings from {RAW_DESIGN_CELLS} raw cells, "
            f"found {len(frame)}"
        )
    rows = frame.to_dict(orient="records")
    baseline_rows = [row for row in rows if baseline_match(row)]
    if len(baseline_rows) != 1:
        raise RuntimeError(f"Expected one baseline row, found {len(baseline_rows)}")
    assert_baseline(baseline_rows[0])

    tracked = frame[frame["tracked"] == True]  # noqa: E712
    top100 = tracked[tracked["within_top100"] == True]  # noqa: E712

    def min_median_max(series: pd.Series, integer: bool = False) -> dict[str, float | int | None]:
        if len(series) == 0:
            return {"min": None, "median": None, "max": None}
        values = {
            "min": float(series.min()),
            "median": float(series.median()),
            "max": float(series.max()),
        }
        if integer:
            values = {
                key: int(value) if key != "median" else value
                for key, value in values.items()
            }
        return values

    summary = {
        "stage": "acrf_v3_5_frozen_core_hyperparameter_robustness",
        "raw_design_cells": RAW_DESIGN_CELLS,
        "unique_parameter_settings": UNIQUE_PARAMETER_SETTINGS,
        "executed_unique_cells": int(len(frame)),
        "baseline_reproduced": True,
        "tracked_cells": int(len(tracked)),
        "rank_le_100_cells": int(len(top100)),
        "rank_le_100_fraction": float(len(top100) / len(frame)),
        "exact_95_recovery_cells": int((frame["final_overlap"] == 95).sum()),
        "exact_95_recovery_fraction": float((frame["final_overlap"] == 95).mean()),
        "at_least_90_recovery_cells": int((frame["final_overlap"] >= 90).sum()),
        "at_least_90_recovery_fraction": float((frame["final_overlap"] >= 90).mean()),
        "at_least_80_recovery_cells": int((frame["final_overlap"] >= 80).sum()),
        "at_least_80_recovery_fraction": float((frame["final_overlap"] >= 80).mean()),
        "rank_quantiles_tracked": {
            str(q): float(tracked["rank"].quantile(q)) if len(tracked) else None
            for q in (0.0, 0.25, 0.5, 0.75, 1.0)
        },
        "final_overlap_quantiles_all_cells": {
            str(q): float(frame["final_overlap"].quantile(q))
            for q in (0.0, 0.25, 0.5, 0.75, 1.0)
        },
        "final_f1_quantiles_top100": {
            str(q): float(top100["final_f1"].quantile(q)) if len(top100) else None
            for q in (0.0, 0.25, 0.5, 0.75, 1.0)
        },
        "member_count_range_top100": [
            int(top100["final_member_count"].min()) if len(top100) else None,
            int(top100["final_member_count"].max()) if len(top100) else None,
        ],
        "min_median_max": {
            "rank_tracked": min_median_max(tracked["rank"], integer=True),
            "final_recall_top100": min_median_max(top100["final_recall"]),
            "final_precision_top100": min_median_max(top100["final_precision"]),
            "final_f1_top100": min_median_max(top100["final_f1"]),
            "final_member_count_top100": min_median_max(top100["final_member_count"], integer=True),
            "final_recall_all_cells": min_median_max(frame["final_recall"]),
            "final_precision_all_cells": min_median_max(frame["final_precision"]),
            "final_f1_all_cells": min_median_max(frame["final_f1"]),
            "final_member_count_all_cells": min_median_max(frame["final_member_count"], integer=True),
        },
        "annual_exact_overlap_cells": {
            str(year): int((frame[f"overlap_{year}"] == count).sum())
            for year, count in ((2022, 10), (2023, 8), (2024, 14), (2025, 34), (2026, 29))
        },
        "grid_breakdown": {},
        "interpretation_rule": "This is post-hoc robustness of the frozen ACRF-v3.5 method. Results do not authorize hyperparameter replacement or tuning.",
    }
    for source in ("scale_factorial", "hdbscan_factorial", "joint_extreme_interactions"):
        subset = frame[frame["grid_sources"].astype(str).str.contains(source, regex=False)]
        summary["grid_breakdown"][source] = {
            "cells": int(len(subset)),
            "rank_le_100_fraction": float((subset["within_top100"] == True).mean()),  # noqa: E712
            "exact_95_fraction": float((subset["final_overlap"] == 95).mean()),
            "at_least_90_fraction": float((subset["final_overlap"] >= 90).mean()),
            "at_least_80_fraction": float((subset["final_overlap"] >= 80).mean()),
            "median_final_overlap": float(subset["final_overlap"].median()),
            "minimum_final_overlap": int(subset["final_overlap"].min()),
            "maximum_final_overlap": int(subset["final_overlap"].max()),
        }

    out.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out / "hyperparameter_sensitivity_cells.csv", index=False)
    (out / "hyperparameter_sensitivity_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    def min_median_max_text(item: dict[str, float | int | None]) -> str:
        return f"{item['min']} / {item['median']} / {item['max']}"

    lines = [
        "# ACRF-v3.5 core-hyperparameter robustness", "",
        "This is a frozen post-hoc sensitivity analysis. It does not select or retune the paper method.", "",
        f"- Raw design cells: **{summary['raw_design_cells']}**",
        f"- Unique parameter settings executed: **{summary['unique_parameter_settings']}**",
        f"- Baseline reproduced exactly: **{summary['baseline_reproduced']}**",
        f"- Tracked family within rank 100: **{summary['rank_le_100_cells']}/{summary['unique_parameter_settings']} ({summary['rank_le_100_fraction']:.1%})**",
        f"- Exact 95/95 recovery: **{summary['exact_95_recovery_cells']}/{summary['unique_parameter_settings']} ({summary['exact_95_recovery_fraction']:.1%})**",
        f"- At least 90/95 recovery: **{summary['at_least_90_recovery_cells']}/{summary['unique_parameter_settings']} ({summary['at_least_90_recovery_fraction']:.1%})**",
        f"- At least 80/95 recovery: **{summary['at_least_80_recovery_cells']}/{summary['unique_parameter_settings']} ({summary['at_least_80_recovery_fraction']:.1%})**", "",
        "## Min/median/max metrics", "",
        "Final metrics are reported for cells whose selected family was within the preregistered top-100 materialization budget; all-cell values are also retained in the JSON summary.", "",
        f"- Rank (tracked), min / median / max: **{min_median_max_text(summary['min_median_max']['rank_tracked'])}**",
        f"- Final recall (top-100), min / median / max: **{min_median_max_text(summary['min_median_max']['final_recall_top100'])}**",
        f"- Final precision (top-100), min / median / max: **{min_median_max_text(summary['min_median_max']['final_precision_top100'])}**",
        f"- Final F1 (top-100), min / median / max: **{min_median_max_text(summary['min_median_max']['final_f1_top100'])}**",
        f"- Final member count (top-100), min / median / max: **{min_median_max_text(summary['min_median_max']['final_member_count_top100'])}**", "",
        "## Grid-specific results", "",
    ]
    for source, item in summary["grid_breakdown"].items():
        lines.extend(
            [
                f"### {source}", "",
                f"- Cells: {item['cells']}",
                f"- Rank <= 100: {item['rank_le_100_fraction']:.1%}",
                f"- Exact 95/95: {item['exact_95_fraction']:.1%}",
                f"- >=90/95: {item['at_least_90_fraction']:.1%}",
                f"- >=80/95: {item['at_least_80_fraction']:.1%}",
                f"- Final overlap median/range: {item['median_final_overlap']:.1f} / {item['minimum_final_overlap']}-{item['maximum_final_overlap']}", "",
            ]
        )
    (out / "HYPERPARAMETER_ROBUSTNESS.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--shard-index", type=int)
    parser.add_argument("--shard-count", type=int)
    parser.add_argument("--aggregate", nargs="*", type=Path)
    args = parser.parse_args()
    if args.aggregate is not None:
        return aggregate(args.aggregate, args.out)
    if args.shard_index is None or args.shard_count is None:
        parser.error("shard mode requires --shard-index and --shard-count")
    if not 0 <= args.shard_index < args.shard_count:
        parser.error("invalid shard index/count")
    return run_shard(args.out, args.shard_index, args.shard_count)


if __name__ == "__main__":
    raise SystemExit(main())
