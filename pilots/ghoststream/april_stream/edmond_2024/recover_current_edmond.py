#!/usr/bin/env python3
"""Recover and validate the missing EDMOND v6.01 2024 annual archive.

This is an acquisition-only audit. It does not alter the frozen GhostStream
solution or inspect candidate membership. A file is accepted only when it is a
real ZIP, all ZIP members pass CRC validation, and a CSV member contains the
13,513 data rows advertised on the EDMOND v6.01 public page.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

OFFICIAL_PAGE = "https://meteornews.net/edmond/"
OFFICIAL_URL = (
    "https://meteornews.net/assets/2025-03-29-edmond-database/"
    "U2_2024_EDM.zip"
)
REFERENCE_2023_URL = (
    "https://meteornews.net/assets/2025-03-29-edmond-database/"
    "U2_2023_EDM.zip"
)
EXPECTED_ROWS = 13_513
USER_AGENT = (
    "GhostStream-EDMOND-recovery/1.0 "
    "(+https://github.com/brandonlign/isef)"
)
MAX_ZIP_BYTES = 100 * 1024 * 1024
MAX_TEXT_BYTES = 20 * 1024 * 1024


@dataclass
class Probe:
    url: str
    source: str
    status: int | None
    final_url: str | None
    content_type: str | None
    content_length: int | None
    first_bytes_hex: str | None
    outcome: str
    error: str | None = None


def request(
    url: str,
    *,
    max_bytes: int,
    headers: dict[str, str] | None = None,
    timeout: int = 40,
) -> tuple[bytes, int, str, dict[str, str]]:
    request_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Encoding": "identity",
    }
    if headers:
        request_headers.update(headers)
    req = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        status = int(getattr(response, "status", response.getcode()))
        final_url = response.geturl()
        response_headers = {k.lower(): v for k, v in response.headers.items()}
        content_length = response_headers.get("content-length")
        if content_length is not None and int(content_length) > max_bytes:
            raise ValueError(
                f"declared content length {content_length} exceeds {max_bytes}"
            )
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = response.read(min(1024 * 1024, max_bytes + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > max_bytes:
                raise ValueError(f"response exceeded {max_bytes} bytes")
        return b"".join(chunks), status, final_url, response_headers


def fetch_text(url: str, *, timeout: int = 40) -> str:
    data, _, _, headers = request(url, max_bytes=MAX_TEXT_BYTES, timeout=timeout)
    encoding = "utf-8"
    content_type = headers.get("content-type", "")
    match = re.search(r"charset=([^;\s]+)", content_type, re.I)
    if match:
        encoding = match.group(1).strip('"\'')
    return data.decode(encoding, errors="replace")


def valid_zip(data: bytes) -> tuple[bool, list[dict[str, object]], str | None]:
    if not data.startswith(b"PK"):
        return False, [], "missing PK ZIP signature"
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            bad = archive.testzip()
            if bad is not None:
                return False, [], f"CRC failure in {bad}"
            members = [
                {
                    "name": item.filename,
                    "compressed_size": item.compress_size,
                    "uncompressed_size": item.file_size,
                    "crc32": f"{item.CRC:08x}",
                }
                for item in archive.infolist()
                if not item.is_dir()
            ]
            if not members:
                return False, [], "ZIP contains no files"
            return True, members, None
    except zipfile.BadZipFile as exc:
        return False, [], f"BadZipFile: {exc}"


def decode_csv(raw: bytes) -> tuple[str, str]:
    encodings = ("utf-8-sig", "cp1250", "cp1252", "latin-1")
    for encoding in encodings:
        try:
            text = raw.decode(encoding)
            return text, encoding
        except UnicodeDecodeError:
            pass
    return raw.decode("latin-1", errors="replace"), "latin-1-replace"


def inspect_csvs(data: bytes) -> list[dict[str, object]]:
    reports: list[dict[str, object]] = []
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for item in archive.infolist():
            if item.is_dir() or not item.filename.lower().endswith((".csv", ".txt")):
                continue
            raw = archive.read(item)
            text, encoding = decode_csv(raw)
            sample = text[:100_000]
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;|\t")
                delimiter = dialect.delimiter
            except csv.Error:
                delimiter = ","
            reader = csv.reader(io.StringIO(text), delimiter=delimiter)
            rows = [row for row in reader if row and any(cell.strip() for cell in row)]
            header = rows[0] if rows else []
            data_rows = max(0, len(rows) - 1)
            reports.append(
                {
                    "member": item.filename,
                    "encoding": encoding,
                    "delimiter": delimiter,
                    "header": header,
                    "row_count_excluding_header": data_rows,
                    "row_count_including_header": len(rows),
                    "first_data_row": rows[1] if len(rows) > 1 else None,
                }
            )
    return reports


def extract_urls_from_html(text: str, base_url: str) -> set[str]:
    urls: set[str] = set()
    for match in re.finditer(r"(?:href|src)=[\"']([^\"']+)[\"']", text, re.I):
        value = match.group(1).replace("&amp;", "&")
        absolute = urllib.parse.urljoin(base_url, value)
        if "2024" in absolute or "edmond" in absolute.lower():
            urls.add(absolute)
    return urls


def wordpress_candidates() -> set[str]:
    candidates: set[str] = set()
    hosts = (
        "https://meteornews.net",
        "https://www.meteornews.net",
        "https://emeteornews.net",
        "https://www.emeteornews.net",
    )
    searches = ("U2_2024_EDM", "2024 EDM", "EDMOND 2024")
    for host in hosts:
        for term in searches:
            query = urllib.parse.urlencode({"search": term, "per_page": 100})
            url = f"{host}/wp-json/wp/v2/media?{query}"
            try:
                payload = json.loads(fetch_text(url))
            except Exception:
                continue
            if not isinstance(payload, list):
                continue
            for item in payload:
                if not isinstance(item, dict):
                    continue
                for key in ("source_url", "guid"):
                    value = item.get(key)
                    if isinstance(value, dict):
                        value = value.get("rendered")
                    if isinstance(value, str) and value:
                        candidates.add(value)
                media_details = item.get("media_details")
                if isinstance(media_details, dict):
                    file_name = media_details.get("file")
                    if isinstance(file_name, str):
                        candidates.add(
                            urllib.parse.urljoin(host + "/wp-content/uploads/", file_name)
                        )
    return candidates


def plausible_candidates() -> set[str]:
    names = {
        "U2_2024_EDM.zip",
        "U2_2024_EDM.ZIP",
        "u2_2024_edm.zip",
        "U2_2024_EDM_v601.zip",
        "U2_2024_EDM_v6.01.zip",
        "U2_2024_EDM_v6_01.zip",
        "U2_2024_EDM_601.zip",
        "U2_2024_EDM-final.zip",
        "U2_2024_EDM_final.zip",
        "U2_2024_EDM(1).zip",
        "U2_2024_EDM%20(1).zip",
        "U2_2024_EDM.zip.zip",
    }
    hosts = (
        "https://meteornews.net",
        "https://www.meteornews.net",
        "https://emeteornews.net",
        "https://www.emeteornews.net",
    )
    roots = {
        "/assets/2025-03-29-edmond-database/",
        "/assets/2025-05-01-edmond-database/",
        "/assets/2025-05-31-edmond-database/",
        "/edmond/edmond/edmond-database/",
    }
    for year, month in ((2024, 12), (2025, 3), (2025, 4), (2025, 5), (2025, 6)):
        roots.add(f"/wp-content/uploads/{year}/{month:02d}/")
    return {
        urllib.parse.urljoin(host + root, name)
        for host in hosts
        for root in roots
        for name in names
    }


def wayback_candidates(targets: Iterable[str]) -> tuple[set[str], list[dict[str, object]]]:
    recovered: set[str] = set()
    records: list[dict[str, object]] = []
    for target in targets:
        query = urllib.parse.urlencode(
            {
                "url": target,
                "output": "json",
                "fl": "timestamp,original,statuscode,mimetype,digest,length",
                "filter": "statuscode:200",
                "collapse": "digest",
            }
        )
        cdx_url = f"https://web.archive.org/cdx/search/cdx?{query}"
        try:
            payload = json.loads(fetch_text(cdx_url, timeout=60))
        except Exception as exc:
            records.append({"target": target, "error": str(exc)})
            continue
        if not isinstance(payload, list) or len(payload) < 2:
            records.append({"target": target, "captures": 0})
            continue
        header = payload[0]
        for raw in payload[1:]:
            row = dict(zip(header, raw))
            records.append(row)
            timestamp = row.get("timestamp")
            original = row.get("original")
            if timestamp and original:
                recovered.add(
                    f"https://web.archive.org/web/{timestamp}id_/{original}"
                )
    return recovered, records


def common_crawl_candidates(targets: Iterable[str]) -> tuple[list[bytes], list[dict[str, object]]]:
    """Return candidate response bodies recovered from recent Common Crawl indexes."""
    bodies: list[bytes] = []
    records: list[dict[str, object]] = []
    try:
        indexes = json.loads(fetch_text("https://index.commoncrawl.org/collinfo.json"))
    except Exception as exc:
        return bodies, [{"error": f"index discovery failed: {exc}"}]
    if not isinstance(indexes, list):
        return bodies, [{"error": "unexpected Common Crawl index response"}]
    # Search recent collections first; older collections cannot contain the May 2025 release.
    for index in indexes[:8]:
        api = index.get("cdx-api") if isinstance(index, dict) else None
        if not isinstance(api, str):
            continue
        for target in targets:
            query = urllib.parse.urlencode({"url": target, "output": "json"})
            try:
                text = fetch_text(f"{api}?{query}", timeout=60)
            except Exception as exc:
                records.append({"index": api, "target": target, "error": str(exc)})
                continue
            for line in text.splitlines():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                records.append(row)
                filename = row.get("filename")
                offset = row.get("offset")
                length = row.get("length")
                if not filename or offset is None or length is None:
                    continue
                try:
                    offset_i = int(offset)
                    length_i = int(length)
                    if length_i > MAX_ZIP_BYTES + 2 * 1024 * 1024:
                        continue
                    warc, _, _, _ = request(
                        "https://data.commoncrawl.org/" + filename,
                        max_bytes=length_i + 1,
                        headers={"Range": f"bytes={offset_i}-{offset_i + length_i - 1}"},
                        timeout=90,
                    )
                    if warc.startswith(b"\x1f\x8b"):
                        warc = gzip.decompress(warc)
                    split = warc.find(b"\r\n\r\n")
                    if split < 0:
                        continue
                    http_block = warc[split + 4 :]
                    split2 = http_block.find(b"\r\n\r\n")
                    if split2 < 0:
                        continue
                    body = http_block[split2 + 4 :]
                    # Handle a simple HTTP chunked transfer body when present.
                    if b"transfer-encoding: chunked" in http_block[:split2].lower():
                        decoded = bytearray()
                        cursor = 0
                        while cursor < len(body):
                            end = body.find(b"\r\n", cursor)
                            if end < 0:
                                break
                            size = int(body[cursor:end].split(b";", 1)[0], 16)
                            if size == 0:
                                break
                            cursor = end + 2
                            decoded.extend(body[cursor : cursor + size])
                            cursor += size + 2
                        body = bytes(decoded)
                    bodies.append(body)
                except Exception as exc:
                    records.append(
                        {
                            "index": api,
                            "target": target,
                            "warc_error": str(exc),
                        }
                    )
    return bodies, records


def probe_url(url: str, source: str) -> tuple[Probe, bytes | None]:
    try:
        data, status, final_url, headers = request(url, max_bytes=MAX_ZIP_BYTES)
        content_type = headers.get("content-type")
        valid, _, reason = valid_zip(data)
        outcome = "VALID_ZIP" if valid else f"NOT_ZIP: {reason}"
        probe = Probe(
            url=url,
            source=source,
            status=status,
            final_url=final_url,
            content_type=content_type,
            content_length=len(data),
            first_bytes_hex=data[:16].hex(),
            outcome=outcome,
        )
        return probe, data if valid else None
    except urllib.error.HTTPError as exc:
        return (
            Probe(
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
            Probe(
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


def archive_report(data: bytes, source_url: str) -> dict[str, object]:
    valid, members, reason = valid_zip(data)
    csv_reports = inspect_csvs(data) if valid else []
    row_match = [
        item
        for item in csv_reports
        if item["row_count_excluding_header"] == EXPECTED_ROWS
    ]
    return {
        "source_url": source_url,
        "byte_count": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "md5": hashlib.md5(data).hexdigest(),  # provenance compatibility only
        "zip_signature_hex": data[:4].hex(),
        "zip_crc_valid": valid,
        "zip_error": reason,
        "zip_members": members,
        "csv_members": csv_reports,
        "expected_data_rows": EXPECTED_ROWS,
        "matching_csv_members": [item["member"] for item in row_match],
        "schema_and_row_gate_passed": bool(row_match),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--skip-common-crawl", action="store_true")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    report: dict[str, object] = {
        "audit": "EDMOND_v6.01_2024_archive_recovery",
        "official_page": OFFICIAL_PAGE,
        "official_url": OFFICIAL_URL,
        "expected_rows": EXPECTED_ROWS,
        "frozen_scientific_solution_accessed": False,
        "candidate_membership_evaluated": False,
        "probes": [],
    }

    candidates: dict[str, str] = {
        OFFICIAL_URL: "official_page_link",
    }
    try:
        page = fetch_text(OFFICIAL_PAGE)
        report["official_page_sha256"] = hashlib.sha256(page.encode()).hexdigest()
        report["official_page_mentions_expected_rows"] = "13,513" in page
        for url in extract_urls_from_html(page, OFFICIAL_PAGE):
            if "2024" in url and url.lower().endswith(".zip"):
                candidates[url] = "official_page_html"
    except Exception as exc:
        report["official_page_error"] = f"{type(exc).__name__}: {exc}"

    for url in wordpress_candidates():
        if "2024" in url and ("edm" in url.lower() or url.lower().endswith(".zip")):
            candidates[url] = "wordpress_media_api"
    for url in plausible_candidates():
        candidates.setdefault(url, "plausible_site_path")

    # First probe only the official link and dynamically discovered media URLs.
    ordered = [OFFICIAL_URL] + sorted(
        url for url, source in candidates.items()
        if url != OFFICIAL_URL and source != "plausible_site_path"
    )
    # Then deterministic path guesses. This order keeps a recovered canonical
    # attachment ahead of archival copies or typo variants.
    ordered.extend(
        sorted(
            url for url, source in candidates.items()
            if source == "plausible_site_path" and url not in ordered
        )
    )

    archive: bytes | None = None
    archive_url: str | None = None
    for index, url in enumerate(ordered, 1):
        probe, data = probe_url(url, candidates[url])
        report["probes"].append(asdict(probe))
        if probe.status != 404:
            print(
                f"[{index}/{len(ordered)}] {probe.status} {probe.outcome} {url}",
                flush=True,
            )
        if data is not None:
            candidate_report = archive_report(data, url)
            if candidate_report["schema_and_row_gate_passed"]:
                archive = data
                archive_url = url
                report["accepted_archive"] = candidate_report
                break

    archival_targets = [OFFICIAL_URL]
    archival_urls, wayback_records = wayback_candidates(archival_targets)
    report["wayback_records"] = wayback_records
    if archive is None:
        for url in sorted(archival_urls):
            probe, data = probe_url(url, "wayback_capture")
            report["probes"].append(asdict(probe))
            print(f"[wayback] {probe.status} {probe.outcome} {url}", flush=True)
            if data is not None:
                candidate_report = archive_report(data, url)
                if candidate_report["schema_and_row_gate_passed"]:
                    archive = data
                    archive_url = url
                    report["accepted_archive"] = candidate_report
                    break

    if archive is None and not args.skip_common_crawl:
        bodies, cc_records = common_crawl_candidates(archival_targets)
        report["common_crawl_records"] = cc_records
        for idx, body in enumerate(bodies):
            candidate_report = archive_report(body, f"common_crawl_body_{idx}")
            if candidate_report["schema_and_row_gate_passed"]:
                archive = body
                archive_url = f"common_crawl_body_{idx}"
                report["accepted_archive"] = candidate_report
                break
    else:
        report["common_crawl_records"] = []

    # Always inventory the live 2023 file. It proves whether the official host
    # and expected annual-archive format are reachable in the same run.
    reference_probe, reference_data = probe_url(
        REFERENCE_2023_URL, "official_2023_reference"
    )
    report["reference_2023_probe"] = asdict(reference_probe)
    if reference_data is not None:
        reference_valid, reference_members, reference_error = valid_zip(reference_data)
        report["reference_2023"] = {
            "byte_count": len(reference_data),
            "sha256": hashlib.sha256(reference_data).hexdigest(),
            "zip_crc_valid": reference_valid,
            "zip_error": reference_error,
            "zip_members": reference_members,
            "csv_members": inspect_csvs(reference_data),
        }

    if archive is not None:
        archive_path = args.output_dir / "U2_2024_EDM.recovered.zip"
        archive_path.write_bytes(archive)
        report["verdict"] = "RECOVERED_SCHEMA_VERIFIED_ARCHIVE"
        report["accepted_archive_url"] = archive_url
        exit_code = 0
    else:
        report["verdict"] = "CLEAN_ACQUISITION_NEGATIVE_NO_VALID_2024_ARCHIVE"
        report["accepted_archive_url"] = None
        exit_code = 3

    report_path = args.output_dir / "current_edmond_recovery.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    summary = {
        "verdict": report["verdict"],
        "accepted_archive_url": report["accepted_archive_url"],
        "probes": len(report["probes"]),
        "live_2023_reference": reference_probe.outcome,
        "report": str(report_path),
    }
    print(json.dumps(summary, indent=2), flush=True)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
