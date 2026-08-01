#!/usr/bin/env python3
"""Apply the frozen GhostStream-April template to linked EDMOND v6.01 ZIPs.

The missing 2024 attachment is not replaced or inferred. This script evaluates
only annual ZIP files that the current public EDMOND page actually links and
that independently pass ZIP CRC and schema checks. No candidate parameter,
width, activity interval, or threshold is fitted from EDMOND.

Selection frozen from ``candidate_solution.json``:
  * epoch solar longitude: 36.901963 deg
  * Sun-centered ecliptic longitude: -149.3763247 deg
  * ecliptic latitude: +7.3230377 deg
  * geocentric speed: 37.641692 km/s
  * angular drifts: -0.1029483 and -0.0230546 deg/deg
  * external speed drift: exactly zero
  * residual sigmas: 0.7369 deg, 0.6250 deg, 1.1596 km/s
  * 3-sigma ellipsoid: standardized squared score <= 9
  * activity half-width: 4 deg

The activity test is the frozen one-sided Fisher/hypergeometric enrichment of
the narrow radiant-speed core inside versus outside the activity interval,
within the expanded antihelion source. Orbit is inspected only after selection.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import random
import statistics
import sys
import urllib.error
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = "https://meteornews.net/assets/2025-03-29-edmond-database"
YEARS = tuple(range(2001, 2025))
USER_AGENT = "GhostStream-frozen-EDMOND-evaluator/1.0"
MAX_BYTES = 100 * 1024 * 1024

EPOCH = 36.901963
LON0 = -149.3763247
LAT0 = 7.3230377
VG0 = 37.641692
DLON = -0.1029483
DLAT = -0.0230546
DVG = 0.0
SIG_LON = 0.7369
SIG_LAT = 0.6250
SIG_VG = 1.1596
SCORE_MAX = 9.0
ACTIVITY_HALF_WIDTH = 4.0

REF_ORBIT = {
    "q": 0.079202,
    "e": 0.946296,
    "i": 24.709376,
    "peri": 333.493819,
    "node": 37.937477,
}

SHOBER_TIMES = {
    "_20140429_213504",
    "_20160425_025942",
    "_20160428_020032",
    "_20170425_235432",
    "_20170426_024406",
    "_20220428_215139",
}

REQUIRED = {
    "_localtime",
    "_sol",
    "_elng",
    "_elat",
    "_vg",
    "_q",
    "_e",
    "_incl",
    "_peri",
    "_node",
}
QUALITY = {"_QA", "_Qc", "_dGP", "_Nts", "_Nos"}


@dataclass
class Meteor:
    year: int
    localtime: str
    sol: float
    sun_lon: float
    elat: float
    vg: float
    score: float
    q: float
    e: float
    incl: float
    peri: float
    node: float
    orbit_d_sh: float
    qa: float
    qc: float
    dgp: float
    nts: float
    nos: float


def request(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/zip,*/*;q=0.8",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        length = response.headers.get("Content-Length")
        if length is not None and int(length) > MAX_BYTES:
            raise ValueError(f"declared size {length} exceeds {MAX_BYTES}")
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError(f"body exceeds {MAX_BYTES}")
        return data


def finite(value: str | None, default: float = math.nan) -> float:
    try:
        result = float(value) if value is not None else default
    except (TypeError, ValueError):
        return default
    return result if math.isfinite(result) else default


def wrap180(value: float) -> float:
    return (value + 180.0) % 360.0 - 180.0


def angular_abs(a: float, b: float) -> float:
    return abs(wrap180(a - b))


def percentile(values: Iterable[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return math.nan
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * p
    lo = int(math.floor(position))
    hi = int(math.ceil(position))
    if lo == hi:
        return ordered[lo]
    weight = position - lo
    return ordered[lo] * (1.0 - weight) + ordered[hi] * weight


def normalize_node_peri(node: float, peri: float, sol: float) -> tuple[float, float]:
    direct = angular_abs(node, sol)
    flipped_node = (node + 180.0) % 360.0
    if angular_abs(flipped_node, sol) < direct:
        return flipped_node, (peri + 180.0) % 360.0
    return node % 360.0, peri % 360.0


def d_sh(q: float, e: float, incl: float, peri: float, node: float) -> float:
    """Standard Southworth-Hawkins orbital dissimilarity."""
    q2 = REF_ORBIT["q"]
    e2 = REF_ORBIT["e"]
    i1, w1, o1, i2, w2, o2 = map(
        math.radians,
        [incl, peri, node, REF_ORBIT["i"], REF_ORBIT["peri"], REF_ORBIT["node"]],
    )
    cos_i = (
        math.cos(i1) * math.cos(i2)
        + math.sin(i1) * math.sin(i2) * math.cos(o1 - o2)
    )
    mutual_i = math.acos(max(-1.0, min(1.0, cos_i)))
    denom = max(1e-15, math.cos(mutual_i / 2.0))
    asin_arg = (
        math.cos((i1 + i2) / 2.0)
        * math.sin((o1 - o2) / 2.0)
        / denom
    )
    asin_arg = max(-1.0, min(1.0, asin_arg))
    pi_angle = (w1 - w2) + 2.0 * math.asin(asin_arg)
    return math.sqrt(
        (e - e2) ** 2
        + (q - q2) ** 2
        + (2.0 * math.sin(mutual_i / 2.0)) ** 2
        + ((e + e2) * math.sin(pi_angle / 2.0)) ** 2
    )


def quality_rank(row: dict[str, str], row_index: int) -> tuple[float, ...]:
    qa = finite(row.get("_QA"), -math.inf)
    qc = finite(row.get("_Qc"), -math.inf)
    dgp = finite(row.get("_dGP"), math.inf)
    nts = finite(row.get("_Nts"), -math.inf)
    nos = finite(row.get("_Nos"), -math.inf)
    # Higher is better. No candidate coordinate enters duplicate resolution.
    return (qa, qc, -dgp, nts, nos, -float(row_index))


def parse_archive(year: int, data: bytes) -> dict[str, Any]:
    if not data.startswith(b"PK"):
        raise ValueError("missing ZIP signature")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise ValueError(f"CRC failure in {bad}")
        csv_members = [
            item for item in archive.infolist()
            if not item.is_dir() and item.filename.lower().endswith(".csv")
        ]
        if len(csv_members) != 1:
            raise ValueError(f"expected one CSV member, found {len(csv_members)}")
        member = csv_members[0]
        raw = archive.read(member)

    text = raw.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise ValueError("CSV has no header")
    columns = set(reader.fieldnames)
    missing = sorted(REQUIRED - columns)
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    best: dict[str, tuple[tuple[float, ...], int, dict[str, str]]] = {}
    raw_rows = 0
    valid_rows = 0
    for index, row in enumerate(reader):
        raw_rows += 1
        localtime = (row.get("_localtime") or "").strip()
        if not localtime:
            continue
        values = [
            finite(row.get(name))
            for name in ("_sol", "_elng", "_elat", "_vg", "_q", "_e", "_incl", "_peri", "_node")
        ]
        if not all(math.isfinite(value) for value in values):
            continue
        valid_rows += 1
        rank = quality_rank(row, index)
        previous = best.get(localtime)
        if previous is None or rank > previous[0]:
            best[localtime] = (rank, index, row)

    meteors: list[Meteor] = []
    broad_points: list[tuple[float, bool, float]] = []
    for localtime, (_, _, row) in best.items():
        sol = finite(row.get("_sol")) % 360.0
        elng = finite(row.get("_elng")) % 360.0
        elat = finite(row.get("_elat"))
        vg = finite(row.get("_vg"))
        sun_lon = wrap180(elng - sol)
        delta_sol = wrap180(sol - EPOCH)
        expected_lon = wrap180(LON0 + DLON * delta_sol)
        expected_lat = LAT0 + DLAT * delta_sol
        expected_vg = VG0 + DVG * delta_sol
        score = (
            (wrap180(sun_lon - expected_lon) / SIG_LON) ** 2
            + ((elat - expected_lat) / SIG_LAT) ** 2
            + ((vg - expected_vg) / SIG_VG) ** 2
        )

        q = finite(row.get("_q"))
        e = finite(row.get("_e"))
        incl = finite(row.get("_incl"))
        peri = finite(row.get("_peri"))
        node = finite(row.get("_node"))
        node, peri = normalize_node_peri(node, peri, sol)
        orbit_d = d_sh(q, e, incl, peri, node)

        broad = 120.0 <= (sun_lon % 360.0) <= 240.0 and abs(elat) <= 35.0 and 15.0 <= vg <= 50.0
        in_activity = angular_abs(sol, EPOCH) <= ACTIVITY_HALF_WIDTH
        in_core = score <= SCORE_MAX
        if broad:
            broad_points.append((sol, in_core, orbit_d))
        if broad and in_activity and in_core:
            meteors.append(
                Meteor(
                    year=year,
                    localtime=localtime,
                    sol=sol,
                    sun_lon=sun_lon,
                    elat=elat,
                    vg=vg,
                    score=score,
                    q=q,
                    e=e,
                    incl=incl,
                    peri=peri,
                    node=node,
                    orbit_d_sh=orbit_d,
                    qa=finite(row.get("_QA")),
                    qc=finite(row.get("_Qc")),
                    dgp=finite(row.get("_dGP")),
                    nts=finite(row.get("_Nts")),
                    nos=finite(row.get("_Nos")),
                )
            )

    inside_total = sum(
        angular_abs(sol, EPOCH) <= ACTIVITY_HALF_WIDTH
        for sol, _, _ in broad_points
    )
    inside_core = sum(
        angular_abs(sol, EPOCH) <= ACTIVITY_HALF_WIDTH and core
        for sol, core, _ in broad_points
    )
    outside_total = len(broad_points) - inside_total
    outside_core = sum(
        angular_abs(sol, EPOCH) > ACTIVITY_HALF_WIDTH and core
        for sol, core, _ in broad_points
    )

    return {
        "year": year,
        "url": f"{ROOT}/U2_{year}_EDM.zip",
        "zip_bytes": len(data),
        "zip_sha256": hashlib.sha256(data).hexdigest(),
        "csv_member": member.filename,
        "csv_columns": len(reader.fieldnames),
        "raw_rows": raw_rows,
        "valid_rows": valid_rows,
        "deduplicated_rows": len(best),
        "broad_source_rows": len(broad_points),
        "inside_total": inside_total,
        "inside_core": inside_core,
        "outside_total": outside_total,
        "outside_core": outside_core,
        "members": meteors,
        "broad_points": broad_points,
    }


def fetch_year(year: int) -> dict[str, Any]:
    url = f"{ROOT}/U2_{year}_EDM.zip"
    try:
        data = request(url)
        result = parse_archive(year, data)
        result["status"] = "VALIDATED"
        return result
    except urllib.error.HTTPError as exc:
        return {
            "year": year,
            "url": url,
            "status": "HTTP_ERROR",
            "http_status": exc.code,
            "error": str(exc),
            "members": [],
            "broad_points": [],
        }
    except Exception as exc:
        return {
            "year": year,
            "url": url,
            "status": "ERROR",
            "error": f"{type(exc).__name__}: {exc}",
            "members": [],
            "broad_points": [],
        }


def log_comb(n: int, k: int) -> float:
    if k < 0 or k > n:
        return -math.inf
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def fisher_greater(a: int, b: int, c: int, d: int) -> float:
    """One-sided Fisher exact p for enrichment in the first row."""
    n_inside = a + b
    n_total = a + b + c + d
    total_core = a + c
    hi = min(n_inside, total_core)
    logs = [
        log_comb(total_core, x)
        + log_comb(n_total - total_core, n_inside - x)
        - log_comb(n_total, n_inside)
        for x in range(a, hi + 1)
    ]
    if not logs:
        return 1.0
    maximum = max(logs)
    return min(1.0, math.exp(maximum) * sum(math.exp(value - maximum) for value in logs))


def odds_ratio(a: int, b: int, c: int, d: int) -> float:
    return ((a + 0.5) * (d + 0.5)) / ((b + 0.5) * (c + 0.5))


def shifted_window_test(points: list[tuple[float, bool, float]]) -> dict[str, Any]:
    def table(center: float) -> tuple[int, int, int, int]:
        inside_total = sum(angular_abs(sol, center) <= ACTIVITY_HALF_WIDTH for sol, _, _ in points)
        inside_core = sum(
            angular_abs(sol, center) <= ACTIVITY_HALF_WIDTH and core
            for sol, core, _ in points
        )
        outside_total = len(points) - inside_total
        outside_core = sum(
            angular_abs(sol, center) > ACTIVITY_HALF_WIDTH and core
            for sol, core, _ in points
        )
        return (
            inside_core,
            inside_total - inside_core,
            outside_core,
            outside_total - outside_core,
        )

    observed_table = table(EPOCH)
    observed_or = odds_ratio(*observed_table)
    shifted: list[dict[str, Any]] = []
    exceed = 0
    for index in range(1, 49):
        center = (EPOCH + index * 360.0 / 49.0) % 360.0
        counts = table(center)
        value = odds_ratio(*counts)
        if value >= observed_or:
            exceed += 1
        shifted.append(
            {
                "index": index,
                "center_solar_longitude_deg": center,
                "table": counts,
                "odds_ratio": value,
            }
        )
    return {
        "observed_table": observed_table,
        "observed_odds_ratio": observed_or,
        "shifted_positions": shifted,
        "shifted_exceedances": exceed,
        "empirical_p_plus_one": (exceed + 1) / 49.0,
        "note": "48 equally spaced frozen-geometry comparison windows; reported as a reproducible supplemental localization audit.",
    }


def orbit_null(selected: list[Meteor], points: list[tuple[float, bool, float]]) -> dict[str, Any]:
    if not selected:
        return {"status": "NOT_RUN_NO_MEMBERS"}
    pool = [
        orbit_d
        for sol, core, orbit_d in points
        if angular_abs(sol, EPOCH) <= ACTIVITY_HALF_WIDTH and not core and math.isfinite(orbit_d)
    ]
    n = len(selected)
    if len(pool) < n:
        return {"status": "NOT_RUN_INSUFFICIENT_NULL_POOL", "pool": len(pool), "n": n}
    observed = [item.orbit_d_sh for item in selected]
    observed_median = statistics.median(observed)
    observed_q90 = percentile(observed, 0.9)
    rng = random.Random(20260731)
    trials = 20_000
    passes = 0
    for _ in range(trials):
        sample = rng.sample(pool, n)
        if statistics.median(sample) <= observed_median and percentile(sample, 0.9) <= observed_q90:
            passes += 1
    return {
        "status": "COMPLETED",
        "metric": "standard Southworth-Hawkins D_SH",
        "null_pool": len(pool),
        "sample_size": n,
        "trials": trials,
        "passes_as_or_more_compact": passes,
        "p_plus_one": (passes + 1) / (trials + 1),
        "observed_median": observed_median,
        "observed_q90": observed_q90,
        "observed_max": max(observed),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(fetch_year, year): year for year in YEARS}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                json.dumps(
                    {
                        "year": result["year"],
                        "status": result["status"],
                        "rows": result.get("deduplicated_rows"),
                        "members": len(result.get("members", [])),
                        "error": result.get("error"),
                    }
                ),
                flush=True,
            )
    results.sort(key=lambda item: item["year"])

    validated = [item for item in results if item["status"] == "VALIDATED"]
    selected = [member for item in validated for member in item["members"]]
    points = [point for item in validated for point in item["broad_points"]]

    a = sum(item["inside_core"] for item in validated)
    b = sum(item["inside_total"] - item["inside_core"] for item in validated)
    c = sum(item["outside_core"] for item in validated)
    d = sum(item["outside_total"] - item["outside_core"] for item in validated)
    activity_p = fisher_greater(a, b, c, d) if validated else math.nan
    activity_or = odds_ratio(a, b, c, d) if validated else math.nan
    shifted = shifted_window_test(points) if points else {"status": "NOT_RUN"}
    orbit = orbit_null(selected, points)

    member_rows = []
    for item in sorted(selected, key=lambda row: (row.year, row.localtime)):
        member_rows.append(
            {
                **item.__dict__,
                "overlaps_shober_selected_event": item.localtime in SHOBER_TIMES,
            }
        )

    year_summaries = []
    for item in results:
        summary = {key: value for key, value in item.items() if key not in {"members", "broad_points"}}
        summary["candidate_members"] = len(item.get("members", []))
        summary["candidate_member_times"] = [member.localtime for member in item.get("members", [])]
        year_summaries.append(summary)

    n_members = len(member_rows)
    n_new_vs_shober = sum(not row["overlaps_shober_selected_event"] for row in member_rows)
    activity_membership_gate = n_members >= 8 and activity_p <= 0.01
    if not validated:
        verdict = "NO_USABLE_LINKED_ARCHIVES"
    elif activity_membership_gate and orbit.get("status") == "COMPLETED" and orbit.get("p_plus_one", 1.0) <= 0.01:
        verdict = "LINKED_EDMOND_ARCHIVES_PASS_FROZEN_ACTIVITY_AND_ORBIT_CHECKS"
    elif n_members:
        verdict = "LINKED_EDMOND_ARCHIVES_PROVIDE_SUPPORT_BUT_NOT_FULL_FROZEN_PASS"
    else:
        verdict = "CLEAN_SCIENTIFIC_NEGATIVE_IN_USABLE_LINKED_ARCHIVES"

    report = {
        "audit": "frozen_GhostStream_template_on_currently_linked_EDMOND_v6.01_annual_ZIPs",
        "verdict": verdict,
        "claim_boundary": (
            "The missing 2024 ZIP is not represented. EDMOND is a compiled archive and may overlap upstream networks. "
            "This run is a frozen-template robustness check, not a clean third-instrument replication."
        ),
        "frozen_parameters": {
            "epoch_solar_longitude_deg": EPOCH,
            "sun_centered_ecliptic_longitude_deg": LON0,
            "ecliptic_latitude_deg": LAT0,
            "geocentric_speed_km_s": VG0,
            "drift_per_solar_longitude_deg": {"sun_lon": DLON, "elat": DLAT, "vg": DVG},
            "sigmas": {"sun_lon_deg": SIG_LON, "elat_deg": SIG_LAT, "vg_km_s": SIG_VG},
            "score_max": SCORE_MAX,
            "activity_half_width_deg": ACTIVITY_HALF_WIDTH,
            "expanded_antihelion": {"sun_lon_0_360_deg": [120.0, 240.0], "abs_elat_max_deg": 35.0, "vg_km_s": [15.0, 50.0]},
        },
        "archive_acquisition": {
            "years_requested": list(YEARS),
            "years_validated": [item["year"] for item in validated],
            "years_unavailable_or_invalid": [
                {"year": item["year"], "status": item["status"], "http_status": item.get("http_status"), "error": item.get("error")}
                for item in results if item["status"] != "VALIDATED"
            ],
            "total_raw_rows": sum(item["raw_rows"] for item in validated),
            "total_deduplicated_rows": sum(item["deduplicated_rows"] for item in validated),
            "per_year": year_summaries,
        },
        "frozen_activity_test": {
            "table": {"inside_core": a, "inside_noncore": b, "outside_core": c, "outside_noncore": d},
            "one_sided_fisher_p": activity_p,
            "odds_ratio_haldane_anscombe": activity_or,
            "selected_members": n_members,
            "preexisting_standalone_rules": {"minimum_members": 8, "maximum_activity_p": 0.01},
            "activity_membership_gate_passed": activity_membership_gate,
        },
        "shifted_window_audit": shifted,
        "post_selection_orbit_check": orbit,
        "members": member_rows,
        "overlap_audit": {
            "selected_members": n_members,
            "exact_UTC_overlaps_with_six_Shober_EDMOND_members": n_members - n_new_vs_shober,
            "selected_events_not_in_prior_six_member_table": n_new_vs_shober,
        },
    }

    json_path = args.output_dir / "linked_v601_frozen_evaluation.json"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")

    csv_path = args.output_dir / "linked_v601_candidate_members.csv"
    fields = list(member_rows[0].keys()) if member_rows else [
        "year", "localtime", "sol", "sun_lon", "elat", "vg", "score", "q", "e", "incl", "peri", "node", "orbit_d_sh", "overlaps_shober_selected_event"
    ]
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(member_rows)

    print(
        json.dumps(
            {
                "verdict": verdict,
                "validated_years": [item["year"] for item in validated],
                "unavailable_years": [item["year"] for item in results if item["status"] != "VALIDATED"],
                "selected_members": n_members,
                "new_vs_prior_Shober_six": n_new_vs_shober,
                "activity_p": activity_p,
                "activity_odds_ratio": activity_or,
                "shifted_window_p": shifted.get("empirical_p_plus_one"),
                "orbit_null_p": orbit.get("p_plus_one"),
                "report": str(json_path),
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
