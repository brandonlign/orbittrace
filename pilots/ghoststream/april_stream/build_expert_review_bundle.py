#!/usr/bin/env python3
"""Build a deterministic, code-inclusive GhostStream expert-review bundle.

The bundle contains the manuscript/MDC package, source and claim-boundary
records, the recovered immutable analysis implementation, exact clean-rerun
evidence, the historical and corrected method-control records, the recovered
blind-discovery lineage, and the CI entrypoints needed for external review.
Raw upstream catalogues remain external and are not silently repackaged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

BASE_FILES = [
    "pilots/ghoststream/RESULTS.md",
    "pilots/ghoststream/results/ghoststream_final_summary.json",
    "pilots/ghoststream/reproducibility_gap_summary.json",
    "pilots/ghoststream/recovery/CURRENT_RECOVERY_STATUS.md",
    "pilots/ghoststream/reconstruction/METHOD_CONTROL_RECONCILIATION.md",
    "pilots/ghoststream/reconstruction/blind_wrapper_fix.json",
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
    "pilots/ghoststream/april_stream/mdc/README.md",
    "pilots/ghoststream/april_stream/mdc/SUBMISSION_CHECKLIST.md",
    "pilots/ghoststream/april_stream/BOOTSTRAP_UNCERTAINTY.md",
    "pilots/ghoststream/april_stream/SPECIFICATION_CURVE.md",
    "pilots/ghoststream/april_stream/ACTIVITY_PROFILE.md",
    "pilots/ghoststream/april_stream/GEOGRAPHIC_SPLIT_VALIDATION.md",
    "pilots/ghoststream/april_stream/ALL_EXTERNAL_ZERO_SPEED.md",
    "pilots/ghoststream/april_stream/all_external_members_zero_speed.csv",
    "pilots/ghoststream/april_stream/shober_edmond/SHOBER_EDMOND_VALIDATION.md",
    "pilots/ghoststream/april_stream/edmond_2024/EDMOND_CURRENT_RELEASE_AUDIT.md",
]

TREE_ROOTS = [
    "pilots/ghoststream/recovered_pipeline",
    "pilots/ghoststream/reconstruction/exact_recovered",
    "pilots/ghoststream/reconstruction/exact_downstream",
    "pilots/ghoststream/reconstruction/exact_external",
    "pilots/ghoststream/reconstruction/exact_method_controls",
    "pilots/ghoststream/reconstruction/exact_method_controls_v3",
    "pilots/ghoststream/reconstruction/exact_blind_rediscovery",
]

CI_FILES = [
    ".github/workflows/ghoststream-primary-reproduction-pr.yml",
    ".github/workflows/ghoststream-recovered-downstream-reproduction.yml",
    ".github/workflows/ghoststream-recovered-external-reproduction.yml",
    ".github/workflows/ghoststream-method-controls-pr.yml",
    ".github/workflows/ghoststream-method-controls-v3.yml",
    ".github/workflows/ghoststream-blind-rediscovery-pr.yml",
    ".github/workflows/ghoststream-mdc-package-audit.yml",
    ".github/workflows/ghoststream-expert-review-bundle.yml",
    ".github/workflows/ghoststream-reproducibility-hold.yml",
]

FIXED_ZIP_TIME = (2026, 8, 1, 0, 0, 0)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def zip_write(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, data)


def collect_files() -> list[str]:
    paths = set(BASE_FILES + CI_FILES)
    for relative_root in TREE_ROOTS:
        tree = ROOT / relative_root
        if not tree.is_dir():
            raise FileNotFoundError(relative_root)
        for path in tree.rglob("*"):
            if path.is_file():
                paths.add(path.relative_to(ROOT).as_posix())
    return sorted(paths)


def bundle_path(relative: str) -> str:
    prefix = "pilots/ghoststream/"
    if relative.startswith(prefix):
        return relative.removeprefix(prefix)
    if relative.startswith(".github/workflows/"):
        return "ci/" + Path(relative).name
    return "repository/" + relative


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--commit-sha", required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, object]] = []
    payloads: list[tuple[str, bytes]] = []
    seen_bundle_paths: set[str] = set()
    for relative in collect_files():
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        data = path.read_bytes()
        name = bundle_path(relative)
        if name in seen_bundle_paths:
            raise RuntimeError(f"duplicate bundle path: {name}")
        seen_bundle_paths.add(name)
        payloads.append((name, data))
        records.append(
            {
                "source_path": relative,
                "bundle_path": name,
                "byte_count": len(data),
                "sha256": sha256(data),
            }
        )

    required_bundle_paths = {
        "april_stream/EXPERT_REVIEW_PACKET.md",
        "april_stream/mdc/MANUSCRIPT_DRAFT.md",
        "april_stream/mdc/GhostStream_April_95_GMN_lookup.csv",
        "recovered_pipeline/SOURCE_MANIFEST.json",
        "recovered_pipeline/pr57_novel/validate_april_candidate.py",
        "reconstruction/exact_recovered/exact_reproduction.json",
        "reconstruction/exact_downstream/downstream_reproduction.json",
        "reconstruction/exact_external/external_reproduction.json",
        "reconstruction/exact_method_controls/method_controls.json",
        "reconstruction/exact_method_controls_v3/method_controls_v3.json",
        "reconstruction/exact_blind_rediscovery/blind_rediscovery.json",
        "reconstruction/METHOD_CONTROL_RECONCILIATION.md",
        "reconstruction/blind_wrapper_fix.json",
        "ci/ghoststream-primary-reproduction-pr.yml",
        "ci/ghoststream-recovered-downstream-reproduction.yml",
        "ci/ghoststream-recovered-external-reproduction.yml",
        "ci/ghoststream-method-controls-v3.yml",
        "ci/ghoststream-blind-rediscovery-pr.yml",
    }
    missing = sorted(required_bundle_paths - seen_bundle_paths)
    if missing:
        raise RuntimeError(f"required bundle files missing: {missing}")

    readme = f"""# GhostStream external expert review bundle

