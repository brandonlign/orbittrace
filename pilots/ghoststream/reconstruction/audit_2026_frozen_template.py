#!/usr/bin/env python3
"""Audit plausible reconstructions of the 2026-frozen GhostStream template.

The later published center/widths are refined from the multi-year sample. This
script reconstructs a discovery-stage template using only the 29 preserved 2026
lookup members, then reports a complete prespecified grid across:

- exact-timestamp versus UTC-second deduplication;
- diagonal Euclidean, full-covariance Mahalanobis, and coordinate-box cores;
- 2.5, 3.0, and 3.5 sigma radii.

All variants are reported. The script does not select a favorable variant as a
new primary result and does not alter the committed preserved lookup.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

import reproduce_primary_gmn_monthly as base

OUTPUT_DEFAULT = Path("pilots/ghoststream/reconstruction/template_ambiguity_audit")
DEDUP_MODES = ("exact_timestamp", "utc_second")
CORE_METRICS = ("diagonal_euclidean", "full_covariance", "coordinate_box")
RADII = (2.5, 3.0, 3.5)


def quality_filter(frame: pd.DataFrame, year: int) -> pd.DataFrame:
    data = frame.copy()
    data["beginning_utc_time"] = pd.to_datetime(data["beginning_utc_time"], errors="coerce", utc=False)
    data["event_second"] = data["beginning_utc_time"].dt.floor("S")
    data["year"] = year
    finite = np.isfinite(data[base.FINITE_COLUMNS].to_numpy(dtype=float)).all(axis=1)
    mask = (
        data["beginning_utc_time"].notna()
        & (data["iau_no"] == -1)
        & (data["num_stat"] >= 2)
        & data["medianfiterr_arcsec"].notna()
        & (data["medianfiterr_arcsec"] <= 180.0)
        & data["vgeo_km_s"].between(5.0, 75.0, inclusive="both")
        & finite
    )
    return data.loc[mask].copy()


def deduplicate(frame: pd.DataFrame, mode: str) -> pd.DataFrame:
    key = "beginning_utc_time" if mode == "exact_timestamp" else "event_second"
    ordered = frame.sort_values(
        [key, "medianfiterr_arcsec", "num_stat", "unique_trajectory_identifier"],
        ascending=[True, True, False, True],
        kind="mergesort",
    )
    return ordered.drop_duplicates(key, keep="first").copy()


def lookup_time(value: str) -> str:
    return value[:10] + " " + value[11:]


def circular_delta(left: float, right: float) -> float:
    return float(base.wrap180(left - right))


def lookup_distance(row: pd.Series, lookup: dict[str, str]) -> float:
    mapping = {
        "rageo_deg": "RA", "decgeo_deg": "DE", "vgeo_km_s": "VG",
        "sol_lon_deg": "LS", "lamgeo_deg": "LO", "betgeo_deg": "LA",
    }
    total = 0.0
    for source_key, lookup_key in mapping.items():
        actual = float(row[source_key])
        expected = float(lookup[lookup_key])
        delta = circular_delta(actual, expected) if source_key in {"rageo_deg", "sol_lon_deg", "lamgeo_deg"} else actual - expected
        total += delta * delta
    actual_sclo = (float(row["lamgeo_deg"]) - float(row["sol_lon_deg"])) % 360.0
    expected_sclo = float(lookup["SCLO"]) % 360.0
    total += circular_delta(actual_sclo, expected_sclo) ** 2
    return math.sqrt(total)


def recover_training_rows(frame_2026: pd.DataFrame, lookup_rows: list[dict[str, str]]) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    lookup_2026 = [row for row in lookup_rows if row["Tobs"].startswith("2026-")]
    if len(lookup_2026) != 29:
        raise RuntimeError(f"Expected 29 preserved 2026 lookup members, found {len(lookup_2026)}")
    selected: list[pd.Series] = []
    evidence: list[dict[str, Any]] = []
    for lookup in lookup_2026:
        timestamp = pd.Timestamp(lookup_time(lookup["Tobs"]))
        candidates = frame_2026.loc[frame_2026["event_second"] == timestamp]
        if candidates.empty:
            raise RuntimeError(f"Preserved 2026 lookup event missing from official source: {timestamp}")
        ranked = sorted(
            ((lookup_distance(row, lookup), index, row) for index, row in candidates.iterrows()),
            key=lambda item: (item[0], float(item[2]["medianfiterr_arcsec"]), -int(item[2]["num_stat"]), str(item[2]["unique_trajectory_identifier"])),
        )
        distance, _, chosen = ranked[0]
        selected.append(chosen)
        evidence.append({
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "candidate_rows_at_second": len(candidates),
            "selected_identifier": str(chosen["unique_trajectory_identifier"]),
            "lookup_field_distance": distance,
        })
    training = pd.DataFrame(selected).reset_index(drop=True)
    if training["event_second"].duplicated().any():
        raise RuntimeError("Recovered 2026 training rows contain duplicate UTC seconds")
    return training, evidence


def fit_template(training: pd.DataFrame) -> dict[str, Any]:
    delta_sol = np.asarray(base.wrap180(training["sol_lon_deg"].to_numpy(float) - base.EPOCH), dtype=float)
    design = np.column_stack([np.ones(len(training)), delta_sol])
    targets = []
    parameters: dict[str, Any] = {}
    for name, column in (("sun_lon", "sun_lon_deg"), ("latitude", "betgeo_deg"), ("speed", "vgeo_km_s")):
        if column == "sun_lon_deg":
            values = (training["lamgeo_deg"].to_numpy(float) - training["sol_lon_deg"].to_numpy(float)) % 360.0
            values = 210.0 + np.asarray(base.wrap180(values - 210.0), dtype=float)
        else:
            values = training[column].to_numpy(float)
        coefficients = np.linalg.lstsq(design, values, rcond=None)[0]
        residuals = values - design @ coefficients
        targets.append(residuals)
        parameters[name] = {
            "intercept_at_epoch": float(coefficients[0]),
            "slope_per_solar_longitude_degree": float(coefficients[1]),
            "sample_sigma": float(np.std(residuals, ddof=1)),
        }
    residual_matrix = np.column_stack(targets)
    covariance = np.cov(residual_matrix, rowvar=False, ddof=1)
    inverse = np.linalg.inv(covariance)
    return {
        "epoch_solar_longitude_deg": base.EPOCH,
        "parameters": parameters,
        "covariance": covariance.tolist(),
        "correlation": np.corrcoef(residual_matrix, rowvar=False).tolist(),
        "inverse_covariance": inverse.tolist(),
        "training_residuals": residual_matrix,
    }


def apply_template(frame: pd.DataFrame, template: dict[str, Any]) -> pd.DataFrame:
    result = frame.copy()
    result["delta_sol_deg"] = base.wrap180(result["sol_lon_deg"] - base.EPOCH)
    result["sun_lon_deg"] = (result["lamgeo_deg"] - result["sol_lon_deg"]) % 360.0
    result["sun_lon_unwrapped"] = 210.0 + base.wrap180(result["sun_lon_deg"] - 210.0)
    p = template["parameters"]
    result["expected_sun_lon_deg"] = p["sun_lon"]["intercept_at_epoch"] + p["sun_lon"]["slope_per_solar_longitude_degree"] * result["delta_sol_deg"]
    result["expected_betgeo_deg"] = p["latitude"]["intercept_at_epoch"] + p["latitude"]["slope_per_solar_longitude_degree"] * result["delta_sol_deg"]
    result["expected_vgeo_km_s"] = p["speed"]["intercept_at_epoch"] + p["speed"]["slope_per_solar_longitude_degree"] * result["delta_sol_deg"]
    result["residual_sun_lon_deg"] = result["sun_lon_unwrapped"] - result["expected_sun_lon_deg"]
    result["residual_betgeo_deg"] = result["betgeo_deg"] - result["expected_betgeo_deg"]
    result["residual_vgeo_km_s"] = result["vgeo_km_s"] - result["expected_vgeo_km_s"]
    sigmas = np.array([
        p["sun_lon"]["sample_sigma"], p["latitude"]["sample_sigma"], p["speed"]["sample_sigma"]
    ])
    residuals = result[["residual_sun_lon_deg", "residual_betgeo_deg", "residual_vgeo_km_s"]].to_numpy(float)
    standardized = residuals / sigmas
    result["diagonal_euclidean_score"] = np.sum(standardized ** 2, axis=1)
    result["coordinate_box_score"] = np.max(np.abs(standardized), axis=1)
    inverse = np.asarray(template["inverse_covariance"], dtype=float)
    result["full_covariance_score"] = np.einsum("ij,jk,ik->i", residuals, inverse, residuals)
    return result


def core_mask(frame: pd.DataFrame, metric: str, radius: float) -> pd.Series:
    if metric == "diagonal_euclidean":
        return frame["diagonal_euclidean_score"] <= radius * radius
    if metric == "full_covariance":
        return frame["full_covariance_score"] <= radius * radius
    if metric == "coordinate_box":
        return frame["coordinate_box_score"] <= radius
    raise ValueError(metric)


def activity_table(frame: pd.DataFrame, core: pd.Series) -> tuple[list[int], int]:
    broad = (
        frame["sun_lon_deg"].between(120.0, 240.0, inclusive="both")
        & (frame["betgeo_deg"].abs() <= 35.0)
        & frame["vgeo_km_s"].between(15.0, 50.0, inclusive="both")
    )
    inside = frame["delta_sol_deg"].abs() <= base.ACTIVITY_HALF_WIDTH
    a = int((broad & inside & core).sum())
    b = int((broad & inside & ~core).sum())
    c = int((broad & ~inside & core).sum())
    d = int((broad & ~inside & ~core).sum())
    return [a, b, c, d], int(broad.sum())


def timestamp_set(frame: pd.DataFrame) -> set[str]:
    return {pd.Timestamp(value).strftime("%Y-%m-%d %H:%M:%S") for value in frame["event_second"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lookup", type=Path, default=base.LOOKUP_DEFAULT)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    lookup_bytes = args.lookup.read_bytes()
    lookup_rows = list(csv.DictReader(io.StringIO(lookup_bytes.decode("utf-8-sig"))))
    expected_by_year = {
        year: {lookup_time(row["Tobs"]) for row in lookup_rows if row["Tobs"].startswith(f"{year}-")}
        for year in base.YEARS
    }

    quality_frames: dict[int, pd.DataFrame] = {}
    sources: list[dict[str, Any]] = []
    for year in base.YEARS:
        raw, url = base.download_month(year)
        parsed = base.parse_month(raw)
        quality_frames[year] = quality_filter(parsed, year)
        sources.append({
            "year": year, "url": url, "bytes": len(raw), "sha256": base.sha256(raw),
            "parsed_rows": len(parsed), "quality_rows": len(quality_frames[year]),
        })
        print(json.dumps({"year": year, "parsed_rows": len(parsed), "quality_rows": len(quality_frames[year])}), flush=True)

    training, training_evidence = recover_training_rows(quality_frames[2026], lookup_rows)
    template = fit_template(training)
    training_scored = apply_template(training, template)
    template_summary = {
        key: value for key, value in template.items() if key != "training_residuals"
    }
    template_summary["training_members"] = len(training)
    template_summary["training_max_scores"] = {
        "diagonal_euclidean": float(training_scored["diagonal_euclidean_score"].max()),
        "full_covariance": float(training_scored["full_covariance_score"].max()),
        "coordinate_box": float(training_scored["coordinate_box_score"].max()),
    }

    results: list[dict[str, Any]] = []
    detail_rows: list[dict[str, Any]] = []
    for dedup_mode in DEDUP_MODES:
        prepared = {
            year: apply_template(deduplicate(frame, dedup_mode), template)
            for year, frame in quality_frames.items()
        }
        for metric in CORE_METRICS:
            for radius in RADII:
                annual: dict[int, dict[str, Any]] = {}
                selected_by_year: dict[int, pd.DataFrame] = {}
                for year, frame in prepared.items():
                    core = core_mask(frame, metric, radius)
                    selected = frame.loc[(frame["delta_sol_deg"].abs() <= base.ACTIVITY_HALF_WIDTH) & core].copy()
                    selected_by_year[year] = selected
                    table, broad_total = activity_table(frame, core)
                    annual[year] = {
                        "members": len(selected), "table": table, "broad_total": broad_total,
                        "activity_p": base.fisher_greater(*table),
                    }
                expected_all = set().union(*(expected_by_year[year] for year in range(2022, 2027)))
                actual_all = set().union(*(timestamp_set(selected_by_year[year]) for year in range(2022, 2027)))
                expected_untouched = expected_by_year[2022] | expected_by_year[2023]
                actual_untouched = timestamp_set(selected_by_year[2022]) | timestamp_set(selected_by_year[2023])
                pooled_table = [sum(annual[year]["table"][index] for year in (2022, 2023)) for index in range(4)]
                pooled_p = base.fisher_greater(*pooled_table)
                result = {
                    "dedup_mode": dedup_mode,
                    "core_metric": metric,
                    "radius_sigma": radius,
                    "annual": {str(year): annual[year] for year in base.YEARS},
                    "total_members_2019_2026": sum(annual[year]["members"] for year in base.YEARS),
                    "significant_year_members_2022_2026": len(actual_all),
                    "all_preserved_overlap": len(expected_all & actual_all),
                    "all_missing": sorted(expected_all - actual_all),
                    "all_additional": sorted(actual_all - expected_all),
                    "all_symmetric_difference": len(expected_all ^ actual_all),
                    "untouched_overlap": len(expected_untouched & actual_untouched),
                    "untouched_missing": sorted(expected_untouched - actual_untouched),
                    "untouched_additional": sorted(actual_untouched - expected_untouched),
                    "untouched_symmetric_difference": len(expected_untouched ^ actual_untouched),
                    "untouched_pooled_table": pooled_table,
                    "untouched_pooled_p": pooled_p,
                    "untouched_familywise_pass": pooled_p <= 0.05 / 12.0,
                }
                results.append(result)
                for year, selected in selected_by_year.items():
                    expected = expected_by_year[year]
                    for _, row in selected.iterrows():
                        timestamp = pd.Timestamp(row["event_second"]).strftime("%Y-%m-%d %H:%M:%S")
                        detail_rows.append({
                            "dedup_mode": dedup_mode, "core_metric": metric, "radius_sigma": radius,
                            "year": year, "timestamp": timestamp,
                            "identifier": str(row["unique_trajectory_identifier"]),
                            "in_preserved_lookup": timestamp in expected,
                            "diagonal_euclidean_score": float(row["diagonal_euclidean_score"]),
                            "full_covariance_score": float(row["full_covariance_score"]),
                            "coordinate_box_score": float(row["coordinate_box_score"]),
                            "medianfiterr_arcsec": float(row["medianfiterr_arcsec"]),
                            "num_stat": int(row["num_stat"]),
                        })

    ranked = sorted(
        results,
        key=lambda item: (
            item["untouched_symmetric_difference"], item["all_symmetric_difference"],
            abs(item["significant_year_members_2022_2026"] - 95),
            abs(item["total_members_2019_2026"] - 101),
            item["dedup_mode"], item["core_metric"], item["radius_sigma"],
        ),
    )
    generated_at = datetime.now(timezone.utc).isoformat()
    summary = {
        "generated_at_utc": generated_at,
        "purpose": "Complete ambiguity audit of a 2026-only chronological template; no best variant is promoted automatically.",
        "lookup": {"path": str(args.lookup), "rows": len(lookup_rows), "sha256": base.sha256(lookup_bytes)},
        "sources": sources,
        "training_reconnection": training_evidence,
        "fitted_2026_template": template_summary,
        "grid": {
            "dedup_modes": list(DEDUP_MODES), "core_metrics": list(CORE_METRICS),
            "radii_sigma": list(RADII), "cells": len(results),
        },
        "ranked_cells": ranked,
    }
    (args.output_dir / "template_ambiguity_audit.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    pd.DataFrame(detail_rows).to_csv(args.output_dir / "selected_event_grid.csv", index=False)
    pd.DataFrame([
        {
            "rank": index + 1,
            "dedup_mode": item["dedup_mode"], "core_metric": item["core_metric"],
            "radius_sigma": item["radius_sigma"],
            "untouched_symmetric_difference": item["untouched_symmetric_difference"],
            "all_symmetric_difference": item["all_symmetric_difference"],
            "untouched_pooled_p": item["untouched_pooled_p"],
            "total_members_2019_2026": item["total_members_2019_2026"],
            "significant_year_members_2022_2026": item["significant_year_members_2022_2026"],
        }
        for index, item in enumerate(ranked)
    ]).to_csv(args.output_dir / "ranked_grid_summary.csv", index=False)

    best = ranked[0]
    lines = [
        "# GhostStream 2026-frozen template ambiguity audit", "",
        f"Generated: `{generated_at}`", "",
        "This audit reports all 18 prespecified interpretations. Ranking is diagnostic and does not automatically redefine the primary analysis.", "",
        "## Reconstructed 2026-only template", "",
    ]
    for key in ("sun_lon", "latitude", "speed"):
        item = template_summary["parameters"][key]
        lines.append(
            f"- {key}: intercept `{item['intercept_at_epoch']:.9g}`, slope `{item['slope_per_solar_longitude_degree']:.9g}`, sigma `{item['sample_sigma']:.9g}`"
        )
    lines += ["", "## Closest grid cell", "",
        f"- Deduplication: `{best['dedup_mode']}`",
        f"- Core metric: `{best['core_metric']}`",
        f"- Radius: `{best['radius_sigma']}σ`",
        f"- Untouched 2022–2023 timestamp differences: **{best['untouched_symmetric_difference']}**",
        f"- All 2022–2026 timestamp differences: **{best['all_symmetric_difference']}**",
        f"- Selected 2022–2026: **{best['significant_year_members_2022_2026']}**",
        f"- Untouched pooled activity p: **{best['untouched_pooled_p']:.12g}**", "",
        "## Full grid", "",
        "| Rank | Dedup | Metric | Radius | Untouched differences | All differences | N 2022–2026 | Pooled p |",
        "|---:|---|---|---:|---:|---:|---:|---:|",
    ]
    for index, item in enumerate(ranked, 1):
        lines.append(
            f"| {index} | {item['dedup_mode']} | {item['core_metric']} | {item['radius_sigma']} | "
            f"{item['untouched_symmetric_difference']} | {item['all_symmetric_difference']} | "
            f"{item['significant_year_members_2022_2026']} | {item['untouched_pooled_p']:.6g} |"
        )
    lines += ["", "## Interpretation", "",
        "A close or exact cell would identify the likely historical implementation. A non-exact grid still provides a leakage-controlled chronological confirmation because the template was fitted only to preserved 2026 discovery members and evaluated separately on earlier years. Source-catalogue additions or label changes remain possible and must be distinguished from algorithmic differences.", ""]
    (args.output_dir / "TEMPLATE_AMBIGUITY_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({
        "grid_cells": len(results),
        "best": {
            "dedup_mode": best["dedup_mode"], "core_metric": best["core_metric"],
            "radius_sigma": best["radius_sigma"],
            "untouched_symmetric_difference": best["untouched_symmetric_difference"],
            "all_symmetric_difference": best["all_symmetric_difference"],
            "untouched_pooled_p": best["untouched_pooled_p"],
        },
        "output": str(args.output_dir),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
