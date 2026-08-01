#!/usr/bin/env python3
"""Apply the frozen GhostStream April template to the latest usable full EDMOND archives.

The advertised 2024 annual ZIP is currently unavailable. This script therefore
runs the unchanged external-validation template on the latest live full annual
v6.01 files (2022 and 2023). It does not fit or tune any parameter.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import statistics
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Iterable

ARCHIVES = {
    2022: "https://meteornews.net/assets/2025-03-29-edmond-database/U2_2022_EDM.zip",
    2023: "https://meteornews.net/assets/2025-03-29-edmond-database/U2_2023_EDM.zip",
}
USER_AGENT = "GhostStream-frozen-EDMOND-validation/1.0 (+https://github.com/brandonlign/isef)"
MAX_BYTES = 100 * 1024 * 1024

# Frozen candidate solution. These values are copied from candidate_solution.json.
EPOCH = 36.901963
CENTER_LSC = -149.3763247
CENTER_BETA = 7.3230377
CENTER_VG = 37.641692
DRIFT_LSC = -0.1029483
DRIFT_BETA = -0.0230546
DRIFT_VG = 0.0  # frozen uniform external-validation rule
SIGMA_LSC = 0.7369
SIGMA_BETA = 0.6250
SIGMA_VG = 1.1596
CORE_SCORE_MAX = 9.0  # unchanged 3-sigma ellipsoid
ACTIVITY_HALF_WIDTH = 4.0

GMN_ORBIT = {
    "q": 0.079202,
    "e": 0.946296,
    "incl": 24.709376,
    "peri": 333.493819,
    "node": 37.937477,
}

REQUIRED = {
    "_localtime", "_sol", "_elng", "_elat", "_vg",
    "_q", "_e", "_incl", "_peri", "_node",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/zip,*/*",
        "Accept-Encoding": "identity",
    })
    with urllib.request.urlopen(req, timeout=90) as response:
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_BYTES:
            raise ValueError(f"archive too large: {length}")
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("archive exceeded byte cap")
    if not data.startswith(b"PK"):
        raise ValueError("missing ZIP signature")
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        bad = zf.testzip()
        if bad:
            raise ValueError(f"ZIP CRC failure: {bad}")
    return data


def wrap180(x: float) -> float:
    return (x + 180.0) % 360.0 - 180.0


def wrap360(x: float) -> float:
    return x % 360.0


def finite(row: dict[str, str], key: str) -> float | None:
    try:
        value = float(row[key])
    except (KeyError, TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def quality_key(row: dict[str, str], original_index: int) -> tuple[float, float, float, int]:
    # Quality-only deduplication: no candidate residual or orbit enters this key.
    ddeg = finite(row, "_ddeg")
    cdeg = finite(row, "_cdeg")
    nos = finite(row, "_Nos")
    return (
        ddeg if ddeg is not None and ddeg >= 0 else math.inf,
        cdeg if cdeg is not None and cdeg >= 0 else math.inf,
        -(nos if nos is not None else -math.inf),
        original_index,
    )


def parse_archive(data: bytes, year: int) -> tuple[list[dict[str, object]], dict[str, object]]:
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        csv_members = [x for x in zf.infolist() if not x.is_dir() and x.filename.lower().endswith(".csv")]
        if len(csv_members) != 1:
            raise ValueError(f"expected one CSV, found {[x.filename for x in csv_members]}")
        member = csv_members[0]
        raw = zf.read(member)
    text = raw.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None or not REQUIRED.issubset(reader.fieldnames):
        missing = sorted(REQUIRED - set(reader.fieldnames or []))
        raise ValueError(f"missing required fields: {missing}")

    raw_rows = 0
    valid_rows: list[tuple[int, dict[str, object], dict[str, str]]] = []
    invalid_rows = 0
    for idx, row in enumerate(reader):
        raw_rows += 1
        sol = finite(row, "_sol")
        elng = finite(row, "_elng")
        beta = finite(row, "_elat")
        vg = finite(row, "_vg")
        q = finite(row, "_q")
        e = finite(row, "_e")
        incl = finite(row, "_incl")
        peri = finite(row, "_peri")
        node = finite(row, "_node")
        localtime = (row.get("_localtime") or "").strip()
        if None in (sol, elng, beta, vg, q, e, incl, peri, node) or not localtime:
            invalid_rows += 1
            continue
        if not (0 <= sol < 360 and -90 <= beta <= 90 and 0 < vg < 100 and q > 0 and e >= 0):
            invalid_rows += 1
            continue
        lsc_signed = wrap180(elng - sol)
        normalized = {
            "year": year,
            "localtime": localtime,
            "sol": sol,
            "sun_centered_longitude_deg": lsc_signed,
            "sun_centered_longitude_360_deg": wrap360(lsc_signed),
            "beta": beta,
            "vg": vg,
            "q": q,
            "e": e,
            "incl": incl,
            "peri": wrap360(peri),
            "node": wrap360(node),
            "stream_label": (row.get("_stream") or "").strip(),
            "id1": (row.get("_ID1") or "").strip(),
            "id2": (row.get("_ID2") or "").strip(),
            "quality_ddeg": finite(row, "_ddeg"),
            "quality_cdeg": finite(row, "_cdeg"),
            "station_count": finite(row, "_Nos"),
        }
        valid_rows.append((idx, normalized, row))

    groups: dict[str, list[tuple[int, dict[str, object], dict[str, str]]]] = {}
    for item in valid_rows:
        groups.setdefault(str(item[1]["localtime"]), []).append(item)
    deduped: list[dict[str, object]] = []
    duplicate_groups = 0
    duplicate_rows_removed = 0
    for group in groups.values():
        if len(group) > 1:
            duplicate_groups += 1
            duplicate_rows_removed += len(group) - 1
        best = min(group, key=lambda item: quality_key(item[2], item[0]))
        deduped.append(best[1])
    deduped.sort(key=lambda row: str(row["localtime"]))
    metadata = {
        "year": year,
        "zip_member": member.filename,
        "zip_member_crc32": f"{member.CRC:08x}",
        "zip_member_compressed_bytes": member.compress_size,
        "zip_member_uncompressed_bytes": member.file_size,
        "raw_rows": raw_rows,
        "invalid_rows": invalid_rows,
        "valid_rows_before_dedup": len(valid_rows),
        "exact_time_duplicate_groups": duplicate_groups,
        "duplicate_rows_removed": duplicate_rows_removed,
        "deduplicated_valid_rows": len(deduped),
        "field_count": len(reader.fieldnames),
        "fields": reader.fieldnames,
    }
    return deduped, metadata


def template_quantities(row: dict[str, object]) -> dict[str, float | bool]:
    sol_delta = wrap180(float(row["sol"]) - EPOCH)
    predicted_lsc = CENTER_LSC + DRIFT_LSC * sol_delta
    predicted_beta = CENTER_BETA + DRIFT_BETA * sol_delta
    predicted_vg = CENTER_VG + DRIFT_VG * sol_delta
    lsc_resid = wrap180(float(row["sun_centered_longitude_deg"]) - predicted_lsc)
    beta_resid = float(row["beta"]) - predicted_beta
    vg_resid = float(row["vg"]) - predicted_vg
    score = (
        (lsc_resid / SIGMA_LSC) ** 2
        + (beta_resid / SIGMA_BETA) ** 2
        + (vg_resid / SIGMA_VG) ** 2
    )
    in_activity = abs(sol_delta) <= ACTIVITY_HALF_WIDTH
    in_core = score <= CORE_SCORE_MAX
    in_source = (
        120.0 <= float(row["sun_centered_longitude_360_deg"]) <= 240.0
        and abs(float(row["beta"])) <= 35.0
        and 15.0 <= float(row["vg"]) <= 50.0
    )
    return {
        "sol_delta": sol_delta,
        "predicted_lsc": predicted_lsc,
        "predicted_beta": predicted_beta,
        "predicted_vg": predicted_vg,
        "lsc_residual_sigma": lsc_resid / SIGMA_LSC,
        "beta_residual_sigma": beta_resid / SIGMA_BETA,
        "vg_residual_sigma": vg_resid / SIGMA_VG,
        "template_score": score,
        "in_activity_window": in_activity,
        "in_radiant_speed_core": in_core,
        "in_expanded_antihelion_source": in_source,
    }


def d_sh(row: dict[str, object]) -> float:
    q1, e1 = GMN_ORBIT["q"], GMN_ORBIT["e"]
    i1, w1, n1 = (math.radians(GMN_ORBIT[k]) for k in ("incl", "peri", "node"))
    q2, e2 = float(row["q"]), float(row["e"])
    i2, w2, n2 = (math.radians(float(row[k])) for k in ("incl", "peri", "node"))
    cos_i = math.cos(i1) * math.cos(i2) + math.sin(i1) * math.sin(i2) * math.cos(n1 - n2)
    I = math.acos(max(-1.0, min(1.0, cos_i)))
    denom = math.cos(I / 2.0)
    arg = math.cos((i1 + i2) / 2.0) * math.sin((n1 - n2) / 2.0) / denom if abs(denom) > 1e-15 else 0.0
    Pi = w1 - w2 + 2.0 * math.asin(max(-1.0, min(1.0, arg)))
    return math.sqrt(
        (e1 - e2) ** 2
        + (q1 - q2) ** 2
        + (2.0 * math.sin(I / 2.0)) ** 2
        + (((e1 + e2) / 2.0) * 2.0 * math.sin(Pi / 2.0)) ** 2
    )


def log_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return -math.inf
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def fisher_greater(a: int, b: int, c: int, d: int) -> float:
    row1, row2 = a + b, c + d
    col1 = a + c
    total = row1 + row2
    lo = max(0, col1 - row2)
    hi = min(row1, col1)
    denominator = log_choose(total, row1)
    terms = []
    for x in range(max(a, lo), hi + 1):
        terms.append(math.exp(log_choose(col1, x) + log_choose(total - col1, row1 - x) - denominator))
    return min(1.0, math.fsum(terms))


def summarize(rows: list[dict[str, object]], label: str) -> tuple[dict[str, object], list[dict[str, object]]]:
    enriched: list[dict[str, object]] = []
    for row in rows:
        item = dict(row)
        item.update(template_quantities(row))
        item["orbit_d_sh_to_gmn"] = d_sh(row)
        enriched.append(item)

    source = [r for r in enriched if r["in_expanded_antihelion_source"]]
    inside = [r for r in source if r["in_activity_window"]]
    outside = [r for r in source if not r["in_activity_window"]]
    inside_core = [r for r in inside if r["in_radiant_speed_core"]]
    outside_core = [r for r in outside if r["in_radiant_speed_core"]]
    members = sorted(inside_core, key=lambda r: (int(r["year"]), str(r["localtime"])))
    a, b = len(inside_core), len(inside) - len(inside_core)
    c, d = len(outside_core), len(outside) - len(outside_core)
    odds = math.inf if b * c == 0 and a * d > 0 else ((a * d) / (b * c) if b * c else None)
    distances = sorted(float(r["orbit_d_sh_to_gmn"]) for r in members)
    q90 = None
    if distances:
        rank = 0.9 * (len(distances) - 1)
        low, high = math.floor(rank), math.ceil(rank)
        q90 = distances[low] if low == high else distances[low] + (rank - low) * (distances[high] - distances[low])
    summary = {
        "label": label,
        "deduplicated_rows": len(enriched),
        "expanded_antihelion_rows": len(source),
        "activity_window_rows": len(inside),
        "outside_window_rows": len(outside),
        "candidate_members": len(members),
        "candidate_years": sorted({int(r["year"]) for r in members}),
        "activity_table": {"inside_core": a, "inside_noncore": b, "outside_core": c, "outside_noncore": d},
        "fisher_exact_greater_p": fisher_greater(a, b, c, d),
        "odds_ratio": odds,
        "median_orbit_d_sh": statistics.median(distances) if distances else None,
        "q90_orbit_d_sh": q90,
        "maximum_orbit_d_sh": max(distances) if distances else None,
        "member_time_ids": [str(r["localtime"]) for r in members],
    }
    return summary, members


def write_members(path: Path, members: Iterable[dict[str, object]]) -> None:
    fields = [
        "year", "localtime", "sol", "sun_centered_longitude_deg", "beta", "vg",
        "template_score", "q", "e", "incl", "peri", "node", "orbit_d_sh_to_gmn",
        "stream_label", "id1", "id2", "quality_ddeg", "quality_cdeg", "station_count",
    ]
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in members:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, object]] = []
    archives_report: dict[str, object] = {}
    year_summaries: dict[str, object] = {}
    for year, url in ARCHIVES.items():
        data = fetch(url)
        rows, metadata = parse_archive(data, year)
        summary, members = summarize(rows, str(year))
        archives_report[str(year)] = {
            "url": url,
            "byte_count": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "md5": hashlib.md5(data).hexdigest(),
            "zip_crc_valid": True,
            **metadata,
        }
        year_summaries[str(year)] = summary
        write_members(args.output_dir / f"edmond_{year}_frozen_members.csv", members)
        all_rows.extend(rows)

    pooled_summary, pooled_members = summarize(all_rows, "2022-2023 pooled")
    write_members(args.output_dir / "edmond_2022_2023_frozen_members.csv", pooled_members)

    prior_external_times = {
        "_20220428_215139",
        "2022/04/25T13:17:27", "2022/04/29T17:13:16",
        "2023/04/27T13:08:10",
    }
    exact_overlap = sorted({str(r["localtime"]) for r in pooled_members} & prior_external_times)

    report = {
        "verdict": None,
        "claim_boundary": (
            "Frozen replication check in the latest usable full EDMOND v6.01 annual files. "
            "EDMOND is a compiled archive and is supporting evidence, not a fully independent instrument."
        ),
        "retuning_performed": False,
        "orbit_used_for_member_selection": False,
        "frozen_template": {
            "epoch_solar_longitude_deg": EPOCH,
            "center_sun_centered_longitude_deg": CENTER_LSC,
            "center_beta_deg": CENTER_BETA,
            "center_vg_km_s": CENTER_VG,
            "drift_lsc_deg_per_deg": DRIFT_LSC,
            "drift_beta_deg_per_deg": DRIFT_BETA,
            "drift_vg_km_s_per_deg": DRIFT_VG,
            "sigmas": {"lsc_deg": SIGMA_LSC, "beta_deg": SIGMA_BETA, "vg_km_s": SIGMA_VG},
            "core_score_max": CORE_SCORE_MAX,
            "activity_half_width_deg": ACTIVITY_HALF_WIDTH,
        },
        "deduplication": (
            "Exact _localtime groups collapsed before selection by lowest nonnegative _ddeg, "
            "then lowest nonnegative _cdeg, then highest _Nos, then source order."
        ),
        "archives": archives_report,
        "year_summaries": year_summaries,
        "pooled_summary": pooled_summary,
        "exact_time_overlap_with_named_prior_external_members": exact_overlap,
    }
    n = int(pooled_summary["candidate_members"])
    p = float(pooled_summary["fisher_exact_greater_p"])
    med = pooled_summary["median_orbit_d_sh"]
    q90 = pooled_summary["q90_orbit_d_sh"]
    if n >= 8 and p <= 0.01 and med is not None and q90 is not None and med <= 0.08 and q90 <= 0.15:
        report["verdict"] = "LATEST_USABLE_FULL_EDMOND_FROZEN_REPLICATION_PASS"
    elif n > 0:
        report["verdict"] = "LATEST_USABLE_FULL_EDMOND_SUPPORTIVE_NOT_STANDALONE_PASS"
    else:
        report["verdict"] = "LATEST_USABLE_FULL_EDMOND_CLEAN_NEGATIVE_NO_FROZEN_MEMBERS"

    report_path = args.output_dir / "latest_usable_edmond_frozen_validation.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "verdict": report["verdict"],
        "year_summaries": year_summaries,
        "pooled_summary": pooled_summary,
        "report": str(report_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
