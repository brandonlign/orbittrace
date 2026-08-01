#!/usr/bin/env python3
"""Extend the historical MDC consistency audit with recovered-code evidence.

The base audit recomputes the 95-row submission record and checks the manuscript,
MDC files, live novelty evidence, and EDMOND claim boundary. This wrapper runs
that audit unchanged, then adds fail-closed checks for the recovered source,
exact primary reproduction, internal downstream rerun, external archive rerun,
current parent screen, and the publication-hold state.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
MDC = ROOT / "pilots/ghoststream/april_stream/mdc"
BASE_AUDIT = MDC / "audit_mdc_package_consistency.py"

SOURCE_MANIFEST = ROOT / "pilots/ghoststream/recovered_pipeline/SOURCE_MANIFEST.json"
EXACT_PRIMARY = ROOT / "pilots/ghoststream/reconstruction/exact_recovered/exact_reproduction.json"
EXACT_DOWNSTREAM = ROOT / "pilots/ghoststream/reconstruction/exact_downstream/downstream_reproduction.json"
EXACT_EXTERNAL = ROOT / "pilots/ghoststream/reconstruction/exact_external/external_reproduction.json"
FINAL = ROOT / "pilots/ghoststream/results/ghoststream_final_summary.json"
GAP = ROOT / "pilots/ghoststream/reproducibility_gap_summary.json"
RECOVERY_STATUS = ROOT / "pilots/ghoststream/recovery/CURRENT_RECOVERY_STATUS.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_check(name: str, passed: bool, observed: Any, expected: Any, note: str | None = None) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "observed": observed,
        "expected": expected,
        "tolerance": None,
        "note": note,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    completed = subprocess.run(
        [sys.executable, str(BASE_AUDIT), "--output-dir", str(args.output_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)

    base_json = args.output_dir / "mdc_package_consistency_audit.json"
    if not base_json.is_file():
        raise RuntimeError("base package audit did not produce its JSON report")
    report = load_json(base_json)

    source = load_json(SOURCE_MANIFEST)
    primary = load_json(EXACT_PRIMARY)
    downstream = load_json(EXACT_DOWNSTREAM)
    external = load_json(EXACT_EXTERNAL)
    final = load_json(FINAL)
    gap = load_json(GAP)

    extra: list[dict[str, Any]] = []
    extra.append(make_check(
        "recovered source manifest status",
        source.get("status") == "RECOVERED_FROM_IMMUTABLE_GITHUB_PR_COMMITS",
        source.get("status"),
        "RECOVERED_FROM_IMMUTABLE_GITHUB_PR_COMMITS",
    ))
    source_counts = {
        "pr56_runner": source["sources"]["pr56_runner"]["file_count"],
        "pr57_novel": source["sources"]["pr57_novel"]["file_count"],
    }
    extra.append(make_check("recovered source file counts", source_counts == {"pr56_runner": 13, "pr57_novel": 35}, source_counts, {"pr56_runner": 13, "pr57_novel": 35}))
    source_commits = {
        "pr56_runner": source["sources"]["pr56_runner"]["commit"],
        "pr57_novel": source["sources"]["pr57_novel"]["commit"],
    }
    extra.append(make_check(
        "recovered source immutable commits",
        source_commits == {
            "pr56_runner": "4175e5187fcc6faf3d1befb099a9e35be96850f2",
            "pr57_novel": "39972b5fe0cf4d47092d3caa2b3ced12bedb065e",
        },
        source_commits,
        {
            "pr56_runner": "4175e5187fcc6faf3d1befb099a9e35be96850f2",
            "pr57_novel": "39972b5fe0cf4d47092d3caa2b3ced12bedb065e",
        },
    ))

    extra.append(make_check("exact primary verdict", primary.get("status") == "EXACT_REPRODUCTION", primary.get("status"), "EXACT_REPRODUCTION"))
    extra.append(make_check("exact primary total", primary.get("total_members") == 101, primary.get("total_members"), 101))
    extra.append(make_check("exact primary preserved lookup", primary.get("preserved_95_exact") is True, primary.get("preserved_95_exact"), True))
    extra.append(make_check(
        "exact primary timestamp discrepancy",
        primary.get("missing_preserved_timestamps") == [] and primary.get("additional_timestamps") == [],
        {
            "missing": primary.get("missing_preserved_timestamps"),
            "additional": primary.get("additional_timestamps"),
        },
        {"missing": [], "additional": []},
    ))

    downstream_checks = downstream["checks"]
    extra.append(make_check("exact downstream verdict", downstream.get("status") == "EXACT_RECOVERED_DOWNSTREAM_REPRODUCTION", downstream.get("status"), "EXACT_RECOVERED_DOWNSTREAM_REPRODUCTION"))
    extra.append(make_check(
        "exact downstream source-preserving null",
        downstream_checks["source_preserving_null"]["verdict"] == "APRIL_STREAM_SURVIVES_SOURCE_PRESERVING_NULL",
        downstream_checks["source_preserving_null"]["verdict"],
        "APRIL_STREAM_SURVIVES_SOURCE_PRESERVING_NULL",
    ))
    extra.append(make_check(
        "exact downstream bootstrap",
        downstream_checks["cluster_bootstrap"]["members"] == 95
        and downstream_checks["cluster_bootstrap"]["nights"] == 29
        and downstream_checks["cluster_bootstrap"]["replicates_each"] == 20000,
        downstream_checks["cluster_bootstrap"],
        {"members": 95, "nights": 29, "replicates_each": 20000},
    ))
    extra.append(make_check(
        "exact downstream geographic member counts",
        downstream_checks["geographic_replication"]["members"] == {
            "Americas": 30,
            "Europe_WestAsia": 22,
            "Oceania_EastAsia_Africa": 44,
        },
        downstream_checks["geographic_replication"]["members"],
        {"Americas": 30, "Europe_WestAsia": 22, "Oceania_EastAsia_Africa": 44},
    ))
    extra.append(make_check(
        "exact downstream specification curve",
        downstream_checks["specification_curve"]["eligible_cells"] == 81
        and downstream_checks["specification_curve"]["passing_cells"] == 81,
        {
            "eligible": downstream_checks["specification_curve"]["eligible_cells"],
            "passing": downstream_checks["specification_curve"]["passing_cells"],
        },
        {"eligible": 81, "passing": 81},
    ))

    external_checks = external["checks"]
    extra.append(make_check("exact external verdict", external.get("status") == "RECOVERED_EXTERNAL_ARCHIVE_REPRODUCTION", external.get("status"), "RECOVERED_EXTERNAL_ARCHIVE_REPRODUCTION"))
    extra.append(make_check("exact external CAMS members", external_checks["cams"]["members"] == 6, external_checks["cams"]["members"], 6))
    extra.append(make_check("exact external SonotaCo members", external_checks["sonotaco"]["members"] == 4, external_checks["sonotaco"]["members"], 4))
    pooled = external_checks["exploratory_pooled_synthesis"]
    extra.append(make_check(
        "exact external pooled member set",
        pooled["members"] == 10 and pooled["member_id_set_exact"] is True,
        {"members": pooled["members"], "member_id_set_exact": pooled["member_id_set_exact"]},
        {"members": 10, "member_id_set_exact": True},
    ))
    parent = external_checks["current_parent_screen"]
    extra.append(make_check(
        "current parent screen boundary",
        parent["valid_orbits"] == 729 and parent["d_le_0_15"] == 0,
        {"valid_orbits": parent["valid_orbits"], "d_le_0_15": parent["d_le_0_15"]},
        {"valid_orbits": 729, "d_le_0_15": 0},
        "Live JPL catalogue result; no parent body is claimed.",
    ))

    repro = final["reproducibility_status"]
    extra.append(make_check(
        "final summary recovered analysis state",
        repro["core_gmn_analysis_code_committed"] is True
        and repro["exact_primary_clean_rerun_completed"] is True
        and repro["internal_downstream_clean_rerun_status"] == "passed"
        and repro["external_archive_clean_rerun_status"] == "passed"
        and repro["analysis_chain_clean_rerun_completed"] is True,
        repro,
        "recovered source plus primary/internal/external reruns passed",
    ))
    extra.append(make_check(
        "final summary submission hold",
        repro["publication_or_formal_mdc_submission_allowed"] is False
        and repro["end_to_end_clean_rerun_completed"] is False,
        {
            "publication_or_formal_mdc_submission_allowed": repro["publication_or_formal_mdc_submission_allowed"],
            "end_to_end_clean_rerun_completed": repro["end_to_end_clean_rerun_completed"],
        },
        {
            "publication_or_formal_mdc_submission_allowed": False,
            "end_to_end_clean_rerun_completed": False,
        },
        "The analysis chain is reproduced, but the submission package still requires rebuild and external review.",
    ))
    extra.append(make_check(
        "reproducibility gap current verdict",
        gap.get("verdict") == "COMPUTATIONAL_RECOVERY_AND_ANALYSIS_RERUNS_COMPLETE_PACKAGE_REVIEW_PENDING",
        gap.get("verdict"),
        "COMPUTATIONAL_RECOVERY_AND_ANALYSIS_RERUNS_COMPLETE_PACKAGE_REVIEW_PENDING",
    ))
    extra.append(make_check(
        "human-readable recovery status",
        "Internal GMN downstream clean rerun: **passed and committed**" in RECOVERY_STATUS.read_text()
        and "External CAMS/SonotaCo clean rerun: **passed and committed**" in RECOVERY_STATUS.read_text(),
        "recovery status phrases",
        "both clean reruns passed and committed",
    ))

    report["checks"].extend(extra)
    report["check_count"] = len(report["checks"])
    report["failed_checks"] = sum(1 for item in report["checks"] if not item["passed"])
    report["passed_checks"] = report["check_count"] - report["failed_checks"]
    report["verdict"] = "PASS_RECOVERED_MDC_PACKAGE_INTERNALLY_CONSISTENT" if report["failed_checks"] == 0 else "FAIL_RECOVERED_MDC_PACKAGE_INCONSISTENT"
    report["recovered_analysis"] = {
        "source_manifest": str(SOURCE_MANIFEST.relative_to(ROOT)),
        "exact_primary": str(EXACT_PRIMARY.relative_to(ROOT)),
        "exact_downstream": str(EXACT_DOWNSTREAM.relative_to(ROOT)),
        "exact_external": str(EXACT_EXTERNAL.relative_to(ROOT)),
        "analysis_chain_clean_rerun_completed": repro["analysis_chain_clean_rerun_completed"],
        "submission_allowed": repro["publication_or_formal_mdc_submission_allowed"],
    }

    for path in [SOURCE_MANIFEST, EXACT_PRIMARY, EXACT_DOWNSTREAM, EXACT_EXTERNAL, GAP, RECOVERY_STATUS]:
        report["manifest"][str(path.relative_to(ROOT))] = {
            "byte_count": path.stat().st_size,
            "sha256": sha256(path),
        }

    base_json.write_text(json.dumps(report, indent=2) + "\n")

    failed = [item for item in report["checks"] if not item["passed"]]
    lines = [
        "# GhostStream recovered MDC package consistency audit",
        "",
        f"**Verdict:** `{report['verdict']}`",
        "",
        f"- Checks: **{report['check_count']}**",
        f"- Passed: **{report['passed_checks']}**",
        f"- Failed: **{report['failed_checks']}**",
        f"- Lookup rows: **{report['lookup_rows']}**",
        "",
        "## Recovered analysis evidence",
        "",
        "- immutable recovered source snapshots: 13 + 35 files",
        "- exact primary reproduction: 101 total events and exact 95-event lookup",
        "- exact internal downstream reproduction: source null, 20,000-replicate bootstrap, activity profile, three geographic groups, and 81/81 specification cells",
        "- recovered external reproduction: 6 CAMS + 4 SonotaCo events, exact 10-event pooled ID set, and current JPL screen",
        "- publication/formal MDC submission remains blocked pending package completion and independent review",
        "",
    ]
    if failed:
        lines.extend(["## Failures", ""])
        for item in failed:
            lines.append(f"- **{item['name']}** — observed `{item['observed']}`, expected `{item['expected']}`")
        lines.append("")
    lines.extend([
        "## Package manifest",
        "",
        "| File | Bytes | SHA-256 |",
        "|---|---:|---|",
    ])
    for name, values in sorted(report["manifest"].items()):
        lines.append(f"| `{name}` | {values['byte_count']} | `{values['sha256']}` |")
    lines.extend([
        "",
        "## Claim boundary",
        "",
        "This audit establishes internal consistency between the draft MDC package and the recovered computational evidence. It does not constitute IAU submission, official recognition, independent scientific review, a complete EDMOND v6.01 replication, or parent-body identification.",
        "",
    ])
    (args.output_dir / "MDC_PACKAGE_CONSISTENCY_AUDIT.md").write_text("\n".join(lines))

    print(json.dumps({
        "verdict": report["verdict"],
        "check_count": report["check_count"],
        "passed_checks": report["passed_checks"],
        "failed_checks": report["failed_checks"],
        "failure_names": [item["name"] for item in failed],
    }, indent=2))
    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
