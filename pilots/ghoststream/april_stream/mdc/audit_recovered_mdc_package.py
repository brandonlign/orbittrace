#!/usr/bin/env python3
"""Extend the MDC consistency audit with final recovered evidence.

The historical audit recomputes the 95-row submission record and checks the
manuscript, MDC files, live novelty evidence, and EDMOND claim boundary. This
wrapper runs it unchanged, then fail-closes on the recovered source, exact
primary/internal/external reruns, the historical method-control no-go, the
prospective corrected holdout, the January–July 2026 blind discovery lineage,
the minimal wrapper repair, and the publication hold.
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
METHOD_ORIGINAL = ROOT / "pilots/ghoststream/reconstruction/exact_method_controls/method_controls.json"
METHOD_V3 = ROOT / "pilots/ghoststream/reconstruction/exact_method_controls_v3/method_controls_v3.json"
BLIND = ROOT / "pilots/ghoststream/reconstruction/exact_blind_rediscovery/blind_rediscovery.json"
WRAPPER_FIX = ROOT / "pilots/ghoststream/reconstruction/blind_wrapper_fix.json"
WRAPPER_REPAIRED = ROOT / "pilots/ghoststream/reconstruction/blind_wrapper_repaired/run_month_year_v3.py"
FINAL = ROOT / "pilots/ghoststream/results/ghoststream_final_summary.json"
CANDIDATE = ROOT / "pilots/ghoststream/april_stream/candidate_solution.json"
GAP = ROOT / "pilots/ghoststream/reproducibility_gap_summary.json"
RECOVERY_STATUS = ROOT / "pilots/ghoststream/recovery/CURRENT_RECOVERY_STATUS.md"
METHOD_RECONCILIATION = ROOT / "pilots/ghoststream/reconstruction/METHOD_CONTROL_RECONCILIATION.md"

EXPECTED_GAP = "COMPUTATIONAL_RECOVERY_AND_DISCOVERY_LINEAGE_COMPLETE_REVIEW_PENDING"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, passed: bool, observed: Any, expected: Any, note: str | None = None) -> dict[str, Any]:
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
    method_original = load_json(METHOD_ORIGINAL)
    method_v3 = load_json(METHOD_V3)
    blind = load_json(BLIND)
    wrapper = load_json(WRAPPER_FIX)
    final = load_json(FINAL)
    candidate = load_json(CANDIDATE)
    gap = load_json(GAP)

    extra: list[dict[str, Any]] = []

    counts = {
        "pr56_runner": source["sources"]["pr56_runner"]["file_count"],
        "pr57_novel": source["sources"]["pr57_novel"]["file_count"],
    }
    commits = {
        "pr56_runner": source["sources"]["pr56_runner"]["commit"],
        "pr57_novel": source["sources"]["pr57_novel"]["commit"],
    }
    extra.extend([
        check("recovered source manifest status", source.get("status") == "RECOVERED_FROM_IMMUTABLE_GITHUB_PR_COMMITS", source.get("status"), "RECOVERED_FROM_IMMUTABLE_GITHUB_PR_COMMITS"),
        check("recovered source file counts", counts == {"pr56_runner": 13, "pr57_novel": 35}, counts, {"pr56_runner": 13, "pr57_novel": 35}),
        check(
            "recovered source immutable commits",
            commits == {
                "pr56_runner": "4175e5187fcc6faf3d1befb099a9e35be96850f2",
                "pr57_novel": "39972b5fe0cf4d47092d3caa2b3ced12bedb065e",
            },
            commits,
            {
                "pr56_runner": "4175e5187fcc6faf3d1befb099a9e35be96850f2",
                "pr57_novel": "39972b5fe0cf4d47092d3caa2b3ced12bedb065e",
            },
        ),
        check("exact primary verdict", primary.get("status") == "EXACT_REPRODUCTION", primary.get("status"), "EXACT_REPRODUCTION"),
        check("exact primary total", primary.get("total_members") == 101, primary.get("total_members"), 101),
        check("exact primary preserved lookup", primary.get("preserved_95_exact") is True, primary.get("preserved_95_exact"), True),
        check(
            "exact primary timestamp discrepancy",
            primary.get("missing_preserved_timestamps") == [] and primary.get("additional_timestamps") == [],
            {"missing": primary.get("missing_preserved_timestamps"), "additional": primary.get("additional_timestamps")},
            {"missing": [], "additional": []},
        ),
    ])

    dc = downstream["checks"]
    extra.extend([
        check("exact downstream verdict", downstream.get("status") == "EXACT_RECOVERED_DOWNSTREAM_REPRODUCTION", downstream.get("status"), "EXACT_RECOVERED_DOWNSTREAM_REPRODUCTION"),
        check("exact downstream source-preserving null", dc["source_preserving_null"]["verdict"] == "APRIL_STREAM_SURVIVES_SOURCE_PRESERVING_NULL", dc["source_preserving_null"]["verdict"], "APRIL_STREAM_SURVIVES_SOURCE_PRESERVING_NULL"),
        check(
            "exact downstream bootstrap",
            dc["cluster_bootstrap"]["members"] == 95 and dc["cluster_bootstrap"]["nights"] == 29 and dc["cluster_bootstrap"]["replicates_each"] == 20000,
            dc["cluster_bootstrap"],
            {"members": 95, "nights": 29, "replicates_each": 20000},
        ),
        check(
            "exact downstream geographic member counts",
            dc["geographic_replication"]["members"] == {"Americas": 30, "Europe_WestAsia": 22, "Oceania_EastAsia_Africa": 44},
            dc["geographic_replication"]["members"],
            {"Americas": 30, "Europe_WestAsia": 22, "Oceania_EastAsia_Africa": 44},
        ),
        check(
            "exact downstream specification curve",
            dc["specification_curve"]["eligible_cells"] == 81 and dc["specification_curve"]["passing_cells"] == 81,
            {"eligible": dc["specification_curve"]["eligible_cells"], "passing": dc["specification_curve"]["passing_cells"]},
            {"eligible": 81, "passing": 81},
        ),
    ])

    ec = external["checks"]
    pooled = ec["exploratory_pooled_synthesis"]
    parent = ec["current_parent_screen"]
    extra.extend([
        check("exact external verdict", external.get("status") == "RECOVERED_EXTERNAL_ARCHIVE_REPRODUCTION", external.get("status"), "RECOVERED_EXTERNAL_ARCHIVE_REPRODUCTION"),
        check("exact external CAMS members", ec["cams"]["members"] == 6, ec["cams"]["members"], 6),
        check("exact external SonotaCo members", ec["sonotaco"]["members"] == 4, ec["sonotaco"]["members"], 4),
        check("exact external pooled member set", pooled["members"] == 10 and pooled["member_id_set_exact"] is True, {"members": pooled["members"], "member_id_set_exact": pooled["member_id_set_exact"]}, {"members": 10, "member_id_set_exact": True}),
        check("current parent screen boundary", parent["valid_orbits"] == 729 and parent["d_le_0_15"] == 0, {"valid_orbits": parent["valid_orbits"], "d_le_0_15": parent["d_le_0_15"]}, {"valid_orbits": 729, "d_le_0_15": 0}, "Live JPL result; no parent body is claimed."),
    ])

    original_gate = method_original["known_shower_recovery"]
    injection = method_original["weak_stream_injection"]
    extra.extend([
        check("historical method-control audit status", method_original.get("status") == "RECOVERED_METHOD_CONTROL_AUDIT_NEGATIVE_GATE_INFEASIBLE", method_original.get("status"), "RECOVERED_METHOD_CONTROL_AUDIT_NEGATIVE_GATE_INFEASIBLE"),
        check("historical v2 no-go preserved", original_gate["original_verdict"] == "NO_GO_DEGENERATE_PARENT_CLUSTER" and method_original["scientific_gate_passed"] is False, {"verdict": original_gate["original_verdict"], "scientific_gate_passed": method_original["scientific_gate_passed"]}, {"verdict": "NO_GO_DEGENERATE_PARENT_CLUSTER", "scientific_gate_passed": False}),
        check("historical named showers recovered", original_gate["untouched_recovered"] == 3 and original_gate["untouched_eligible"] == 3, {"recovered": original_gate["untouched_recovered"], "eligible": original_gate["untouched_eligible"]}, {"recovered": 3, "eligible": 3}),
        check("historical injection gate", injection["verdict"] == "INJECTION_GATE_PASS", injection["verdict"], "INJECTION_GATE_PASS"),
        check("corrected method-control verdict", method_v3.get("status") == "CORRECTED_INDEPENDENT_YEAR_CONTROL_PASS" and method_v3.get("passed") is True, {"status": method_v3.get("status"), "passed": method_v3.get("passed")}, {"status": "CORRECTED_INDEPENDENT_YEAR_CONTROL_PASS", "passed": True}),
        check("corrected method-control frozen holdout", method_v3["correction_frozen_before_2024_holdout_run"] is True and method_v3["recovered_controls"] == 3 and method_v3["non_target_degeneracy_passes"] == 3, {"frozen": method_v3["correction_frozen_before_2024_holdout_run"], "recovered": method_v3["recovered_controls"], "non_target_passes": method_v3["non_target_degeneracy_passes"]}, {"frozen": True, "recovered": 3, "non_target_passes": 3}),
        check("corrected method-control ceiling", method_v3["corrected_pass_rule"]["maximum_largest_non_target_cluster_fraction"] == 0.30, method_v3["corrected_pass_rule"]["maximum_largest_non_target_cluster_fraction"], 0.30),
    ])

    april = blind["april_survivor"]
    extra.extend([
        check("blind discovery verdict", blind.get("status") == "EXACT_2026_BLIND_REDISCOVERY", blind.get("status"), "EXACT_2026_BLIND_REDISCOVERY"),
        check("blind discovery matrix", blind["months_scanned"] == [1, 2, 3, 4, 5, 6, 7] and blind["validation_years"] == [2025, 2024], {"months": blind["months_scanned"], "validation_years": blind["validation_years"]}, {"months": [1, 2, 3, 4, 5, 6, 7], "validation_years": [2025, 2024]}),
        check("blind discovery unique survivor", blind["full_gate_survivors_across_matrix"] == 1 and blind["additional_non_april_survivors"] == [], {"survivors": blind["full_gate_survivors_across_matrix"], "additional": blind["additional_non_april_survivors"]}, {"survivors": 1, "additional": []}),
        check("blind discovery validation", april["validation"]["2025"]["passed"] is True and april["validation"]["2024"]["passed"] is True and april["validation"]["2025"]["members"] == 36 and april["validation"]["2024"]["members"] == 14, {"2025": april["validation"]["2025"], "2024": april["validation"]["2024"]}, {"2025_members": 36, "2024_members": 14, "both_passed": True}),
        check("blind discovery clone stability", april["clone_stability"]["passed"] is True and april["clone_stability"]["pass_fraction"] == 1.0, april["clone_stability"], {"passed": True, "pass_fraction": 1.0}),
        check("blind discovery automated IAU veto", april["nearest_iau"]["matched"] is False, april["nearest_iau"]["matched"], False),
        check("blind wrapper repair record", wrapper["status"] == "MINIMAL_RECOVERED_WRAPPER_REPAIR" and wrapper["scientific_logic_changed"] is False, {"status": wrapper["status"], "scientific_logic_changed": wrapper["scientific_logic_changed"]}, {"status": "MINIMAL_RECOVERED_WRAPPER_REPAIR", "scientific_logic_changed": False}),
        check("blind repaired wrapper hash", sha256(WRAPPER_REPAIRED) == blind["wrapper_repair"]["repaired_wrapper_sha256"], sha256(WRAPPER_REPAIRED), blind["wrapper_repair"]["repaired_wrapper_sha256"]),
    ])

    repro = final["reproducibility_status"]
    extra.extend([
        check("final summary discovery state", final.get("blind_discovery_reproduction", {}).get("status") == "EXACT_2026_BLIND_REDISCOVERY" and repro.get("discovery_lineage_reproduced") is True, {"blind_status": final.get("blind_discovery_reproduction", {}).get("status"), "lineage_reproduced": repro.get("discovery_lineage_reproduced")}, {"blind_status": "EXACT_2026_BLIND_REDISCOVERY", "lineage_reproduced": True}),
        check("final summary method reconciliation", final.get("method_control_reconciliation", {}).get("historical_v2", {}).get("aggregate_verdict") == "NO_GO_DEGENERATE_PARENT_CLUSTER" and final.get("method_control_reconciliation", {}).get("corrected_independent_2024", {}).get("status") == "CORRECTED_INDEPENDENT_YEAR_CONTROL_PASS", final.get("method_control_reconciliation"), "historical no-go plus corrected independent holdout pass"),
        check("final summary recovered analysis state", repro["core_gmn_analysis_code_committed"] is True and repro["exact_primary_clean_rerun_completed"] is True and repro["internal_downstream_clean_rerun_status"] == "passed" and repro["external_archive_clean_rerun_status"] == "passed" and repro["analysis_chain_clean_rerun_completed"] is True, repro, "recovered source plus primary/internal/external reruns passed"),
        check("final summary submission hold", repro["publication_or_formal_mdc_submission_allowed"] is False and repro["end_to_end_clean_rerun_completed"] is False, {"publication_or_formal_mdc_submission_allowed": repro["publication_or_formal_mdc_submission_allowed"], "end_to_end_clean_rerun_completed": repro["end_to_end_clean_rerun_completed"]}, {"publication_or_formal_mdc_submission_allowed": False, "end_to_end_clean_rerun_completed": False}, "Independent review remains required."),
        check("candidate solution finalized recovery", candidate.get("computational_recovery", {}).get("blind_discovery") == "EXACT_2026_BLIND_REDISCOVERY" and candidate.get("method_control_reconciliation", {}).get("corrected_independent_2024", {}).get("passed") is True, {"blind": candidate.get("computational_recovery", {}).get("blind_discovery"), "method_passed": candidate.get("method_control_reconciliation", {}).get("corrected_independent_2024", {}).get("passed")}, {"blind": "EXACT_2026_BLIND_REDISCOVERY", "method_passed": True}),
        check("reproducibility gap current verdict", gap.get("verdict") == EXPECTED_GAP, gap.get("verdict"), EXPECTED_GAP),
        check("human-readable final recovery status", "Actual January–July 2026 blind-discovery matrix: **passed and committed**" in RECOVERY_STATUS.read_text() and "Corrected independent-year 2024 method controls: **passed 3/3**" in RECOVERY_STATUS.read_text(), "recovery status phrases", "blind and corrected method controls passed"),
        check("method reconciliation document", "historical v2 gate remains recorded" in METHOD_RECONCILIATION.read_text() and "Independent 2024 result" in METHOD_RECONCILIATION.read_text(), "reconciliation sections", "historical no-go and prospective pass disclosed"),
    ])

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
        "historical_method_controls": str(METHOD_ORIGINAL.relative_to(ROOT)),
        "corrected_method_controls": str(METHOD_V3.relative_to(ROOT)),
        "blind_discovery": str(BLIND.relative_to(ROOT)),
        "blind_wrapper_repair": str(WRAPPER_FIX.relative_to(ROOT)),
        "analysis_chain_clean_rerun_completed": repro["analysis_chain_clean_rerun_completed"],
        "discovery_lineage_reproduced": repro.get("discovery_lineage_reproduced"),
        "submission_allowed": repro["publication_or_formal_mdc_submission_allowed"],
    }

    manifest_paths = [
        SOURCE_MANIFEST, EXACT_PRIMARY, EXACT_DOWNSTREAM, EXACT_EXTERNAL,
        METHOD_ORIGINAL, METHOD_V3, BLIND, WRAPPER_FIX, WRAPPER_REPAIRED,
        FINAL, CANDIDATE, GAP, RECOVERY_STATUS, METHOD_RECONCILIATION,
    ]
    for path in manifest_paths:
        report["manifest"][str(path.relative_to(ROOT))] = {
            "byte_count": path.stat().st_size,
            "sha256": sha256(path),
        }

    base_json.write_text(json.dumps(report, indent=2) + "\n")
    failed = [item for item in report["checks"] if not item["passed"]]
    lines = [
        "# GhostStream recovered MDC package consistency audit", "",
        f"**Verdict:** `{report['verdict']}`", "",
        f"- Checks: **{report['check_count']}**",
        f"- Passed: **{report['passed_checks']}**",
        f"- Failed: **{report['failed_checks']}**",
        f"- Lookup rows: **{report['lookup_rows']}**", "",
        "## Recovered evidence", "",
        "- immutable source snapshots: 13 + 35 files",
        "- January–July 2026 blind matrix: one April survivor; no non-April survivors",
        "- historical v2 method-control no-go preserved",
        "- corrected independent 2024 method controls: 3/3 passed",
        "- exact primary reproduction: 101 total events and exact 95-event lookup",
        "- exact internal downstream reproduction: source null, bootstrap, activity, geography, and 81/81 specification cells",
        "- recovered external reproduction: 6 CAMS + 4 SonotaCo, exact pooled 10-event set, and current JPL screen",
        "- formal submission remains blocked pending independent review", "",
    ]
    if failed:
        lines.extend(["## Failures", ""])
        for item in failed:
            lines.append(f"- **{item['name']}** — observed `{item['observed']}`, expected `{item['expected']}`")
        lines.append("")
    lines.extend(["## Package manifest", "", "| File | Bytes | SHA-256 |", "|---|---:|---|"])
    for name, values in sorted(report["manifest"].items()):
        lines.append(f"| `{name}` | {values['byte_count']} | `{values['sha256']}` |")
    lines.extend([
        "", "## Claim boundary", "",
        "This audit establishes internal consistency between the draft MDC package and the recovered computational evidence. It does not constitute IAU submission, official recognition, independent scientific review, a complete EDMOND v6.01 replication, or parent-body identification.", "",
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