Branch commit: `{args.commit_sha}`
Prepared: 2026-08-01 UTC
Included repository files: {len(records)}

## Recovery and reproducibility status

The original executable GhostStream analysis survived in immutable temporary
runner commits and is included under `recovered_pipeline/` with file-level
SHA-256 provenance. The unchanged recovered primary validator exactly
regenerated 101 selected GMN events, including the preserved 95-event
2022–2026 lookup. The recovered internal downstream and CAMS/SonotaCo/JPL
stages were also rerun and their complete outputs are included under
`reconstruction/`.

The package preserves both the historical v2 method-control no-go and the
prospective corrected 2024 holdout pass. It also includes the actual recovered
January–July 2026 blind-discovery lineage and the minimal wrapper-repair record;
the original recovered wrapper remains preserved unchanged.

This resolves the prior code-loss and analysis-rerun gap. It does not replace
external meteor-science review, make the shower official, or make the current
draft automatically suitable for submission.

## Suggested reading order

1. `april_stream/EXPERT_REVIEW_PACKET.md`
2. `april_stream/mdc/MANUSCRIPT_DRAFT.md`
3. `results/ghoststream_final_summary.json`
4. `reconstruction/exact_blind_rediscovery/BLIND_REDISCOVERY.md`
5. `reconstruction/METHOD_CONTROL_RECONCILIATION.md`
6. `reconstruction/exact_recovered/EXACT_REPRODUCTION.md`
7. `reconstruction/exact_downstream/DOWNSTREAM_REPRODUCTION.md`
8. `reconstruction/exact_external/EXTERNAL_REPRODUCTION.md`
9. `recovered_pipeline/SOURCE_MANIFEST.json`
10. `april_stream/mdc/MDC_PACKAGE_CONSISTENCY_AUDIT.md`
11. source and robustness records as needed

## Requested outcome

Please return a critical verdict using the A–E scale in
`april_stream/EXPERT_REVIEW_PACKET.md`, identify any fatal error or likely
known-shower duplicate, and state the required work before a possible IAU
Meteor Data Center submission.

## AI/software transparency

The package discloses substantive generative-AI assistance with research
planning, code development, source discovery, auditing, organization, and
manuscript preparation. AI tools were not treated as authors or independent
scientific reviewers. Reviewers should consider whether the documented
verification and human-responsibility controls are adequate.

## Input-data boundary

Upstream GMN, CAMS, SonotaCo, EDMOND, IAU MDC, and JPL catalogues are not
silently redistributed in this ZIP. The included source records their public
acquisition paths and the exact clean runs record the resulting selected and
audit tables. Raw monthly GMN bytes were not vendored as a complete immutable
archive, so long-term source-byte preservation remains a disclosed limitation.

## Claim boundary

This is a draft pre-submission research package. The candidate is not an
official IAU discovery, an established shower, a named shower, a demonstrated
parent-body association, a complete EDMOND v6.01 replication, or a completed
external scientific review.

## Integrity

`MANIFEST.json` records the source path, bundle path, byte count, and SHA-256
of every included file. The ZIP is deterministic for the same inputs and
commit identifier.
""".encode("utf-8")

    manifest = {
        "bundle": "GhostStream external expert review",
        "prepared_utc": "2026-08-01T00:00:00Z",
        "source_commit": args.commit_sha,
        "file_count": len(records),
        "required_bundle_paths": sorted(required_bundle_paths),
        "files": records,
        "reproducibility_status": "source_recovered_primary_internal_external_method_and_blind_evidence_complete",
        "claim_boundary": (
            "Draft pre-submission package; not official IAU recognition, an "
            "established shower, a complete EDMOND v6.01 replication, or a "
            "completed external scientific review."
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
        "verdict": "PASS_CODE_INCLUSIVE_EXPERT_REVIEW_BUNDLE_BUILT",
        "source_commit": args.commit_sha,
        "included_files": len(records),
        "zip_members": 2 + len(records),
        "zip_byte_count": output.stat().st_size,
        "zip_sha256": sha256(output.read_bytes()),
        "required_paths_present": True,
        "output": str(output),
    }
    (args.output_dir / "expert_review_bundle_build.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
