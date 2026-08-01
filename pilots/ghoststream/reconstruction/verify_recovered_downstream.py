#!/usr/bin/env python3
"""Verify the recovered GhostStream downstream outputs against preserved evidence.

This verifier is intentionally separate from the recovered scientific scripts.
The scripts are run unchanged from immutable remotion-worker commit
39972b5fe0cf4d47092d3caa2b3ced12bedb065e. This file only checks their outputs,
assembles a checksum manifest, and fails closed on any discrepancy.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

SOURCE_COMMIT = "39972b5fe0cf4d47092d3caa2b3ced12bedb065e"
EXPECTED_ANNUAL = {2019: 1, 2020: 4, 2021: 1, 2022: 10, 2023: 8, 2024: 14, 2025: 34, 2026: 29}


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def close(name: str, actual: float, expected: float, *, atol: float = 0.0, rtol: float = 0.0) -> float:
    actual = float(actual)
    expected = float(expected)
    if not math.isclose(actual, expected, abs_tol=atol, rel_tol=rtol):
        raise AssertionError(f"{name}: expected {expected}, found {actual}")
    return actual


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("ghoststream_exact_downstream_evidence"))
    parser.add_argument(
        "--lookup",
        type=Path,
        default=Path("pilots/ghoststream/april_stream/mdc/GhostStream_April_95_GMN_lookup.csv"),
    )
    parser.add_argument("--environment", type=Path, default=Path("ghoststream_downstream_environment.txt"))
    parser.add_argument("--source-hashes", type=Path, default=Path("ghoststream_downstream_source_sha256.txt"))
    args = parser.parse_args()

    root = args.output_dir
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)

    checks: dict[str, Any] = {}

    # Exact primary membership is required before downstream evidence is accepted.
    members_path = Path("ghoststream_april_validation/april_candidate_members.csv")
    members = pd.read_csv(members_path)
    times = pd.to_datetime(members["beginning_utc_time"], errors="raise", utc=True)
    annual = Counter(int(year) for year in times.dt.year)
    if len(members) != 101:
        raise AssertionError(f"primary total: expected 101, found {len(members)}")
    if dict(sorted(annual.items())) != EXPECTED_ANNUAL:
        raise AssertionError(f"annual counts: expected {EXPECTED_ANNUAL}, found {dict(annual)}")
    with args.lookup.open(newline="", encoding="utf-8-sig") as handle:
        lookup = list(csv.DictReader(handle))
    lookup_seconds = {row["Tobs"][:10] + " " + row["Tobs"][11:] for row in lookup}
    recovered_seconds = set(times[times.dt.year >= 2022].dt.strftime("%Y-%m-%d %H:%M:%S"))
    if recovered_seconds != lookup_seconds:
        raise AssertionError(
            f"95-event lookup mismatch: missing={sorted(lookup_seconds-recovered_seconds)}, "
            f"additional={sorted(recovered_seconds-lookup_seconds)}"
        )
    checks["primary_membership"] = {
        "total": 101,
        "significant_year_members": 95,
        "annual_counts": {str(key): value for key, value in EXPECTED_ANNUAL.items()},
        "lookup_timestamp_set_exact": True,
    }

    # Source-preserving antihelion test and post-selection orbit null.
    source = load_json("ghoststream_april_source_null/april_source_preserving_null.json")
    assert source["verdict"] == "APRIL_STREAM_SURVIVES_SOURCE_PRESERVING_NULL"
    assert source["passed"] is True
    assert source["untouched_years"]["individually_confirmed"] == [2022, 2023]
    source_activity = close(
        "untouched pooled activity p",
        source["untouched_years"]["activity"]["p"],
        1.857e-5,
        rtol=0.01,
    )
    source_shift = close(
        "untouched shifted-window p",
        source["untouched_years"]["shifted_windows"]["empirical_p"],
        0.01754,
        atol=0.00002,
    )
    source_orbit = close(
        "untouched source/time orbit-null p",
        source["untouched_years"]["orbit"]["null_p"],
        0.0001,
        atol=1e-12,
    )
    checks["source_preserving_null"] = {
        "verdict": source["verdict"],
        "untouched_activity_p": source_activity,
        "untouched_shifted_window_p": source_shift,
        "untouched_orbit_null_p": source_orbit,
    }

    # Hierarchical year/night bootstrap.
    boot = load_json("ghoststream_april_bootstrap/bootstrap_uncertainty.json")
    assert boot["members"] == 95
    assert boot["unique_nights"] == 29
    assert boot["replicates_each"] == 20000
    interpretation = boot["interpretation"]
    assert interpretation["ra_drift_excludes_zero"] is True
    assert interpretation["dec_drift_excludes_zero"] is True
    assert interpretation["speed_drift_excludes_zero"] is False
    point = boot["point_estimate"]
    close("bootstrap solar longitude", point["solar_longitude_deg"], 37.150, atol=0.002)
    close("bootstrap RA", point["ra_deg"], 247.170, atol=0.002)
    close("bootstrap Dec", point["dec_deg"], -14.343, atol=0.002)
    close("bootstrap Vg", point["vg_km_s"], 37.618, atol=0.002)
    primary = boot["primary_year_night_bootstrap"]
    expected_intervals = {
        "dra_deg_per_deg": (0.672, 1.040),
        "ddec_deg_per_deg": (-0.248, -0.037),
        "dvg_km_s_per_deg": (-0.178, 0.221),
    }
    reproduced_intervals: dict[str, list[float]] = {}
    for key, (low, high) in expected_intervals.items():
        actual_low = close(f"{key} low", primary[key]["ci95_low"], low, atol=0.003)
        actual_high = close(f"{key} high", primary[key]["ci95_high"], high, atol=0.003)
        reproduced_intervals[key] = [actual_low, actual_high]
    checks["cluster_bootstrap"] = {
        "members": 95,
        "nights": 29,
        "replicates_each": 20000,
        "interpretation": interpretation,
        "ci95": reproduced_intervals,
    }

    # Corrected March-May exposure-normalized activity profile.
    activity = load_json("ghoststream_april_activity_v2/activity_profile.json")
    close("activity baseline rate", activity["baseline_rate_per_1000_background"], 1.604, atol=0.005)
    close("activity peak solar longitude", activity["peak_solar_longitude_deg"], 38.652, atol=0.002)
    assert activity["peak_stream_count"] == 15
    assert activity["peak_background_count"] == 1021
    close("activity peak rate", activity["peak_rate_per_1000_background"], 15.17, atol=0.03)
    assert activity["posterior_supported_interval_delta_deg"] == [-1.0, 3.0]
    close("activity odds ratio", activity["aggregate_odds_ratio"], 4.162, atol=0.005)
    close("activity aggregate p", activity["aggregate_p"], 6.51e-19, rtol=0.03)
    expected_year_activity = {
        "2022": (10, 1086, 6, 2239),
        "2023": (8, 1525, 3, 4064),
        "2024": (14, 2181, 15, 10410),
        "2025": (35, 5277, 15, 9267),
        "2026": (29, 4471, 25, 14366),
    }
    yearly_activity: dict[str, list[int]] = {}
    for year, expected in expected_year_activity.items():
        item = activity["yearly"][year]
        found = (
            item["stream_inside"],
            item["background_inside"],
            item["stream_baseline"],
            item["background_baseline"],
        )
        if found != expected:
            raise AssertionError(f"activity {year}: expected {expected}, found {found}")
        yearly_activity[year] = list(found)
    checks["activity_profile"] = {
        "peak_solar_longitude_deg": activity["peak_solar_longitude_deg"],
        "peak_counts": [15, 1021],
        "supported_solar_longitude_interval_deg": [35.902, 39.902],
        "aggregate_odds_ratio": activity["aggregate_odds_ratio"],
        "aggregate_p": activity["aggregate_p"],
        "yearly_counts": yearly_activity,
    }

    # Three disjoint geographic groups.
    geographic = load_json("ghoststream_geographic_splits/geographic_split_validation.json")
    assert geographic["verdict"] == "APRIL_STREAM_REPLICATES_ACROSS_THREE_DISJOINT_GMN_GEOGRAPHIC_GROUPS"
    assert geographic["passed"] is True
    expected_regions = {
        "Americas": (30, 0.04503),
        "Europe_WestAsia": (22, 0.03375),
        "Oceania_EastAsia_Africa": (44, 0.04795),
    }
    region_checks: dict[str, Any] = {}
    for region, (count, expected_median) in expected_regions.items():
        item = geographic["regions"][region]
        assert item["members"] == count
        assert item["passed"] is True
        median_d = close(
            f"{region} median D", item["orbit"]["observed"]["median_d"], expected_median, atol=0.0001
        )
        orbit_p = close(f"{region} orbit-null p", item["orbit"]["null_p"], 0.0001, atol=1e-12)
        region_checks[region] = {"members": count, "median_d": median_d, "orbit_null_p": orbit_p}
    max_cross = close(
        "maximum cross-region medoid D",
        geographic["maximum_cross_region_medoid_d"],
        0.04054,
        atol=0.0001,
    )
    checks["geographic_replication"] = {
        "verdict": geographic["verdict"],
        "regions": region_checks,
        "maximum_cross_region_medoid_d": max_cross,
    }

    # Frozen 81-cell specification curve.
    spec = load_json("ghoststream_april_specification_curve/specification_curve.json")
    assert spec["verdict"] == "APRIL_STREAM_ROBUST_ACROSS_FROZEN_SPECIFICATION_GRID"
    assert spec["passed"] is True
    assert spec["grid"]["total_cells"] == 81
    assert spec["eligible_cells"] == 81
    assert spec["passing_cells"] == 81
    close("specification pass fraction", spec["pass_fraction"], 1.0, atol=1e-12)
    close("specification positive odds", spec["positive_odds_fraction"], 1.0, atol=1e-12)
    assert spec["member_count_range_eligible"] == [29, 129]
    min_median = close(
        "specification minimum median D", spec["orbit_median_d_range_eligible"][0], 0.03640, atol=0.0001
    )
    max_median = close(
        "specification maximum median D", spec["orbit_median_d_range_eligible"][1], 0.05548, atol=0.0001
    )
    worst_p = close(
        "specification worst activity p",
        spec["activity_p_quantiles_eligible"]["1.0"],
        8.55e-7,
        rtol=0.05,
    )
    checks["specification_curve"] = {
        "verdict": spec["verdict"],
        "eligible_cells": 81,
        "passing_cells": 81,
        "member_count_range": [29, 129],
        "orbit_median_d_range": [min_median, max_median],
        "worst_activity_p": worst_p,
    }

    source_dirs = {
        "primary": Path("ghoststream_april_validation"),
        "source_null": Path("ghoststream_april_source_null"),
        "bootstrap": Path("ghoststream_april_bootstrap"),
        "activity": Path("ghoststream_april_activity_v2"),
        "geographic": Path("ghoststream_geographic_splits"),
        "specification": Path("ghoststream_april_specification_curve"),
    }
    for name, source_dir in source_dirs.items():
        if not source_dir.is_dir():
            raise RuntimeError(f"Missing regenerated output directory: {source_dir}")
        shutil.copytree(source_dir, root / name)
    shutil.copy2(args.environment, root / "environment.txt")
    shutil.copy2(args.source_hashes, root / "source_sha256.txt")

    files = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        files.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    manifest = {
        "status": "EXACT_RECOVERED_DOWNSTREAM_REPRODUCTION",
        "source_repository": "brandonlign/remotion-worker",
        "source_commit": SOURCE_COMMIT,
        "python": "3.9",
        "checks": checks,
        "files": files,
    }
    (root / "downstream_reproduction.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    lines = [
        "# GhostStream recovered downstream reproduction",
        "",
        "**Verdict:** `EXACT_RECOVERED_DOWNSTREAM_REPRODUCTION`",
        "",
        f"The recovered source was run unchanged from immutable commit `{SOURCE_COMMIT}`. All checked internal-GMN downstream outputs matched the preserved evidence boundary.",
        "",
        "- Primary membership: 101 total; exact 95-event 2022–2026 lookup",
        f"- Untouched pooled activity p: {source_activity:.8g}",
        f"- Untouched shifted-window p: {source_shift:.8g}",
        f"- Untouched source/time orbit-null p: {source_orbit:.8g}",
        "- Bootstrap: 95 members, 29 nights, 20,000 replicates; RA/Dec drift resolved, speed drift unresolved",
        f"- Activity core: 35.902°–39.902° solar longitude; aggregate p={activity['aggregate_p']:.8g}",
        f"- Geographic replication: 30 / 22 / 44 members; maximum medoid D={max_cross:.6f}",
        "- Specification curve: 81/81 eligible cells passed",
        "",
        "This resolves the internal GMN downstream reproducibility gap. External archive and parent-body stages remain separate claim-boundary checks.",
        "",
    ]
    (root / "DOWNSTREAM_REPRODUCTION.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(checks, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
