#!/usr/bin/env python3
"""Audit public attachment and web-archive indexes for U2_2024_EDM.zip.

This acquisition audit is intentionally independent of the GhostStream
scientific selector. It searches attachment metadata and archived URL indexes,
then validates any recovered body with the same ZIP/CRC/13,513-row gate used by
``recover_current_edmond.py``.
"""

from __future__ import annotations

import argparse
import gzip
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import recover_current_edmond as base

TARGET = base.OFFICIAL_URL
TARGET_NAME = "U2_2024_EDM.zip"


def get_bytes(
    url: str,
    *,
    timeout: int = 35,
    max_bytes: int = 25 * 1024 * 1024,
    headers: dict[str, str] | None = None,
    attempts: int = 3,
) -> tuple[bytes, int, str, dict[str, str]]:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            return base.request(
                url,
                max_bytes=max_bytes,
                headers=headers,
                timeout=timeout,
            )
        except Exception as exc:  # evidence must retain transient failures
            last = exc
            if attempt + 1 < attempts:
                time.sleep(1.5 * (attempt + 1))
    assert last is not None
    raise last


def get_text(url: str, **kwargs: Any) -> tuple[str, int, str, dict[str, str]]:
    raw, status, final, headers = get_bytes(url, **kwargs)
    return raw.decode("utf-8", errors="replace"), status, final, headers


def probe_candidate(url: str, source: str) -> dict[str, Any]:
    try:
        raw, status, final, headers = get_bytes(
            url,
            timeout=60,
            max_bytes=base.MAX_ZIP_BYTES,
        )
        report = base.archive_report(raw, url)
        return {
            "source": source,
            "url": url,
            "status": status,
            "final_url": final,
            "content_type": headers.get("content-type"),
            "accepted": bool(report["schema_and_row_gate_passed"]),
            "archive_report": report,
        }
    except urllib.error.HTTPError as exc:
        return {
            "source": source,
            "url": url,
            "status": exc.code,
            "accepted": False,
            "error": str(exc),
        }
    except Exception as exc:
        return {
            "source": source,
            "url": url,
            "status": None,
            "accepted": False,
            "error": f"{type(exc).__name__}: {exc}",
        }


def wordpress_queries() -> list[dict[str, Any]]:
    endpoints: list[tuple[str, str]] = []
    for host in (
        "https://meteornews.net",
        "https://www.meteornews.net",
        "https://emeteornews.net",
        "https://www.emeteornews.net",
    ):
        for term in (TARGET_NAME, "U2_2024_EDM", "EDMOND 2024", "2024 EDM"):
            query = urllib.parse.urlencode(
                {"search": term, "per_page": 100, "context": "view"}
            )
            endpoints.append((host, f"{host}/wp-json/wp/v2/media?{query}"))

    results: list[dict[str, Any]] = []

    def run(item: tuple[str, str]) -> dict[str, Any]:
        host, url = item
        try:
            text, status, final, headers = get_text(url, timeout=30, max_bytes=5_000_000)
            payload = json.loads(text)
            media: list[dict[str, Any]] = []
            if isinstance(payload, list):
                for entry in payload:
                    if not isinstance(entry, dict):
                        continue
                    source_url = entry.get("source_url")
                    guid = entry.get("guid")
                    if isinstance(guid, dict):
                        guid = guid.get("rendered")
                    media.append(
                        {
                            "id": entry.get("id"),
                            "date": entry.get("date"),
                            "slug": entry.get("slug"),
                            "source_url": source_url,
                            "guid": guid,
                            "media_details_file": (
                                entry.get("media_details", {}).get("file")
                                if isinstance(entry.get("media_details"), dict)
                                else None
                            ),
                        }
                    )
            return {
                "host": host,
                "url": url,
                "status": status,
                "final_url": final,
                "content_type": headers.get("content-type"),
                "result_count": len(media),
                "media": media,
            }
        except Exception as exc:
            return {
                "host": host,
                "url": url,
                "status": None,
                "result_count": None,
                "media": [],
                "error": f"{type(exc).__name__}: {exc}",
            }

    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(run, item) for item in endpoints]
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda row: row["url"])


