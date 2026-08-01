#!/usr/bin/env python3
"""Parallel fast path for the EDMOND 2024 acquisition audit.

The exhaustive resolver remains the authoritative path inventory. This runner
uses the same ZIP/CRC/schema gate but probes deterministic site paths in
parallel, then checks exact Wayback captures. It never evaluates GhostStream
membership.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

import recover_current_edmond as audit


def fast_probe(url: str, source: str):
    """Probe one URL without mutating shared module state."""
    try:
        data, status, final_url, headers = audit.request(
            url,
            max_bytes=audit.MAX_ZIP_BYTES,
            timeout=12,
        )
        valid, _, reason = audit.valid_zip(data)
        outcome = "VALID_ZIP" if valid else f"NOT_ZIP: {reason}"
        probe = audit.Probe(
            url=url,
            source=source,
            status=status,
            final_url=final_url,
            content_type=headers.get("content-type"),
            content_length=len(data),
            first_bytes_hex=data[:16].hex(),
            outcome=outcome,
        )
        return probe, data if valid else None
    except urllib.error.HTTPError as exc:
        return (
            audit.Probe(
                url=url,
                source=source,
                status=exc.code,
                final_url=exc.geturl(),
                content_type=exc.headers.get("Content-Type") if exc.headers else None,
                content_length=None,
                first_bytes_hex=None,
                outcome="HTTP_ERROR",
                error=str(exc),
            ),
            None,
        )
    except Exception as exc:
        return (
            audit.Probe(
                url=url,
                source=source,
                status=None,
                final_url=None,
                content_type=None,
                content_length=None,
                first_bytes_hex=None,
                outcome="ERROR",
                error=f"{type(exc).__name__}: {exc}",
            ),
            None,
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    candidates = {audit.OFFICIAL_URL: "official_page_link"}
    for url in audit.plausible_candidates():
        candidates.setdefault(url, "plausible_site_path")

    # Add any attachment URL explicitly present in the current page.
    page_error = None
    try:
        page = audit.fetch_text(audit.OFFICIAL_PAGE, timeout=20)
        for url in audit.extract_urls_from_html(page, audit.OFFICIAL_PAGE):
            if "2024" in url and url.lower().endswith(".zip"):
                candidates[url] = "official_page_html"
    except Exception as exc:
        page_error = f"{type(exc).__name__}: {exc}"

    probes = []
    archive = None
    accepted = None
    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = {
            executor.submit(fast_probe, url, source): (url, source)
            for url, source in candidates.items()
        }
        for future in as_completed(futures):
            url, source = futures[future]
            try:
                probe, data = future.result()
            except Exception as exc:
                probe = audit.Probe(
                    url=url,
                    source=source,
                    status=None,
                    final_url=None,
                    content_type=None,
                    content_length=None,
                    first_bytes_hex=None,
                    outcome="WORKER_ERROR",
                    error=f"{type(exc).__name__}: {exc}",
                )
                data = None
            probes.append(asdict(probe))
            if probe.status != 404:
                print(f"{probe.status} {probe.outcome} {url}", flush=True)
            if data is not None and archive is None:
                candidate = audit.archive_report(data, url)
                if candidate["schema_and_row_gate_passed"]:
                    archive = data
                    accepted = candidate

    wayback_records = []
    if archive is None:
        urls, wayback_records = audit.wayback_candidates([audit.OFFICIAL_URL])
        for url in sorted(urls):
            probe, data = fast_probe(url, "wayback_capture")
            probes.append(asdict(probe))
            print(f"wayback {probe.status} {probe.outcome} {url}", flush=True)
            if data is not None:
                candidate = audit.archive_report(data, url)
                if candidate["schema_and_row_gate_passed"]:
                    archive = data
                    accepted = candidate
                    break

    reference_probe, reference_data = fast_probe(
        audit.REFERENCE_2023_URL, "official_2023_reference"
    )
    report = {
        "audit": "EDMOND_v6.01_2024_archive_recovery_fast",
        "official_page": audit.OFFICIAL_PAGE,
        "official_url": audit.OFFICIAL_URL,
        "expected_rows": audit.EXPECTED_ROWS,
        "frozen_scientific_solution_accessed": False,
        "candidate_membership_evaluated": False,
        "page_error": page_error,
        "probes": sorted(probes, key=lambda item: item["url"]),
        "wayback_records": wayback_records,
        "reference_2023_probe": asdict(reference_probe),
    }
    if reference_data is not None:
        report["reference_2023"] = {
            "byte_count": len(reference_data),
            "sha256": hashlib.sha256(reference_data).hexdigest(),
            "csv_members": audit.inspect_csvs(reference_data),
        }

    if archive is not None and accepted is not None:
        path = args.output_dir / "U2_2024_EDM.recovered.zip"
        path.write_bytes(archive)
        report["accepted_archive"] = accepted
        report["accepted_archive_url"] = accepted["source_url"]
        report["verdict"] = "RECOVERED_SCHEMA_VERIFIED_ARCHIVE"
        status = 0
    else:
        report["accepted_archive"] = None
        report["accepted_archive_url"] = None
        report["verdict"] = "FAST_PATH_NEGATIVE_NO_VALID_2024_ARCHIVE"
        status = 3

    output = args.output_dir / "current_edmond_recovery_fast.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "verdict": report["verdict"],
                "probes": len(probes),
                "accepted_archive_url": report["accepted_archive_url"],
                "reference_2023": reference_probe.outcome,
            },
            indent=2,
        )
    )
    return status


if __name__ == "__main__":
    sys.exit(main())
