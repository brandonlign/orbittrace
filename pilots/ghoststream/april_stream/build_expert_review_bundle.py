#!/usr/bin/env python3
"""Build a deterministic, bounded GhostStream expert-review bundle.

The bundle contains the primary manuscript/data package, the frozen scientific
record, the AI/software provenance disclosure, and the minimum robustness
reports needed for an external meteor expert to issue a critical verdict. It
excludes raw catalogues, temporary workflows, and internal development logs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

FILES = [
    "pilots/ghoststream/april_stream/EXPERT_REVIEW_PACKET.md",
    "pilots/ghoststream/april_stream/CANDIDATE_DOSSIER.md",
    "pilots/ghoststream/april_stream/candidate_solution.json",
    "pilots/ghoststream/april_stream/mdc/MANUSCRIPT_DRAFT.md",
    "pilots/ghoststream/april_stream/mdc/GhostStream_April_95_GMN_lookup.csv",
    "pilots/ghoststream/april_stream/mdc/GhostStream_April_mean_submission.json",
    "pilots/ghoststream/april_stream/mdc/GhostStream_April_mean_legacy.txt",
    "pilots/ghoststream/april_stream/mdc/calculation_audit.json",
    "pilots/ghoststream/april_stream/mdc/MDC_OFFICIAL_CHECKER_REPORT.md",
    "pilots/ghoststream/april_stream/mdc/exact_official_checker_summary.json",
    "pilots/ghoststream/april_stream/mdc/LIVE_MDC_NOVELTY_REFRESH.md",
    "pilots/ghoststream/april_stream/mdc/live_mdc_novelty_refresh_summary.json",
    "pilots/ghoststream/april_stream/mdc/MDC_PACKAGE_CONSISTENCY_AUDIT.md",
    "pilots/ghoststream/april_stream/mdc/mdc_package_consistency_summary.json",
    "pilots/ghoststream/april_stream/mdc/AI_AND_SOFTWARE_PROVENANCE.md",
    "pilots/ghoststream/april_stream/BOOTSTRAP_UNCERTAINTY.md",
    "pilots/ghoststream/april_stream/SPECIFICATION_CURVE.md",
    "pilots/ghoststream/april_stream/ACTIVITY_PROFILE.md",
    "pilots/ghoststream/april_stream/GEOGRAPHIC_SPLIT_VALIDATION.md",
    "pilots/ghoststream/april_stream/ALL_EXTERNAL_ZERO_SPEED.md",
    "pilots/ghoststream/april_stream/all_external_members_zero_speed.csv",
    "pilots/ghoststream/april_stream/shober_edmond/SHOBER_EDMOND_VALIDATION.md",
    "pilots/ghoststream/april_stream/edmond_2024/EDMOND_CURRENT_RELEASE_AUDIT.md",
]

FIXED_ZIP_TIME = (2026, 8, 1, 0, 0, 0)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def zip_write(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--commit-sha", required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []
    payloads: list[tuple[str, bytes]] = []
    for relative in FILES:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        data = path.read_bytes()
        bundle_name = relative.removeprefix("pilots/ghoststream/april_stream/")
        payloads.append((bundle_name, data))
        records.append(
            {
                "source_path": relative,
                "bundle_path": bundle_name,
                "byte_count": len(data),
                "sha256": sha256(data),
            }
        )

    readme = f"""# GhostStream external expert review bundle

Branch commit: `{args.commit_sha}`
Prepared: 2026-08-01 UTC
Files: {len(records)}

## Suggested reading order

1. `EXPERT_REVIEW_PACKET.md`
2. `mdc/MANUSCRIPT_DRAFT.md`
3. `mdc/AI_AND_SOFTWARE_PROVENANCE.md`
4. `mdc/GhostStream_April_95_GMN_lookup.csv`
5. `mdc/GhostStream_April_mean_submission.json`
6. `mdc/calculation_audit.json`
7. `mdc/LIVE_MDC_NOVELTY_REFRESH.md`
8. `mdc/MDC_PACKAGE_CONSISTENCY_AUDIT.md`
9. `candidate_solution.json`
10. robustness and external-archive reports as needed

## Requested outcome

Please return a critical verdict using the A–E scale in `EXPERT_REVIEW_PACKET.md`, identify any fatal error or likely known-shower duplicate, and state the required work before a possible IAU Meteor Data Center submission.

## AI/software transparency

The package discloses substantive generative-AI assistance with research planning, code development, source discovery, auditing, organization, and manuscript preparation. AI tools were not treated as authors or independent scientific reviewers. Reviewers should consider whether the documented verification and human-responsibility controls are adequate.

## Claim boundary

This is a draft pre-submission research package. The candidate is not an official IAU discovery, an established shower, a named shower, or a demonstrated parent-body association. Mechanical validation does not replace scientific review.

## Integrity

`MANIFEST.json` records the source path, bundle path, byte count, and SHA-256 of every included file. The ZIP is deterministic for the same inputs and commit identifier.
""".encode("utf-8")

    manifest = {
        "bundle": "GhostStream external expert review",
        "prepared_utc": "2026-08-01T00:00:00Z",
        "source_commit": args.commit_sha,
        "file_count": len(records),
        "files": records,
        "claim_boundary": (
            "Draft pre-submission package; not official IAU recognition, an "
            "established shower, or a completed external scientific review."
        ),
    }
    manifest_data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")

    output = args.output_dir / "GhostStream_Expert_Review_Bundle.zip"
    with zipfile.ZipFile(output, "w") as archive:
        zip_write(archive, "README.md", readme)
        zip_write(archive, "MANIFEST.json", manifest_data)
        for name, data in sorted(payloads):
            zip_write(archive, name, data)

    with zipfile.ZipFile(output) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise RuntimeError(f"ZIP CRC failure in {bad}")
        names = archive.namelist()
        expected = 2 + len(records)
        if len(names) != expected:
            raise RuntimeError(f"expected {expected} ZIP members, found {len(names)}")

    result = {
        "verdict": "PASS_EXPERT_REVIEW_BUNDLE_BUILT",
        "source_commit": args.commit_sha,
        "included_files": len(records),
        "zip_members": 2 + len(records),
        "zip_byte_count": output.stat().st_size,
        "zip_sha256": sha256(output.read_bytes()),
        "output": str(output),
    }
    (args.output_dir / "expert_review_bundle_build.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