def sitemap_queries() -> list[dict[str, Any]]:
    urls = [
        "https://meteornews.net/wp-sitemap.xml",
        "https://meteornews.net/sitemap_index.xml",
        "https://meteornews.net/wp-sitemap-posts-attachment-1.xml",
        "https://www.meteornews.net/wp-sitemap.xml",
        "https://emeteornews.net/wp-sitemap.xml",
    ]
    out: list[dict[str, Any]] = []
    for url in urls:
        try:
            text, status, final, headers = get_text(url, timeout=30, max_bytes=15_000_000)
            matches = sorted(
                set(
                    re.findall(
                        r"https?://[^<\s\"']*(?:U2_2024_EDM|2024[^<\s\"']*EDM|EDM[^<\s\"']*2024)[^<\s\"']*",
                        text,
                        flags=re.I,
                    )
                )
            )
            out.append(
                {
                    "url": url,
                    "status": status,
                    "final_url": final,
                    "content_type": headers.get("content-type"),
                    "byte_count": len(text.encode()),
                    "matches": matches,
                }
            )
        except Exception as exc:
            out.append(
                {
                    "url": url,
                    "status": None,
                    "matches": [],
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return out


def wayback_availability() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for stamp in ("20250401", "20250501", "20250601", "20260101", "20260801"):
        query = urllib.parse.urlencode({"url": TARGET, "timestamp": stamp})
        url = f"https://archive.org/wayback/available?{query}"
        try:
            text, status, final, _ = get_text(url, timeout=45, max_bytes=2_000_000)
            rows.append(
                {
                    "timestamp_requested": stamp,
                    "url": url,
                    "status": status,
                    "final_url": final,
                    "response": json.loads(text),
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "timestamp_requested": stamp,
                    "url": url,
                    "status": None,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return rows


def wayback_cdx() -> list[dict[str, Any]]:
    patterns = [
        TARGET,
        "meteornews.net/assets/2025-03-29-edmond-database/*2024*",
        "meteornews.net/*U2_2024_EDM*",
        "www.meteornews.net/*U2_2024_EDM*",
        "emeteornews.net/*U2_2024_EDM*",
    ]
    rows: list[dict[str, Any]] = []
    for pattern in patterns:
        params = {
            "url": pattern,
            "output": "json",
            "fl": "timestamp,original,statuscode,mimetype,digest,length",
            "filter": "statuscode:200",
            "collapse": "digest",
        }
        url = "https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(params)
        try:
            text, status, final, _ = get_text(url, timeout=90, max_bytes=10_000_000)
            captures: list[dict[str, Any]] = []
            payload = json.loads(text)
            if isinstance(payload, list) and len(payload) > 1:
                header = payload[0]
                captures = [dict(zip(header, item)) for item in payload[1:]]
            rows.append(
                {
                    "pattern": pattern,
                    "url": url,
                    "status": status,
                    "final_url": final,
                    "captures": captures,
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "pattern": pattern,
                    "url": url,
                    "status": None,
                    "captures": [],
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return rows


def common_crawl() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    query_rows: list[dict[str, Any]] = []
    recovered: list[dict[str, Any]] = []
    try:
        text, _, _, _ = get_text(
            "https://index.commoncrawl.org/collinfo.json",
            timeout=60,
            max_bytes=5_000_000,
        )
        indexes = json.loads(text)
    except Exception as exc:
        return ([{"error": f"index discovery failed: {type(exc).__name__}: {exc}"}], [])

    if not isinstance(indexes, list):
        return ([{"error": "unexpected collinfo response"}], [])

    for index in indexes[:12]:
        api = index.get("cdx-api") if isinstance(index, dict) else None
        name = index.get("name") if isinstance(index, dict) else None
        if not isinstance(api, str):
            continue
        url = api + "?" + urllib.parse.urlencode({"url": TARGET, "output": "json"})
        try:
            text, status, final, _ = get_text(url, timeout=60, max_bytes=10_000_000)
            records: list[dict[str, Any]] = []
            for line in text.splitlines():
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(value, dict):
                    records.append(value)
            query_rows.append(
                {
                    "index": name,
                    "url": url,
                    "status": status,
                    "final_url": final,
                    "records": records,
                }
            )
            for record in records:
                filename = record.get("filename")
                offset = record.get("offset")
                length = record.get("length")
                if not filename or offset is None or length is None:
                    continue
                try:
                    offset_i = int(offset)
                    length_i = int(length)
                    if length_i > base.MAX_ZIP_BYTES + 3_000_000:
                        continue
                    warc_url = "https://data.commoncrawl.org/" + str(filename)
                    raw, _, _, _ = get_bytes(
                        warc_url,
                        timeout=90,
                        max_bytes=length_i + 10,
                        headers={"Range": f"bytes={offset_i}-{offset_i + length_i - 1}"},
                    )
                    if raw.startswith(b"\x1f\x8b"):
                        raw = gzip.decompress(raw)
                    first = raw.find(b"\r\n\r\n")
                    second = raw.find(b"\r\n\r\n", first + 4) if first >= 0 else -1
                    body = raw[second + 4 :] if second >= 0 else b""
                    report = base.archive_report(body, f"commoncrawl:{name}:{offset_i}")
                    recovered.append(
                        {
                            "index": name,
                            "record": record,
                            "accepted": bool(report["schema_and_row_gate_passed"]),
                            "archive_report": report,
                        }
                    )
                except Exception as exc:
                    recovered.append(
                        {
                            "index": name,
                            "record": record,
                            "accepted": False,
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
        except Exception as exc:
            query_rows.append(
                {
                    "index": name,
                    "url": url,
                    "status": None,
                    "records": [],
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    return query_rows, recovered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    wp = wordpress_queries()
    sitemap = sitemap_queries()
    availability = wayback_availability()
    cdx = wayback_cdx()
    cc_queries, cc_recovered = common_crawl()

    candidate_urls: set[str] = set()
    for row in wp:
        for media in row.get("media", []):
            for key in ("source_url", "guid"):
                value = media.get(key)
                if isinstance(value, str) and value:
                    candidate_urls.add(value)
    for row in sitemap:
        candidate_urls.update(row.get("matches", []))
    for row in availability:
        closest = row.get("response", {}).get("archived_snapshots", {}).get("closest", {})
        if isinstance(closest, dict) and closest.get("available") and closest.get("url"):
            candidate_urls.add(str(closest["url"]).replace("/http", "id_/http", 1))
    for row in cdx:
        for capture in row.get("captures", []):
            timestamp = capture.get("timestamp")
            original = capture.get("original")
            if timestamp and original:
                candidate_urls.add(
                    f"https://web.archive.org/web/{timestamp}id_/{original}"
                )

    probes: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {
            pool.submit(probe_candidate, url, "attachment_or_archive_index"): url
            for url in sorted(candidate_urls)
        }
        for future in as_completed(futures):
            probes.append(future.result())

    accepted = [item for item in probes if item.get("accepted")]
    accepted.extend(item for item in cc_recovered if item.get("accepted"))

    report = {
        "audit": "EDMOND_2024_attachment_and_archive_indices",
        "target": TARGET,
        "expected_data_rows": base.EXPECTED_ROWS,
        "scientific_selector_accessed": False,
        "candidate_membership_evaluated": False,
        "wordpress_queries": wp,
        "sitemap_queries": sitemap,
        "wayback_availability": availability,
        "wayback_cdx": cdx,
        "common_crawl_queries": cc_queries,
        "common_crawl_recovered_bodies": cc_recovered,
        "candidate_urls_discovered": sorted(candidate_urls),
        "candidate_url_probes": sorted(probes, key=lambda row: row["url"]),
        "accepted_archives": accepted,
        "verdict": (
            "ARCHIVAL_COPY_RECOVERED_AND_SCHEMA_VERIFIED"
            if accepted
            else "NO_VALID_COPY_IN_QUERIED_ATTACHMENT_OR_ARCHIVE_INDEXES"
        ),
    }
    path = args.output_dir / "archive_index_audit.json"
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "verdict": report["verdict"],
                "wordpress_queries": len(wp),
                "wordpress_media_records": sum(
                    len(row.get("media", [])) for row in wp
                ),
                "sitemap_matches": sum(
                    len(row.get("matches", [])) for row in sitemap
                ),
                "wayback_captures": sum(
                    len(row.get("captures", [])) for row in cdx
                ),
                "common_crawl_records": sum(
                    len(row.get("records", [])) for row in cc_queries
                ),
                "candidate_urls_probed": len(probes),
                "accepted_archives": len(accepted),
                "report": str(path),
            },
            indent=2,
        ),
        flush=True,
    )
    return 0 if accepted else 3


if __name__ == "__main__":
    sys.exit(main())
