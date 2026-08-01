#!/usr/bin/env python3
"""Finalize GhostStream machine-readable status from committed evidence.

This script does not recompute scientific results. It fail-closes unless the
primary, downstream, external, historical method-control, corrected method
holdout, and blind-discovery evidence files are internally consistent, then
updates the project summary and candidate record from those sources.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
FINAL = ROOT / "pilots/ghoststream/results/ghoststream_final_summary.json"
CANDIDATE = ROOT / "pilots/ghoststream/april_stream/candidate_solution.json"
PRIMARY = ROOT / "pilots/ghoststream/reconstruction/exact_recovered/exact_reproduction.json"
DOWNSTREAM = ROOT / "pilots/ghoststream/reconstruction/exact_downstream/downstream_reproduction.json"
EXTERNAL = ROOT / "pilots/ghoststream/reconstruction/exact_external/external_reproduction.json"
METHOD_ORIGINAL = ROOT / "pilots/ghoststream/reconstruction/exact_method_controls/method_controls.json"
METHOD_V3 = ROOT / "pilots/ghoststream/reconstruction/exact_method_controls_v3/method_controls_v3.json"
BLIND = ROOT / "pilots/ghoststream/reconstruction/exact_blind_rediscovery/blind_rediscovery.json"
WRAPPER_FIX = ROOT / "pilots/ghoststream/reconstruction/blind_wrapper_fix.json"

FINAL_VERDICT = "GO_SCIENTIFIC_CANDIDATE_PUBLICATION_HOLD"
GAP_VERDICT = "COMPUTATIONAL_RECOVERY_AND_DISCOVERY_LINEAGE_COMPLETE_REVIEW_PENDING"


def load(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text())


def write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> int:
    final = load(FINAL)
    candidate = load(CANDIDATE)
    primary = load(PRIMARY)
    downstream = load(DOWNSTREAM)
    external = load(EXTERNAL)
    method_original = load(METHOD_ORIGINAL)
    method_v3 = load(METHOD_V3)
    blind = load(BLIND)
    wrapper = load(WRAPPER_FIX)

    assert primary["status"] == "EXACT_REPRODUCTION"
    assert primary["total_members"] == 101
    assert primary["preserved_95_exact"] is True
    assert downstream["status"] == "EXACT_RECOVERED_DOWNSTREAM_REPRODUCTION"
    assert downstream["checks"]["specification_curve"]["passing_cells"] == 81
    assert external["status"] == "RECOVERED_EXTERNAL_ARCHIVE_REPRODUCTION"
    assert external["checks"]["exploratory_pooled_synthesis"]["member_id_set_exact"] is True
    assert method_original["status"] == "RECOVERED_METHOD_CONTROL_AUDIT_NEGATIVE_GATE_INFEASIBLE"
    assert method_original["known_shower_recovery"]["original_verdict"] == "NO_GO_DEGENERATE_PARENT_CLUSTER"
    assert method_original["weak_stream_injection"]["verdict"] == "INJECTION_GATE_PASS"
    assert method_v3["status"] == "CORRECTED_INDEPENDENT_YEAR_CONTROL_PASS"
    assert method_v3["passed"] is True
    assert method_v3["recovered_controls"] == 3
    assert method_v3["non_target_degeneracy_passes"] == 3
    assert blind["status"] == "EXACT_2026_BLIND_REDISCOVERY"
    assert blind["months_scanned"] == [1, 2, 3, 4, 5, 6, 7]
    assert blind["validation_years"] == [2025, 2024]
    assert blind["full_gate_survivors_across_matrix"] == 1
    assert blind["additional_non_april_survivors"] == []
    assert wrapper["status"] == "MINIMAL_RECOVERED_WRAPPER_REPAIR"
    assert wrapper["scientific_logic_changed"] is False

    blind_april = blind["april_survivor"]
    method_controls = method_v3["controls"]

    final["overall_verdict"] = FINAL_VERDICT
    final["blind_discovery_reproduction"] = {
        "status": blind["status"],
        "source_commit": blind["source_commit"],
        "entrypoint": blind["entrypoint"],
        "months_scanned": blind["months_scanned"],
        "validation_years": blind["validation_years"],
        "full_gate_survivors": blind["full_gate_survivors_across_matrix"],
        "additional_non_april_survivors": blind["additional_non_april_survivors"],
        "april_survivor": blind_april,
        "wrapper_repair": {
            "original_source_sha256": wrapper["original_source_sha256"],
            "repair_commit": wrapper["repair_commit"],
            "scientific_logic_changed": wrapper["scientific_logic_changed"],
            "scope": wrapper["repair_scope"],
        },
    }
    final["method_control_reconciliation"] = {
        "historical_v2": {
            "status": method_original["status"],
            "aggregate_verdict": method_original["known_shower_recovery"]["original_verdict"],
            "named_showers_recovered": method_original["known_shower_recovery"]["untouched_recovered"],
            "named_showers_tested": method_original["known_shower_recovery"]["untouched_eligible"],
            "weak_stream_injection_verdict": method_original["weak_stream_injection"]["verdict"],
            "scientific_gate_passed": False,
        },
        "corrected_independent_2024": {
            "status": method_v3["status"],
            "correction_frozen_before_holdout": method_v3["correction_frozen_before_2024_holdout_run"],
            "recovered_controls": method_v3["recovered_controls"],
            "eligible_controls": method_v3["eligible_controls"],
            "non_target_degeneracy_passes": method_v3["non_target_degeneracy_passes"],
            "largest_non_target_cluster_ceiling": method_v3["corrected_pass_rule"]["maximum_largest_non_target_cluster_fraction"],
            "controls": method_controls,
            "passed": method_v3["passed"],
        },
        "interpretation": (
            "The historical v2 no-go is preserved. A prospective correction "
            "addressing its mathematically infeasible target-cluster ceiling "
            "passed all three independent 2024 controls without changing the "
            "clustering or recovery thresholds."
        ),
    }

    repro = final.setdefault("reproducibility_status", {})
    repro.update({
        "core_gmn_analysis_code_committed": True,
        "source_file_hash_manifest_committed": True,
        "environment_and_random_seeds_recovered": True,
        "exact_core_raw_input_byte_manifest_committed": False,
        "exact_primary_clean_rerun_completed": True,
        "exact_101_member_result_reproduced": True,
        "exact_95_member_lookup_reproduced": True,
        "internal_downstream_clean_rerun_status": "passed",
        "external_archive_clean_rerun_status": "passed",
        "historical_method_control_status": "negative_gate_preserved",
        "corrected_method_control_status": "passed",
        "blind_discovery_lineage_status": "passed_with_minimal_non_scientific_wrapper_repair",
        "current_parent_screen_completed": True,
        "analysis_chain_clean_rerun_completed": True,
        "discovery_lineage_reproduced": True,
        "end_to_end_clean_rerun_completed": False,
        "current_branch_status": "computational_recovery_and_discovery_lineage_complete_package_and_independent_review_pending",
        "publication_or_formal_mdc_submission_allowed": False,
        "resolution_required": (
            "Regenerate the recovered MDC package audit and code-inclusive expert "
            "bundle from the final evidence, then obtain independent scientific "
            "and duplicate-shower review before submission."
        ),
    })
    final["claim_limit"] = (
        "The original source, exact primary selection, internal downstream analyses, "
        "external archive support, corrected independent-year method controls, and "
        "January-July 2026 blind discovery lineage have been reproduced and preserved. "
        "The historical v2 method-control no-go remains disclosed, and the blind "
        "lineage required only a documented non-scientific year-key/reporting repair. "
        "The result remains an uncatalogued candidate, not official IAU recognition, "
        "an established shower, a complete EDMOND v6.01 replication, a fully "
        "independent third-network replication, an absolute-flux measurement, or a "
        "parent-body identification. Formal submission remains blocked pending the "
        "final package audit and independent expert review."
    )

    historical_jpl = {
        "small_bodies_screened": candidate["novelty_audit"].get("jpl_small_bodies_screened"),
        "objects_with_orbit_distance_le_0_15": candidate["novelty_audit"].get("jpl_objects_with_orbit_distance_le_0_15"),
        "ci_evidence": candidate["novelty_audit"].get("ci_evidence"),
    }
    parent = external["checks"]["current_parent_screen"]
    candidate["computational_recovery"] = {
        "source_recovered": True,
        "primary": primary["status"],
        "internal_downstream": downstream["status"],
        "external": external["status"],
        "historical_method_control": method_original["status"],
        "corrected_method_control": method_v3["status"],
        "blind_discovery": blind["status"],
        "blind_wrapper_repair": wrapper,
    }
    candidate["blind_discovery_reproduction"] = final["blind_discovery_reproduction"]
    candidate["method_control_reconciliation"] = final["method_control_reconciliation"]
    candidate["novelty_audit"]["historical_jpl_screen"] = historical_jpl
    candidate["novelty_audit"]["current_jpl_screen"] = {
        "broad_compatible_objects": parent["broad_box_count"],
        "valid_orbits": parent["valid_orbits"],
        "objects_with_orbit_distance_le_0_15": parent["d_le_0_15"],
        "objects_with_orbit_distance_le_0_25": parent["d_le_0_25"],
        "nearest": parent["nearest"],
        "parent_body_claimed": False,
    }
    candidate["next_required_actions"] = [
        "Regenerate and pass the recovered MDC package consistency audit",
        "Build and checksum-lock the final code-inclusive expert-review bundle",
        "Obtain independent meteor-science and duplicate-shower review",
        "Confirm GMN data-use, acknowledgment, authorship, and submission language",
        "Preserve final source catalogue hashes or allowed archived copies",
        "Submit to the MDC or a journal only after the preceding review gates pass",
    ]
    candidate["claim_boundary"] = (
        "Recovered and computationally reproduced high-confidence uncatalogued "
        "late-April meteor-stream candidate; not yet submitted to or recognized "
        "by the IAU Meteor Data Center and not cleared for submission before "
        "independent review."
    )

    write(FINAL, final)
    write(CANDIDATE, candidate)
    print(json.dumps({
        "status": "FINALIZED_GHOSTSTREAM_RECOVERY_METADATA",
        "gap_verdict_to_use": GAP_VERDICT,
        "final_summary": str(FINAL.relative_to(ROOT)),
        "candidate_solution": str(CANDIDATE.relative_to(ROOT)),
        "blind_status": blind["status"],
        "method_v3_status": method_v3["status"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
