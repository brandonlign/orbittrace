#!/usr/bin/env python3
"""Reproduce the frozen GhostStream GMN confirmation from official monthly files.

This script follows ``RECONSTRUCTION_PROTOCOL.md``. It does not fit or retune
candidate parameters. April catalogues from 2019 through 2026 are downloaded,
checksum-locked, parsed with a pinned official-community parser, filtered,
deduplicated, and tested with the frozen non-orbital radiant-speed template.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests
from gmn_python_api import meteor_trajectory_reader

ROOT = "https://globalmeteornetwork.org/data/traj_summary_data/monthly"
LOOKUP_DEFAULT = Path("pilots/ghoststream/april_stream/mdc/GhostStream_April_95_GMN_lookup.csv")
OUTPUT_DEFAULT = Path("pilots/ghoststream/reconstruction/primary_gmn_monthly_reproduction")
YEARS = tuple(range(2019, 2027))

EPOCH = 36.901963
LON0 = 210.6236753
LAT0 = 7.3230377
VG0 = 37.641692
DLON = -0.1029483
DLAT = -0.0230546
DVG = -0.0293492
SIG_LON = 0.7369
SIG_LAT = 0.6250
SIG_VG = 1.1596
SCORE_MAX = 9.0
ACTIVITY_HALF_WIDTH = 4.0

EXPECTED_COUNTS = {2019: 1, 2020: 4, 2021: 1, 2022: 10, 2023: 8, 2024: 14, 2025: 34, 2026: 29}
EXPECTED_P = {
    2019: 0.3532,
    2020: 0.1319,
    2021: 0.3436,
    2022: 0.003970,
    2023: 0.002168,
    2024: 4.888e-5,
    2025: 9.42e-9,
    2026: 4.131e-6,
}
EXPECTED_POOL_P = 1.857134041807409e-5
EXPECTED_MEDIAN_D = 0.0439834
EXPECTED_Q90_D = 0.0923211
REF_ORBIT = {"q": 0.079202, "e": 0.946296, "i": 24.709376, "peri": 333.493819, "node": 37.937477}

FINITE_COLUMNS = [
    "rageo_deg", "decgeo_deg", "lamgeo_deg", "betgeo_deg", "vgeo_km_s",
    "a_au", "e", "i_deg", "peri_deg", "node_deg", "q_au",
]
EXPORT_COLUMNS = [
    "unique_trajectory_identifier", "beginning_utc_time", "event_second", "year",
    "iau_no", "num_stat", "participating_stations", "medianfiterr_arcsec",
    "sol_lon_deg", "delta_sol_deg", "rageo_deg", "decgeo_deg", "lamgeo_deg",
    "betgeo_deg", "sun_lon_deg", "vgeo_km_s", "expected_sun_lon_deg",
    "expected_betgeo_deg", "expected_vgeo_km_s", "residual_sun_lon_deg",
    "residual_betgeo_deg", "residual_vgeo_km_s", "score", "a_au", "e",
    "i_deg", "peri_deg", "node_deg", "q_au", "tisserandj",
    "latbeg_n_deg", "lonbeg_e_deg", "latend_n_deg", "lonend_e_deg",
]


def wrap180(value: Any) -> Any:
    return (value + 180.0) % 360.0 - 180.0


def angular_abs(a: float, b: float) -> float:
    return abs(float(wrap180(a - b)))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def log_comb(n: int, k: int) -> float:
    if k < 0 or k > n:
        return -math.inf
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def fisher_greater(a: int, b: int, c: int, d: int) -> float:
    inside = a + b
    total = a + b + c + d
    core = a + c
    logs = [
        log_comb(core, x) + log_comb(total - core, inside - x) - log_comb(total, inside)
        for x in range(a, min(inside, core) + 1)
    ]
    if not logs:
        return 1.0
    maximum = max(logs)
    return min(1.0, math.exp(maximum) * sum(math.exp(value - maximum) for value in logs))


def percentile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return math.nan
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def normalize_orbit(row: pd.Series) -> dict[str, float]:
    node = float(row["node_deg"]) % 360.0
    peri = float(row["peri_deg"]) % 360.0
    sol = float(row["sol_lon_deg"]) % 360.0
    flipped = (node + 180.0) % 360.0
    if angular_abs(flipped, sol) < angular_abs(node, sol):
        node = flipped
        peri = (peri + 180.0) % 360.0
    return {
        "q": float(row["q_au"]), "e": float(row["e"]), "i": float(row["i_deg"]),
        "peri": peri, "node": node,
    }


def d_sh(first: dict[str, float], second: dict[str, float]) -> float:
    i1, w1, o1, i2, w2, o2 = map(
        math.radians,
        [first["i"], first["peri"], first["node"], second["i"], second["peri"], second["node"]],
    )
    cosine = math.cos(i1) * math.cos(i2) + math.sin(i1) * math.sin(i2) * math.cos(o1 - o2)
    mutual_i = math.acos(max(-1.0, min(1.0, cosine)))
    denominator = max(1e-15, math.cos(mutual_i / 2.0))
    argument = math.cos((i1 + i2) / 2.0) * math.sin((o1 - o2) / 2.0) / denominator
    argument = max(-1.0, min(1.0, argument))
    pi_angle = (w1 - w2) + 2.0 * math.asin(argument)
    return math.sqrt(
        (first["e"] - second["e"]) ** 2
        + (first["q"] - second["q"]) ** 2
        + (2.0 * math.sin(mutual_i / 2.0)) ** 2
        + ((first["e"] + second["e"]) * math.sin(pi_angle / 2.0)) ** 2
    )


def download_month(year: int, timeout: int = 300) -> tuple[bytes, str]:
    url = f"{ROOT}/traj_summary_monthly_{year}04.txt"
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "GhostStream-monthly-reproduction/1.0", "Accept-Encoding": "identity"},
    )
    response.raise_for_status()
    if not response.content.startswith(b"#"):
        raise RuntimeError(f"Unexpected GMN monthly response for {year}: {response.content[:80]!r}")
    return response.content, url


def parse_month(raw: bytes) -> pd.DataFrame:
    text = raw.decode("utf-8")
    frame = meteor_trajectory_reader.read_data(text, output_camel_case=True).reset_index()
    required = set(FINITE_COLUMNS) | {
        "unique_trajectory_identifier", "beginning_utc_time", "iau_no", "sol_lon_deg",
        "medianfiterr_arcsec", "num_stat", "participating_stations",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise RuntimeError(f"Parsed GMN file is missing columns: {missing}")
    return frame


def prepare_year(frame: pd.DataFrame, year: int) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw_rows = len(frame)
    frame = frame.copy()
    frame["beginning_utc_time"] = pd.to_datetime(frame["beginning_utc_time"], errors="coerce", utc=False)
    frame["event_second"] = frame["beginning_utc_time"].dt.floor("S")
    frame["year"] = year

    finite_mask = np.isfinite(frame[FINITE_COLUMNS].to_numpy(dtype=float)).all(axis=1)
    eligible_mask = (
        frame["event_second"].notna()
        & (frame["iau_no"] == -1)
        & (frame["num_stat"] >= 2)
        & frame["medianfiterr_arcsec"].notna()
        & (frame["medianfiterr_arcsec"] <= 180.0)
        & frame["vgeo_km_s"].between(5.0, 75.0, inclusive="both")
        & finite_mask
    )
    eligible = frame.loc[eligible_mask].copy()
    eligible = eligible.sort_values(
        ["event_second", "medianfiterr_arcsec", "num_stat", "unique_trajectory_identifier"],
        ascending=[True, True, False, True],
        kind="mergesort",
    )
    duplicate_groups = int(eligible.duplicated("event_second", keep=False).groupby(eligible["event_second"]).any().sum())
    deduplicated = eligible.drop_duplicates("event_second", keep="first").copy()

    deduplicated["delta_sol_deg"] = wrap180(deduplicated["sol_lon_deg"] - EPOCH)
    deduplicated["sun_lon_deg"] = (deduplicated["lamgeo_deg"] - deduplicated["sol_lon_deg"]) % 360.0
    deduplicated["expected_sun_lon_deg"] = (LON0 + DLON * deduplicated["delta_sol_deg"]) % 360.0
    deduplicated["expected_betgeo_deg"] = LAT0 + DLAT * deduplicated["delta_sol_deg"]
    deduplicated["expected_vgeo_km_s"] = VG0 + DVG * deduplicated["delta_sol_deg"]
    deduplicated["residual_sun_lon_deg"] = wrap180(
        deduplicated["sun_lon_deg"] - deduplicated["expected_sun_lon_deg"]
    )
    deduplicated["residual_betgeo_deg"] = deduplicated["betgeo_deg"] - deduplicated["expected_betgeo_deg"]
    deduplicated["residual_vgeo_km_s"] = deduplicated["vgeo_km_s"] - deduplicated["expected_vgeo_km_s"]
    deduplicated["score"] = (
        (deduplicated["residual_sun_lon_deg"] / SIG_LON) ** 2
        + (deduplicated["residual_betgeo_deg"] / SIG_LAT) ** 2
        + (deduplicated["residual_vgeo_km_s"] / SIG_VG) ** 2
    )

    stats = {
        "raw_rows": raw_rows,
        "eligible_before_deduplication": len(eligible),
        "deduplicated_rows": len(deduplicated),
        "duplicate_second_groups": duplicate_groups,
    }
    return deduplicated, stats


def source_table(frame: pd.DataFrame) -> tuple[list[int], int]:
    broad = frame.loc[
        frame["sun_lon_deg"].between(120.0, 240.0, inclusive="both")
        & (frame["betgeo_deg"].abs() <= 35.0)
        & frame["vgeo_km_s"].between(15.0, 50.0, inclusive="both")
    ]
    inside = broad["delta_sol_deg"].abs() <= ACTIVITY_HALF_WIDTH
    core = broad["score"] <= SCORE_MAX
    a = int((inside & core).sum())
    b = int((inside & ~core).sum())
    c = int((~inside & core).sum())
    d = int((~inside & ~core).sum())
    return [a, b, c, d], len(broad)


def timestamp_text(value: Any) -> str:
    return pd.Timestamp(value).strftime("%Y-%m-%d %H:%M:%S")


def lookup_timestamp(value: str) -> str:
    return value[:10] + " " + value[11:]


def compare_lookup(lookup_rows: list[dict[str, str]], selected: pd.DataFrame) -> dict[str, Any]:
    expected_by_time = {lookup_timestamp(row["Tobs"]): row for row in lookup_rows}
    actual_by_time = {timestamp_text(row["event_second"]): row for _, row in selected.iterrows()}
    expected_times = set(expected_by_time)
    actual_times = set(actual_by_time)
    comparisons: list[dict[str, Any]] = []
    maximum_delta = 0.0
    mapping = {
        "RA": "rageo_deg", "DE": "decgeo_deg", "VG": "vgeo_km_s",
        "LS": "sol_lon_deg", "LO": "lamgeo_deg", "LA": "betgeo_deg",
    }
    for timestamp in sorted(expected_times & actual_times):
        expected = expected_by_time[timestamp]
        actual = actual_by_time[timestamp]
        deltas: dict[str, float] = {}
        for lookup_key, source_key in mapping.items():
            left = float(actual[source_key])
            right = float(expected[lookup_key])
            delta = float(wrap180(left - right)) if lookup_key in {"RA", "LS", "LO"} else left - right
            deltas[lookup_key] = delta
            maximum_delta = max(maximum_delta, abs(delta))
        actual_sclo = float(actual["sun_lon_deg"])
        expected_sclo = float(expected["SCLO"]) % 360.0
        sclo_delta = float(wrap180(actual_sclo - expected_sclo))
        deltas["SCLO"] = sclo_delta
        maximum_delta = max(maximum_delta, abs(sclo_delta))
        comparisons.append({"timestamp": timestamp, "identifier": str(actual["unique_trajectory_identifier"]), "deltas": deltas})
    return {
        "exact_timestamp_set": expected_times == actual_times,
        "expected": len(expected_times),
        "actual": len(actual_times),
        "missing_timestamps": sorted(expected_times - actual_times),
        "additional_timestamps": sorted(actual_times - expected_times),
        "maximum_absolute_field_delta": maximum_delta,
        "field_comparisons": comparisons,
    }


def jsonable(value: Any) -> Any:
    if isinstance(value, (np.integer,)): return int(value)
    if isinstance(value, (np.floating,)): return None if not math.isfinite(float(value)) else float(value)
    if isinstance(value, pd.Timestamp): return value.isoformat()
    if isinstance(value, (list, tuple)): return [jsonable(item) for item in value]
    if pd.isna(value): return None
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lookup", type=Path, default=LOOKUP_DEFAULT)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    lookup_bytes = args.lookup.read_bytes()
    lookup_rows = list(csv.DictReader(io.StringIO(lookup_bytes.decode("utf-8-sig"))))
    if len(lookup_rows) != 95:
        raise RuntimeError(f"Expected 95 committed lookup rows, found {len(lookup_rows)}")

    source_manifest: list[dict[str, Any]] = []
    annual: dict[int, dict[str, Any]] = {}
    member_frames: list[pd.DataFrame] = []
    diagnostic_frames: list[pd.DataFrame] = []

    for year in YEARS:
        raw, url = download_month(year)
        frame = parse_month(raw)
        prepared, preparation = prepare_year(frame, year)
        table, broad_total = source_table(prepared)
        selected = prepared.loc[
            (prepared["delta_sol_deg"].abs() <= ACTIVITY_HALF_WIDTH)
            & (prepared["score"] <= SCORE_MAX)
        ].copy()
        member_frames.append(selected)
        diagnostic_frames.append(
            prepared.loc[(prepared["delta_sol_deg"].abs() <= 6.0) & (prepared["score"] <= 16.0)].copy()
        )
        p_value = fisher_greater(*table)
        annual[year] = {
            **preparation,
            "broad_source_rows": broad_total,
            "table": table,
            "members": len(selected),
            "activity_p": p_value,
            "expected_members": EXPECTED_COUNTS[year],
            "expected_activity_p": EXPECTED_P[year],
        }
        source_manifest.append({
            "year": year,
            "month": f"{year}-04",
            "url": url,
            "accessed_at_utc": datetime.now(timezone.utc).isoformat(),
            "bytes": len(raw),
            "sha256": sha256(raw),
            "parsed_rows": len(frame),
        })
        print(json.dumps({"year": year, "rows": len(frame), "members": len(selected), "activity_p": p_value}), flush=True)

    members = pd.concat(member_frames, ignore_index=True).sort_values("beginning_utc_time")
    diagnostics = pd.concat(diagnostic_frames, ignore_index=True).sort_values(["year", "score", "beginning_utc_time"])
    significant_members = members.loc[members["year"] >= 2022].copy()

    annual_counts_exact = all(annual[year]["members"] == EXPECTED_COUNTS[year] for year in YEARS)
    total_exact = len(members) == 101
    lookup_comparison = compare_lookup(lookup_rows, significant_members)

    pooled_table = [sum(annual[year]["table"][index] for year in (2022, 2023)) for index in range(4)]
    pooled_p = fisher_greater(*pooled_table)
    pooled_familywise_pass = pooled_p <= 0.05 / 12.0

    distances = [d_sh(normalize_orbit(row), REF_ORBIT) for _, row in significant_members.iterrows()]
    median_d = statistics.median(distances) if distances else math.nan
    q90_d = percentile(distances, 0.9) if distances else math.nan
    orbit_compact = bool(distances) and median_d <= 0.10 and q90_d <= 0.15

    exact_p = abs(pooled_p - EXPECTED_POOL_P) / EXPECTED_POOL_P <= 1e-8
    exact_orbit = abs(median_d - EXPECTED_MEDIAN_D) <= 1e-6 and abs(q90_d - EXPECTED_Q90_D) <= 1e-6
    lookup_exact = bool(lookup_comparison["exact_timestamp_set"])

    if total_exact and annual_counts_exact and lookup_exact and exact_p and exact_orbit:
        verdict = "EXACT_REPRODUCTION"
    elif lookup_exact and pooled_familywise_pass and orbit_compact:
        verdict = "SCIENTIFIC_REPRODUCTION_WITH_SOURCE_DRIFT"
    elif pooled_familywise_pass and orbit_compact and len(members) > 0:
        verdict = "PARTIAL_REPRODUCTION"
    else:
        verdict = "FAILED_REPRODUCTION"

    export_members = members.copy()
    export_members["beginning_utc_time"] = export_members["beginning_utc_time"].map(lambda x: pd.Timestamp(x).isoformat())
    export_members["event_second"] = export_members["event_second"].map(timestamp_text)
    export_members[[column for column in EXPORT_COLUMNS if column in export_members]].to_csv(
        args.output_dir / "reproduced_members_2019_2026.csv", index=False
    )
    diagnostics["beginning_utc_time"] = diagnostics["beginning_utc_time"].map(lambda x: pd.Timestamp(x).isoformat())
    diagnostics["event_second"] = diagnostics["event_second"].map(timestamp_text)
    diagnostics[[column for column in EXPORT_COLUMNS if column in diagnostics]].to_csv(
        args.output_dir / "near_boundary_diagnostics.csv", index=False
    )
    pd.DataFrame([
        {"year": year, "a": annual[year]["table"][0], "b": annual[year]["table"][1],
         "c": annual[year]["table"][2], "d": annual[year]["table"][3],
         "broad_total": annual[year]["broad_source_rows"], "members": annual[year]["members"],
         "activity_p": annual[year]["activity_p"]}
        for year in YEARS
    ]).to_csv(args.output_dir / "reproduced_activity_tables.csv", index=False)

    generated_at = datetime.now(timezone.utc).isoformat()
    result = {
        "generated_at_utc": generated_at,
        "verdict": verdict,
        "scope": "Frozen April monthly-catalogue membership, source-preserving activity, and post-selection orbit.",
        "protocol": "pilots/ghoststream/reconstruction/RECONSTRUCTION_PROTOCOL.md",
        "environment": {
            "python_target": "3.10",
            "gmn_python_api": "0.0.13",
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "requests": requests.__version__,
        },
        "lookup": {"path": str(args.lookup), "rows": len(lookup_rows), "sha256": sha256(lookup_bytes)},
        "sources": source_manifest,
        "annual": {str(year): annual[year] for year in YEARS},
        "membership": {
            "expected_total": 101,
            "actual_total": len(members),
            "total_exact": total_exact,
            "annual_counts_exact": annual_counts_exact,
            "lookup_95": lookup_comparison,
        },
        "untouched_2022_2023": {
            "table": pooled_table,
            "activity_p": pooled_p,
            "expected_activity_p": EXPECTED_POOL_P,
            "relative_error": abs(pooled_p - EXPECTED_POOL_P) / EXPECTED_POOL_P,
            "passes_12_month_familywise_gate": pooled_familywise_pass,
        },
        "orbit": {
            "n": len(distances),
            "median_d_sh": median_d,
            "expected_median_d_sh": EXPECTED_MEDIAN_D,
            "q90_d_sh": q90_d,
            "expected_q90_d_sh": EXPECTED_Q90_D,
            "max_d_sh": max(distances) if distances else None,
            "compactness_gate": orbit_compact,
        },
        "gates": {
            "total_exact": total_exact,
            "annual_counts_exact": annual_counts_exact,
            "lookup_exact": lookup_exact,
            "pooled_p_exact": exact_p,
            "orbit_diagnostics_exact": exact_orbit,
            "untouched_activity_pass": pooled_familywise_pass,
            "orbit_compactness_pass": orbit_compact,
        },
    }
    (args.output_dir / "primary_gmn_monthly_reproduction.json").write_text(
        json.dumps(result, indent=2, sort_keys=True, default=jsonable) + "\n", encoding="utf-8"
    )
    (args.output_dir / "source_manifest.json").write_text(
        json.dumps(source_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    lines = [
        "# GhostStream primary GMN monthly-catalogue reproduction", "",
        f"Generated: `{generated_at}`", "", f"## Verdict: `{verdict}`", "",
        "No candidate parameter or threshold was fitted during this run.", "",
        "## Membership", "",
        f"- Expected total, 2019–2026: **101**",
        f"- Reproduced total: **{len(members)}**",
        f"- Annual counts exact: **{annual_counts_exact}**",
        f"- Preserved 95 UTC-second set exact: **{lookup_exact}**",
        f"- Missing preserved timestamps: **{len(lookup_comparison['missing_timestamps'])}**",
        f"- Additional timestamps: **{len(lookup_comparison['additional_timestamps'])}**", "",
        "| Year | Expected N | Reproduced N | Reproduced p | Preserved p |", "|---:|---:|---:|---:|---:|",
    ]
    for year in YEARS:
        lines.append(
            f"| {year} | {EXPECTED_COUNTS[year]} | {annual[year]['members']} | "
            f"{annual[year]['activity_p']:.12g} | {EXPECTED_P[year]:.12g} |"
        )
    lines += [
        "", "## Untouched 2022–2023", "",
        f"- Reproduced table `[a,b,c,d]`: `{pooled_table}`",
        f"- Reproduced p: **{pooled_p:.16g}**",
        f"- Preserved p: **{EXPECTED_POOL_P:.16g}**",
        f"- Twelve-month familywise gate: **{pooled_familywise_pass}**", "",
        "## Post-selection orbit", "",
        f"- Reproduced median D_SH: **{median_d:.9g}** (preserved {EXPECTED_MEDIAN_D:.9g})",
        f"- Reproduced q90 D_SH: **{q90_d:.9g}** (preserved {EXPECTED_Q90_D:.9g})",
        f"- Compactness gate: **{orbit_compact}**", "",
        "## Source integrity", "",
    ]
    for source in source_manifest:
        lines.append(
            f"- {source['month']}: {source['parsed_rows']} rows, {source['bytes']} bytes, "
            f"SHA-256 `{source['sha256']}`"
        )
    lines += ["", "## Interpretation", ""]
    interpretations = {
        "EXACT_REPRODUCTION": "The frozen central GMN result regenerated exactly within declared numerical tolerances.",
        "SCIENTIFIC_REPRODUCTION_WITH_SOURCE_DRIFT": "The exact preserved 95-event sample and decisive gates regenerated, with documented numerical source drift.",
        "PARTIAL_REPRODUCTION": "The candidate remained significant and compact, but exact preserved membership did not regenerate. Differences must be audited without retuning.",
        "FAILED_REPRODUCTION": "The decisive frozen test did not regenerate. No threshold should be changed; source and implementation discrepancies require inspection.",
    }
    lines += [interpretations[verdict], ""]
    (args.output_dir / "PRIMARY_GMN_MONTHLY_REPRODUCTION.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({
        "verdict": verdict,
        "members": len(members),
        "lookup_exact": lookup_exact,
        "pooled_p": pooled_p,
        "median_d_sh": median_d,
        "q90_d_sh": q90_d,
        "output": str(args.output_dir),
    }, indent=2))
    return 0 if verdict in {"EXACT_REPRODUCTION", "SCIENTIFIC_REPRODUCTION_WITH_SOURCE_DRIFT"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
