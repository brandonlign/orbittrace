#!/usr/bin/env python3
"""Integrate the checksum-locked live IAU MDC novelty refresh.

This one-time migration updates canonical scientific outputs without changing
the frozen GhostStream candidate or its duplicate-screen thresholds.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

VERSION = "2026-06-25"
SHOWERS = 1072
SOLUTIONS = 2174
BYTES = 3308032
SHA256 = "821fa09734314e2796388c4f2fc94bb770998f2f2b08d6a84135660849aef899"
ARTIFACT_SHA256 = "d7a88515dcc97762812dd4df6b431a2c65805928969ad114b3636809254ae393"


def replace_once(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text()
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{relative}: expected one exact match, found {count}")
    path.write_text(text.replace(old, new, 1))


# Top-level results headline and novelty section.
replace_once(
    "pilots/ghoststream/RESULTS.md",
    "- is absent from all **2,174** parsable IAU Meteor Data Center shower solutions used in the audit;",
    "- has **zero hard duplicates and zero radiant–speed–activity near matches** among all **2,174** solutions in the checksum-locked official IAU Meteor Data Center catalogue version **2026-06-25**;",
)
replace_once(
    "pilots/ghoststream/RESULTS.md",
    "### Novelty and parent-body audit\n\n- IAU shower solutions checked: **2,174**\n- Hard matches: **0**\n- Nearest official orbit: Northern May Ophiuchids, D ≈ **0.235**, with the wrong activity epoch and radiant\n- JPL small bodies screened: **6,284**\n- Credible objects at D ≤ 0.15: **0**\n- Nearest object: D ≈ 0.159, but uncertainty code 8 and only an 11-day observational arc\n\nNo parent body is claimed.",
    "### Novelty and parent-body audit\n\nThe official IAU MDC full shower-data JSON was refreshed and checksum-locked on 2026-08-01. Catalogue version **2026-06-25** contained **1,072 shower records** and **2,174 submitted solutions**. Under the frozen activity, drifted-radiant, speed, and complete-orbit duplicate rules:\n\n- Hard duplicate matches: **0**\n- Activity-compatible radiant–speed near matches: **0**\n- Orbit-incomplete near matches: **0**\n- Catalogue SHA-256: `821fa09734314e2796388c4f2fc94bb770998f2f2b08d6a84135660849aef899`\n- Nearest complete orbit: Northern May Ophiuchids solution 004, D_SH = **0.23445**\n- NOP activity interval: solar longitude **45°–75°**, which does not overlap the candidate interval\n- NOP drifted-radiant separation: **9.59°**\n\nThe current official catalogue therefore contains no duplicate or incomplete-orbit near match hidden by missing elements.\n\n- JPL small bodies screened: **6,284**\n- Credible objects at D ≤ 0.15: **0**\n- Nearest object: D ≈ 0.159, but uncertainty code 8 and only an 11-day observational arc\n\nNo parent body is claimed.",
)

# Manuscript abstract and catalogue-results paragraph.
replace_once(
    "pilots/ghoststream/april_stream/mdc/MANUSCRIPT_DRAFT.md",
    "No matching solution was found among 2,174 parsed IAU MDC shower solutions.",
    "A checksum-locked refresh of the official IAU MDC catalogue version 2026-06-25 parsed 1,072 shower records and 2,174 solutions and found no hard duplicate, no activity-compatible radiant–speed near match, and no orbit-incomplete near match.",
)
replace_once(
    "pilots/ghoststream/april_stream/mdc/MANUSCRIPT_DRAFT.md",
    "No hard match was found among 2,174 parsed IAU MDC shower solutions. The nearest official orbit was the Northern May Ophiuchids at D ≈ 0.235, but its activity epoch and radiant do not match the candidate.",
    "The official IAU MDC full shower-data JSON was refreshed on 2026-08-01 and checksum-locked at catalogue version 2026-06-25 (1,072 shower records, 2,174 submitted solutions; SHA-256 `821fa09734314e2796388c4f2fc94bb770998f2f2b08d6a84135660849aef899`). The frozen screen found no hard duplicate, no activity-compatible radiant–speed near match, and no orbit-incomplete near match. The nearest complete orbit was Northern May Ophiuchids solution 004 at Southworth–Hawkins D = 0.23445. Its published activity interval of solar longitude 45°–75° does not overlap the candidate interval, and its drifted radiant remained separated by 9.59°.",
)

# Candidate machine-readable record.
candidate_path = ROOT / "pilots/ghoststream/april_stream/candidate_solution.json"
candidate = json.loads(candidate_path.read_text())
novelty = candidate["novelty_audit"]
novelty.update({
    "iau_catalogue_version": VERSION,
    "iau_catalogue_shower_records": SHOWERS,
    "iau_solutions_parsed": SOLUTIONS,
    "iau_catalogue_byte_count": BYTES,
    "iau_catalogue_sha256": SHA256,
    "hard_iau_matches": 0,
    "radiant_speed_activity_near_matches": 0,
    "orbit_incomplete_near_matches": 0,
    "duplicate_rules": {
        "candidate_activity_interval_solar_longitude_deg": [32.901963, 40.901963],
        "mean_epoch_fallback_half_width_deg": 8.0,
        "maximum_drifted_radiant_separation_deg": 5.0,
        "maximum_drifted_speed_difference_km_s": 5.0,
        "maximum_southworth_hawkins_d": 0.15,
        "hard_match_requires_complete_orbit": True
    },
    "nearest_official_orbit": {
        "iau_number": "00149",
        "code": "NOP",
        "name": "Northern May Ophiuchids",
        "solution_number": "004",
        "orbit_distance_d_sh": 0.23445149980443517,
        "published_activity_interval_solar_longitude_deg": [45.0, 75.0],
        "mean_epoch_delta_deg": 21.698037,
        "drifted_radiant_separation_deg": 9.587885339576435,
        "drifted_speed_difference_km_s": 1.0048719724795987,
        "active_at_candidate_epoch": False,
        "hard_duplicate_match": False
    },
    "ci_evidence": {
        "workflow_run_id": 30678572191,
        "artifact_id": 8811375826,
        "artifact_sha256": ARTIFACT_SHA256
    }
})
candidate_path.write_text(json.dumps(candidate, indent=2) + "\n")

# Canonical final summary.
summary_path = ROOT / "pilots/ghoststream/results/ghoststream_final_summary.json"
summary = json.loads(summary_path.read_text())
primary = summary["primary_result"]
primary.update({
    "iau_catalogue_version": VERSION,
    "iau_catalogue_shower_records": SHOWERS,
    "iau_solutions_parsed": SOLUTIONS,
    "iau_catalogue_sha256": SHA256,
    "hard_iau_matches": 0,
    "radiant_speed_activity_near_matches": 0,
    "orbit_incomplete_near_matches": 0
})
summary_path.write_text(json.dumps(summary, indent=2) + "\n")

print("Integrated live IAU MDC novelty refresh successfully.")
