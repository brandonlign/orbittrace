#!/usr/bin/env python3
"""Reconnect the preserved GhostStream lookup to the live official GMN database.

This is a fail-closed reconstruction stage. It does not assert that the preserved
candidate is reproduced. It fetches the full source records corresponding to the
95 committed lookup rows, inventories the live database schema, and downloads a
broad non-orbital neighbourhood around the frozen radiant/time solution for the
next reconstruction stage.

Only Python's standard library is required.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

API_URL = "https://explore.globalmeteornetwork.org/gmn_data_store/-/query.csv"
LOOKUP_DEFAULT = Path(
    "pilots/ghoststream/april_stream/mdc/GhostStream_April_95_GMN_lookup.csv"
)
OUTPUT_DEFAULT = Path("pilots/ghoststream/reconstruction/live_source_audit")

SOURCE_COLUMNS = [
    "unique_trajectory_identifier",
    "beginning_utc_time",
    "shower_iau_no",
    "sol_lon_deg",
    "rageo_deg",
    "decgeo_deg",
    "lamgeo_deg",
    "betgeo_deg",
    "vgeo_km_s",
    "a_au",
    "e",
    "i_deg",
    "peri_deg",
    "node_deg",
    "q_au",
    "tisserandj",
    "medianfiterr_arcsec",
    "beg_in_fov",
    "end_in_fov",
    "latbeg_n_deg",
    "lonbeg_e_deg",
    "latend_n_deg",
    "lonend_e_deg",
    "created_at",
    "updated_at",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sql_literal(text: str) -> str:
    return "'" + text.replace("'", "''") + "'"


def fetch_csv(sql: str, *, retries: int = 5, timeout: int = 120) -> tuple[list[dict[str, str]], dict[str, Any]]:
    query = urllib.parse.urlencode({"sql": sql, "_size": "max"})
    url = f"{API_URL}?{query}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "GhostStream-reconstruction/1.0 (+https://github.com/brandonlign/isef)",
            "Accept": "text/csv,*/*;q=0.1",
        },
    )
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = response.read()
                status = getattr(response, "status", 200)
                content_type = response.headers.get("Content-Type", "")
            text = payload.decode("utf-8-sig")
            rows = list(csv.DictReader(io.StringIO(text)))
            return rows, {
                "url": url,
                "status": status,
                "content_type": content_type,
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
                "rows": len(rows),
                "attempt": attempt,
            }
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(min(2 ** (attempt - 1), 16))
    raise RuntimeError(f"GMN query failed after {retries} attempts: {last_error}; SQL={sql}")


def chunks(items: list[str], size: int) -> Iterable[list[str]]:
    for index in range(0, len(items), size):
        yield items[index : index + size]


def lookup_time_to_sql(value: str) -> str:
    # Committed form: YYYY-MM-DD-HH:MM:SS
    if len(value) != 19 or value[10] != "-":
        raise ValueError(f"Unexpected lookup timestamp: {value!r}")
    return value[:10] + " " + value[11:]


def as_float(row: dict[str, str], key: str) -> float | None:
    value = row.get(key, "")
    if value is None or value.strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def circular_delta_deg(a: float, b: float) -> float:
    return ((a - b + 180.0) % 360.0) - 180.0


def source_sc_lon(row: dict[str, str]) -> float | None:
    lam = as_float(row, "lamgeo_deg")
    sol = as_float(row, "sol_lon_deg")
    if lam is None or sol is None:
        return None
    return (lam - sol) % 360.0


def row_distance_to_lookup(source: dict[str, str], lookup: dict[str, str]) -> float:
    terms: list[float] = []
    mapping = {
        "rageo_deg": "RA",
        "decgeo_deg": "DE",
        "vgeo_km_s": "VG",
        "sol_lon_deg": "LS",
        "lamgeo_deg": "LO",
        "betgeo_deg": "LA",
    }
    scales = {
        "rageo_deg": 1.0,
        "decgeo_deg": 1.0,
        "vgeo_km_s": 1.0,
        "sol_lon_deg": 1.0,
        "lamgeo_deg": 1.0,
        "betgeo_deg": 1.0,
    }
    for source_key, lookup_key in mapping.items():
        sv = as_float(source, source_key)
        try:
            lv = float(lookup[lookup_key])
        except (ValueError, KeyError):
            continue
        if sv is None:
            continue
        if source_key in {"rageo_deg", "sol_lon_deg", "lamgeo_deg"}:
            delta = circular_delta_deg(sv, lv)
        else:
            delta = sv - lv
        terms.append((delta / scales[source_key]) ** 2)
    return math.sqrt(sum(terms)) if terms else math.inf


def compare_row(source: dict[str, str], lookup: dict[str, str]) -> dict[str, Any]:
    comparisons: dict[str, Any] = {}
    mapping = {
        "RA": "rageo_deg",
        "DE": "decgeo_deg",
        "VG": "vgeo_km_s",
        "LS": "sol_lon_deg",
        "LO": "lamgeo_deg",
        "LA": "betgeo_deg",
    }
    for lookup_key, source_key in mapping.items():
        expected = float(lookup[lookup_key])
        actual = as_float(source, source_key)
        if actual is None:
            comparisons[lookup_key] = {"expected": expected, "actual": None, "delta": None}
            continue
        delta = circular_delta_deg(actual, expected) if lookup_key in {"RA", "LS", "LO"} else actual - expected
        comparisons[lookup_key] = {"expected": expected, "actual": actual, "delta": delta}

    expected_sc = float(lookup["SCLO"])
    actual_sc = source_sc_lon(source)
    comparisons["SCLO"] = {
        "expected": expected_sc,
        "actual": actual_sc,
        "delta": None if actual_sc is None else circular_delta_deg(actual_sc, expected_sc),
    }
    return comparisons


def max_abs_delta(comparisons: dict[str, Any]) -> float | None:
    values = [
        abs(item["delta"])
        for item in comparisons.values()
        if isinstance(item, dict) and item.get("delta") is not None
    ]
    return max(values) if values else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lookup", type=Path, default=LOOKUP_DEFAULT)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    lookup_bytes = args.lookup.read_bytes()
    lookup_rows = list(csv.DictReader(io.StringIO(lookup_bytes.decode("utf-8-sig"))))
    if len(lookup_rows) != 95:
        raise RuntimeError(f"Expected 95 committed lookup rows, found {len(lookup_rows)}")

    timestamp_to_lookup: dict[str, dict[str, str]] = {}
    for row in lookup_rows:
        timestamp = lookup_time_to_sql(row["Tobs"])
        if timestamp in timestamp_to_lookup:
            raise RuntimeError(f"Duplicate timestamp in committed lookup: {timestamp}")
        timestamp_to_lookup[timestamp] = row

    query_evidence: list[dict[str, Any]] = []
    source_candidates: list[dict[str, str]] = []
    timestamps = list(timestamp_to_lookup)
    columns_sql = ", ".join(SOURCE_COLUMNS)
    for group in chunks(timestamps, 8):
        in_sql = ", ".join(sql_literal(value) for value in group)
        sql = (
            f"select {columns_sql} from meteor "
            f"where substr(beginning_utc_time, 1, 19) in ({in_sql}) "
            "order by beginning_utc_time, medianfiterr_arcsec"
        )
        rows, evidence = fetch_csv(sql)
        evidence["purpose"] = "exact_lookup_reconnection"
        evidence["timestamp_count"] = len(group)
        query_evidence.append(evidence)
        source_candidates.extend(rows)

    by_timestamp: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_candidates:
        timestamp = row.get("beginning_utc_time", "")[:19]
        by_timestamp[timestamp].append(row)

    matched_rows: list[dict[str, Any]] = []
    missing: list[str] = []
    ambiguous: list[dict[str, Any]] = []
    shower_labels: Counter[str] = Counter()
    maximum_lookup_delta = 0.0

    for timestamp, lookup in timestamp_to_lookup.items():
        candidates = by_timestamp.get(timestamp, [])
        if not candidates:
            missing.append(timestamp)
            continue
        ranked = sorted(candidates, key=lambda row: row_distance_to_lookup(row, lookup))
        chosen = ranked[0]
        comparisons = compare_row(chosen, lookup)
        row_max_delta = max_abs_delta(comparisons)
        if row_max_delta is not None:
            maximum_lookup_delta = max(maximum_lookup_delta, row_max_delta)
        shower_labels[str(chosen.get("shower_iau_no", ""))] += 1
        matched_rows.append(
            {
                "lookup_cur_num": lookup["CurNum"],
                "lookup_timestamp": timestamp,
                "candidate_rows_at_exact_second": len(candidates),
                "selected_source_record": chosen,
                "lookup_comparison": comparisons,
            }
        )
        if len(candidates) > 1:
            ambiguous.append(
                {
                    "timestamp": timestamp,
                    "rows": len(candidates),
                    "selected_identifier": chosen.get("unique_trajectory_identifier"),
                    "ranked_identifiers": [
                        {
                            "identifier": row.get("unique_trajectory_identifier"),
                            "distance_to_lookup": row_distance_to_lookup(row, lookup),
                            "medianfiterr_arcsec": as_float(row, "medianfiterr_arcsec"),
                        }
                        for row in ranked
                    ],
                }
            )

    schema_results: dict[str, Any] = {}
    schema_queries = {
        "objects": "select type, name, sql from sqlite_master where type in ('table','view') order by type, name",
        "meteor_columns": "select * from pragma_table_info('meteor') order by cid",
    }
    for name, sql in schema_queries.items():
        try:
            rows, evidence = fetch_csv(sql)
            schema_results[name] = rows
            evidence["purpose"] = f"schema_{name}"
            query_evidence.append(evidence)
        except Exception as exc:  # Keep exact-source recovery useful even if schema access is restricted.
            schema_results[name] = {"error": str(exc)}

    # Download a deliberately broad, non-orbital neighbourhood. This is not the
    # final member selector. It is wide enough to reconstruct fit/station/core
    # rules without using q, e, i, omega, or node in selection.
    neighbourhood_sql = (
        f"select {columns_sql} from meteor "
        "where sol_lon_deg between 28.0 and 45.0 "
        "and (lamgeo_deg - sol_lon_deg) between 202.0 and 219.0 "
        "and betgeo_deg between -1.0 and 16.0 "
        "and vgeo_km_s between 30.0 and 45.0 "
        "and medianfiterr_arcsec <= 300.0 "
        "and cast(substr(beginning_utc_time, 1, 4) as integer) between 2019 and 2026 "
        "order by beginning_utc_time, medianfiterr_arcsec"
    )
    neighbourhood_rows, neighbourhood_evidence = fetch_csv(neighbourhood_sql)
    neighbourhood_evidence["purpose"] = "broad_nonorbital_candidate_neighbourhood"
    query_evidence.append(neighbourhood_evidence)

    neighbourhood_path = output_dir / "gmn_broad_nonorbital_neighbourhood.csv"
    if neighbourhood_rows:
        with neighbourhood_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(neighbourhood_rows[0]))
            writer.writeheader()
            writer.writerows(neighbourhood_rows)
    else:
        neighbourhood_path.write_text("", encoding="utf-8")

    matched_source_path = output_dir / "gmn_reconnected_95_source_records.csv"
    source_only = [entry["selected_source_record"] for entry in matched_rows]
    if source_only:
        with matched_source_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(source_only[0]))
            writer.writeheader()
            writer.writerows(source_only)

    generated_at = datetime.now(timezone.utc).isoformat()
    summary = {
        "generated_at_utc": generated_at,
        "status": "PASS" if len(matched_rows) == 95 and not missing else "FAIL",
        "purpose": "Reconnect preserved GhostStream lookup rows to live official GMN source records; not a final scientific reproduction.",
        "source": {
            "api": API_URL,
            "official_gmn_data_index": "https://globalmeteornetwork.org/data/traj_summary_data/",
        },
        "committed_lookup": {
            "path": str(args.lookup),
            "rows": len(lookup_rows),
            "sha256": sha256_bytes(lookup_bytes),
        },
        "reconnection": {
            "matched": len(matched_rows),
            "missing": missing,
            "ambiguous_exact_seconds": ambiguous,
            "live_shower_iau_no_counts": dict(shower_labels),
            "maximum_absolute_lookup_field_delta": maximum_lookup_delta,
        },
        "broad_neighbourhood": {
            "rows": len(neighbourhood_rows),
            "path": str(neighbourhood_path),
            "selection_uses_orbital_elements": False,
            "bounds": {
                "solar_longitude_deg": [28.0, 45.0],
                "sun_centered_ecliptic_longitude_deg": [202.0, 219.0],
                "ecliptic_latitude_deg": [-1.0, 16.0],
                "geocentric_speed_km_s": [30.0, 45.0],
                "median_fit_error_arcsec_max": 300.0,
                "years": [2019, 2026],
            },
        },
        "schema": schema_results,
        "query_evidence": query_evidence,
        "matches": matched_rows,
    }

    summary_path = output_dir / "live_gmn_source_audit.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    markdown = [
        "# GhostStream live GMN source reconstruction audit",
        "",
        f"Generated: `{generated_at}`",
        "",
        f"**Status: {summary['status']}**",
        "",
        "This stage reconnects the committed 95-row lookup to the live official GMN database. It does not by itself reproduce the discovery statistics.",
        "",
        "## Exact-source reconnection",
        "",
        f"- Committed lookup rows: **{len(lookup_rows)}**",
        f"- Live source records matched: **{len(matched_rows)}**",
        f"- Missing timestamps: **{len(missing)}**",
        f"- Exact-second timestamps with multiple live rows: **{len(ambiguous)}**",
        f"- Maximum absolute delta across committed lookup fields: **{maximum_lookup_delta:.12g}**",
        f"- Live `shower_iau_no` counts: `{dict(shower_labels)}`",
        "",
        "## Reconstruction dataset",
        "",
        f"- Broad non-orbital neighbourhood rows: **{len(neighbourhood_rows)}**",
        "- Selection dimensions: solar longitude, Sun-centered ecliptic radiant, latitude, geocentric speed, fit error, and year.",
        "- Orbital elements were fetched for later testing but were not used to select this neighbourhood.",
        "",
        "## Files",
        "",
        "- `live_gmn_source_audit.json` — full query provenance, schema inventory, comparisons, and source records",
        "- `gmn_reconnected_95_source_records.csv` — selected live source record for every committed lookup row",
        "- `gmn_broad_nonorbital_neighbourhood.csv` — broad reconstruction sample",
        "",
        "## Fail-closed interpretation",
        "",
    ]
    if summary["status"] == "PASS":
        markdown.append(
            "The preserved lookup has been reconnected to live official GMN records. The next stage may reconstruct quality filtering, deduplication, frozen radiant-speed membership, and statistical tests from these source records."
        )
    else:
        markdown.append(
            "The source reconnection is incomplete. Do not proceed to claim reproduction until every missing or ambiguous record is resolved and documented."
        )
    markdown.append("")
    (output_dir / "LIVE_GMN_SOURCE_AUDIT.md").write_text("\n".join(markdown), encoding="utf-8")

    print(json.dumps({
        "status": summary["status"],
        "matched": len(matched_rows),
        "missing": len(missing),
        "ambiguous": len(ambiguous),
        "neighbourhood_rows": len(neighbourhood_rows),
        "output": str(summary_path),
    }, indent=2))
    return 0 if summary["status"] == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
