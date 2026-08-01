#!/usr/bin/env python3
"""Compare linked EDMOND annual ZIP contents with the v6.01 page table.

The scientific evaluator must not silently treat stale or incomplete annual
attachments as the advertised 628,271-orbit v6.01 release. This audit records
ZIP checksums, CSV row counts, and every value in the CSV ``_Version`` column.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import urllib.error
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = "https://meteornews.net/assets/2025-03-29-edmond-database"
USER_AGENT = "GhostStream-EDMOND-release-integrity/1.0"
MAX_BYTES = 100 * 1024 * 1024

ADVERTISED = {
    2001: 248, 2002: 75, 2003: 121, 2004: 36, 2005: 81,
    2006: 510, 2007: 2315, 2008: 5344, 2009: 7911, 2010: 19049,
    2011: 36110, 2012: 33872, 2013: 41270, 2014: 46563,
    2015: 66396, 2016: 72009, 2017: 59055, 2018: 60020,
    2019: 61235, 2020: 39710, 2021: 18129, 2022: 19708,
    2023: 24991, 2024: 13513,
}


def download(year: int) -> bytes:
    url = f"{ROOT}/U2_{year}_EDM.zip"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/zip,*/*;q=0.8",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("archive exceeds size guard")
        return raw


def inspect(year: int) -> dict[str, Any]:
    url = f"{ROOT}/U2_{year}_EDM.zip"
    try:
        raw = download(year)
        if not raw.startswith(b"PK"):
            raise ValueError("missing ZIP signature")
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            bad = archive.testzip()
            if bad is not None:
                raise ValueError(f"CRC failure in {bad}")
            members = [
                item for item in archive.infolist()
                if not item.is_dir() and item.filename.lower().endswith(".csv")
            ]
            if len(members) != 1:
                raise ValueError(f"expected one CSV, found {len(members)}")
            member = members[0]
            text = archive.read(member).decode("utf-8-sig", errors="replace")
        reader = csv.DictReader(io.StringIO(text))
        if reader.fieldnames is None:
            raise ValueError("missing header")
        versions: dict[str, int] = {}
        rows = 0
        for row in reader:
            rows += 1
            version = (row.get("_Version") or "<missing>").strip()
            versions[version] = versions.get(version, 0) + 1
        advertised = ADVERTISED[year]
        return {
            "year": year,
            "url": url,
            "status": "VALIDATED",
            "zip_bytes": len(raw),
            "zip_sha256": hashlib.sha256(raw).hexdigest(),
            "csv_member": member.filename,
            "csv_columns": len(reader.fieldnames),
            "csv_rows": rows,
            "advertised_rows": advertised,
            "row_difference": rows - advertised,
            "row_fraction_of_advertised": rows / advertised if advertised else None,
            "version_counts": versions,
        }
    except urllib.error.HTTPError as exc:
        return {
            "year": year,
            "url": url,
            "status": "HTTP_ERROR",
            "http_status": exc.code,
            "advertised_rows": ADVERTISED[year],
            "error": str(exc),
        }
    except Exception as exc:
        return {
            "year": year,
            "url": url,
            "status": "ERROR",
            "advertised_rows": ADVERTISED[year],
            "error": f"{type(exc).__name__}: {exc}",
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(inspect, year): year for year in ADVERTISED}
        for future in as_completed(futures):
            result = future.result()
            rows.append(result)
            print(json.dumps(result, sort_keys=True), flush=True)
    rows.sort(key=lambda item: item["year"])

    valid = [item for item in rows if item["status"] == "VALIDATED"]
    actual_total = sum(item["csv_rows"] for item in valid)
    advertised_available_total = sum(item["advertised_rows"] for item in valid)
    advertised_full_total = sum(ADVERTISED.values())
    all_version_counts: dict[str, int] = {}
    for item in valid:
        for version, count in item["version_counts"].items():
            all_version_counts[version] = all_version_counts.get(version, 0) + count

    exact_count_years = [
        item["year"] for item in valid
        if item["csv_rows"] == item["advertised_rows"]
    ]
    mismatched_years = [
        {
            "year": item["year"],
            "csv_rows": item["csv_rows"],
            "advertised_rows": item["advertised_rows"],
            "difference": item["row_difference"],
            "fraction": item["row_fraction_of_advertised"],
            "version_counts": item["version_counts"],
        }
        for item in valid
        if item["csv_rows"] != item["advertised_rows"]
    ]

    if len(valid) == 23 and not exact_count_years and len(all_version_counts) == 1:
        verdict = "LINKED_ZIPS_ARE_INTERNALLY_CONSISTENT_BUT_DO_NOT_MATCH_ADVERTISED_V601_COUNTS"
    elif mismatched_years:
        verdict = "LINKED_ZIPS_PARTIALLY_MISMATCH_ADVERTISED_V601_COUNTS"
    else:
        verdict = "LINKED_ZIPS_MATCH_ADVERTISED_COUNTS"

    report = {
        "audit": "EDMOND_linked_release_integrity",
        "verdict": verdict,
        "advertised_release": "v6.01 (May 2025)",
        "advertised_full_orbits_2001_2024": advertised_full_total,
        "validated_years": [item["year"] for item in valid],
        "unavailable_or_invalid": [item for item in rows if item["status"] != "VALIDATED"],
        "actual_rows_in_validated_linked_ZIPs": actual_total,
        "advertised_rows_for_same_validated_years": advertised_available_total,
        "coverage_fraction_for_same_years": actual_total / advertised_available_total,
        "all_version_counts": all_version_counts,
        "exact_count_years": exact_count_years,
        "mismatched_years": mismatched_years,
        "per_year": rows,
        "claim_boundary": (
            "A linked ZIP can be technically valid yet fail to represent the counts advertised for v6.01. "
            "Scientific results from these attachments must be described as results on the currently linked files, not automatically as a complete v6.01 release test."
        ),
    }
    path = args.output_dir / "linked_release_integrity.json"
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "verdict": verdict,
                "actual_rows": actual_total,
                "advertised_same_year_rows": advertised_available_total,
                "coverage_fraction": report["coverage_fraction_for_same_years"],
                "version_counts": all_version_counts,
                "exact_count_years": exact_count_years,
                "mismatched_year_count": len(mismatched_years),
                "unavailable_years": [item["year"] for item in rows if item["status"] != "VALIDATED"],
                "report": str(path),
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
