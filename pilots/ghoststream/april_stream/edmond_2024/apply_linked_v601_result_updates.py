#!/usr/bin/env python3
"""Apply the completed linked-EDMOND result to project-level scientific outputs.

Every prose change uses an exact single-match replacement. The script aborts
rather than silently editing an unexpected document version.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def replace_once(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text()
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{relative}: expected one exact match, found {count}")
    path.write_text(text.replace(old, new, 1))


# Top-level results: add the full-public-series reproduction to the headline evidence.
replace_once(
    "pilots/ghoststream/RESULTS.md",
    "- receives additional orbitally strong support from **six non-overlapping meteors** in a shower-removed EDMOND subset; and",
    "- receives additional orbitally strong support from **six non-overlapping meteors** in a shower-removed EDMOND subset;\n"
    "- reproduces exactly those six and no additional members when the unchanged template is applied to every usable linked EDMOND v6.01 annual archive from 2001–2023; and",
)

replace_once(
    "pilots/ghoststream/RESULTS.md",
    "The advertised public EDMOND 2024 annual attachment was unavailable during the audit. The page, WordPress API, sitemaps, and 252 plausible asset paths did not yield a valid file. No scientific inference was drawn from its absence.",
    "The advertised public EDMOND 2024 annual attachment remains unavailable. A networked recovery audit tested 434 candidate URLs, direct and alternate site paths, the WordPress media API, Wayback, and recent Common Crawl indexes without finding a CRC-valid 2024 ZIP; the neighboring official 2023 archive passed ZIP, CRC, and schema validation in the same environment. The missing 2024 file was not inferred or reconstructed.\n\n"
    "The unchanged zero-speed-drift template was then applied to all **23 usable linked annual archives from 2001–2023**. It selected exactly the same six 2014, 2016, 2017, and 2022 events already preserved from the Shober subset and no additional events. The full-series activity enrichment was strong (one-sided Fisher p = **3.3785×10⁻⁴**, odds ratio **7.455**) and the post-selection orbit remained decisive (median Southworth–Hawkins D = **0.03601**, q90 = **0.07344**, 20,000-trial orbit-null p = **4.99975×10⁻⁵**). The 48-position shifted-window audit gave p = **0.06122**. This is therefore supporting evidence rather than a standalone frozen pass: the sample remains below the preexisting N ≥ 8 rule and the supplemental localization audit is slightly above 0.05. No scientific inference is drawn from the absent 2024 attachment.",
)

# Manuscript data description: distinguish missing-2024 acquisition from the usable-series evaluation.
replace_once(
    "pilots/ghoststream/april_stream/mdc/MANUSCRIPT_DRAFT.md",
    "The public EDMOND v6.01 page advertises a 2024 annual file containing 13,513 refined orbits, but its live attachment was unavailable during the audit. The page HTML, WordPress media API, sitemaps, and 252 plausible asset paths were checked without locating a valid ZIP. No result was inferred from that missing file.",
    "The public EDMOND v6.01 page advertises a 2024 annual file containing 13,513 refined orbits, but its live attachment returned HTTP 404. A networked recovery audit tested 434 candidate URLs, direct and alternate site paths, the WordPress media API, Wayback, and recent Common Crawl indexes without locating a CRC-valid 2024 ZIP; the neighboring official 2023 attachment passed ZIP, CRC, and schema validation in the same environment. The missing 2024 file was not inferred or reconstructed. The frozen candidate was instead evaluated in every usable annual ZIP linked by the same page, covering 2001–2023. No result was inferred from the missing 2024 file.",
)

replace_once(
    "pilots/ghoststream/april_stream/mdc/MANUSCRIPT_DRAFT.md",
    "The EDMOND sample narrowly missed the standalone p ≤ 0.01 and N ≥ 8 rules, so it is supportive rather than independently decisive.",
    "The EDMOND sample narrowly missed the standalone p ≤ 0.01 and N ≥ 8 rules, so it is supportive rather than independently decisive.\n\n"
    "#### Full linked EDMOND v6.01 audit\n\n"
    "The unchanged zero-speed-drift template was subsequently applied to all 23 usable annual archives linked by the public EDMOND v6.01 page from 2001 through 2023; the linked 2024 archive remained unavailable. The full annual series selected exactly the same six UTC events as the Shober subset and no additional events. Within the expanded antihelion source, the frozen inside-versus-outside activity test gave p = 3.3785 × 10⁻⁴ and a Haldane–Anscombe odds ratio of 7.455. A 48-position shifted-window audit gave a plus-one empirical p = 0.06122. The six post-selection orbits had median Southworth–Hawkins D = 0.03601, q90 D = 0.07344, and a 20,000-trial source/time-matched orbit-null p = 4.99975 × 10⁻⁵. This full-series check confirms that the six selected events are reproducible in the public annual archives, but it does not create an independent sample and does not pass the frozen N ≥ 8 or shifted-window localization gates.",
)

# Zero-speed synthesis: add the completed full linked-series audit before interpretation.
replace_once(
    "pilots/ghoststream/april_stream/ALL_EXTERNAL_ZERO_SPEED.md",
    "## Interpretation",
    "## Full linked EDMOND v6.01 annual audit\n\n"
    "The unchanged zero-speed-drift template was also applied to every usable annual archive linked by the public EDMOND v6.01 page. Twenty-three annual ZIPs from 2001–2023 passed signature, CRC, schema, and finite-field checks; the linked 2024 ZIP returned HTTP 404. The evaluation selected exactly the same six EDMOND events already listed above and no additional events.\n\n"
    "- Members: **6**\n"
    "- Years: **2014, 2016, 2017, 2022**\n"
    "- One-sided activity p: **3.3785294 × 10⁻⁴**\n"
    "- Activity odds ratio: **7.4554**\n"
    "- Shifted-window p: **0.0612245**\n"
    "- Median Southworth–Hawkins D: **0.036005**\n"
    "- q90 Southworth–Hawkins D: **0.073441**\n"
    "- Orbit-null p: **4.99975 × 10⁻⁵**\n"
    "- Exact overlaps with the six Shober-selected events: **6/6**\n"
    "- Additional selected events: **0**\n\n"
    "This strengthens the provenance and reproducibility of the six-event EDMOND support but does not turn it into a new independent sample. It remains below the frozen N ≥ 8 standalone gate, and its supplemental shifted-window audit is slightly above 0.05.\n\n"
    "## Interpretation",
)

# Shober-specific validation note: append the completed full annual-series check.
shober_path = ROOT / "pilots/ghoststream/april_stream/shober_edmond/SHOBER_EDMOND_VALIDATION.md"
shober_text = shober_path.read_text()
marker = "## Later full linked-series audit"
if marker in shober_text:
    raise RuntimeError("SHOBER_EDMOND_VALIDATION.md already contains linked-series section")
shober_text += (
    "\n## Later full linked-series audit\n\n"
    "The unchanged zero-speed-drift template was later applied to all 23 usable annual ZIPs linked by the public EDMOND v6.01 page from 2001–2023. The linked 2024 ZIP remained unavailable. The full annual series selected exactly these same six UTC events and no additional events. Its one-sided activity p was 3.3785×10⁻⁴, the 48-position shifted-window p was 0.06122, and the 20,000-trial post-selection orbit-null p was 4.99975×10⁻⁵. This confirms the six-member extraction in the full usable public series without changing the interpretation: supportive, orbitally strong, provenance-limited evidence rather than an independent standalone pass.\n"
)
shober_path.write_text(shober_text)

# Candidate JSON: preserve the result in the canonical machine-readable candidate record.
candidate_path = ROOT / "pilots/ghoststream/april_stream/candidate_solution.json"
candidate = json.loads(candidate_path.read_text())
archive_evidence = candidate["independent_archive_evidence"]
if "full_linked_edmond_v601" in archive_evidence:
    raise RuntimeError("candidate_solution.json already contains full_linked_edmond_v601")
archive_evidence["full_linked_edmond_v601"] = {
    "validated_annual_archives": 23,
    "validated_years": list(range(2001, 2024)),
    "unavailable_years": [2024],
    "selected_members": 6,
    "selected_years": [2014, 2016, 2017, 2022],
    "exact_overlaps_with_prior_shober_six": 6,
    "additional_selected_events": 0,
    "uniform_speed_drift_km_s_per_deg": 0.0,
    "activity_p": 0.0003378529391388961,
    "activity_odds_ratio": 7.4554307337988845,
    "shifted_window_p": 0.061224489795918366,
    "median_orbit_d_sh": 0.03600524759144138,
    "q90_orbit_d_sh": 0.07344069219748785,
    "maximum_orbit_d_sh": 0.09805965651612987,
    "orbit_null_p": 0.00004999750012499375,
    "standalone_gate_passed": False,
    "interpretation": "The complete usable linked v6.01 annual series reproduces exactly the prior six EDMOND events. It is supporting, provenance-limited evidence, not an additional independent sample or a full frozen pass."
}
candidate_path.write_text(json.dumps(candidate, indent=2) + "\n")

# Replace the stale final summary, which still treated the older NMV recovery as primary.
final_summary = {
    "pilot": "GhostStream",
    "overall_verdict": "GO",
    "primary_result": {
        "internal_id": "GhostStream-April-36.9",
        "status": "high_confidence_uncatalogued_stream_candidate",
        "official_iau_designation": None,
        "significant_gmn_years": [2022, 2023, 2024, 2025, 2026],
        "confirmed_gmn_members": 95,
        "deduplicated_selected_gmn_members_2019_2026": 101,
        "untouched_confirmation_years": [2022, 2023],
        "untouched_pooled_activity_p": 0.00001857134041807409,
        "untouched_shifted_window_p": 0.017543859649122806,
        "untouched_orbit_null_p": 0.0001,
        "geographic_groups_passing": 3,
        "specification_grid_passes": 81,
        "specification_grid_cells": 81,
        "uncertainty_clone_passes": 1000,
        "uncertainty_clone_trials": 1000,
        "iau_solutions_parsed": 2174,
        "hard_iau_matches": 0
    },
    "primary_external_support": {
        "catalogs": ["CAMS", "SonotaCo"],
        "members": 10,
        "years": [2011, 2012, 2022, 2023, 2025],
        "activity_p_posthoc": 0.0001621843884718582,
        "shifted_window_p_posthoc": 0.02040816326530612,
        "orbit_null_p": 0.00005
    },
    "supporting_edmond_evidence": {
        "members": 6,
        "years": [2014, 2016, 2017, 2022],
        "full_linked_annual_archives_validated": 23,
        "full_linked_years": [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
        "unavailable_linked_years": [2024],
        "exact_overlaps_with_prior_six": 6,
        "additional_selected_events": 0,
        "activity_p": 0.0003378529391388961,
        "shifted_window_p": 0.061224489795918366,
        "orbit_null_p": 0.00004999750012499375,
        "standalone_gate_passed": False
    },
    "secondary_result": {
        "iau_code": "NMV",
        "name": "Northern March gamma-Virginids",
        "iau_status": "working list",
        "finding": "Independent multi-year method-validation recovery in GMN meteors labeled sporadic"
    },
    "method_validation": {
        "untouched_known_showers_recovered": 3,
        "untouched_known_showers_tested": 3,
        "injection_recovery": {
            "20_members": "4/9",
            "40_members": "7/9",
            "80_members": "8/9"
        }
    },
    "claim_limit": "This supports a high-confidence uncatalogued annual April meteor-stream candidate. It is not official IAU recognition, an established shower, a fully independent third-network replication, an absolute-flux measurement, or a parent-body identification."
}
(ROOT / "pilots/ghoststream/results/ghoststream_final_summary.json").write_text(
    json.dumps(final_summary, indent=2) + "\n"
)

print("Applied linked EDMOND v6.01 result updates successfully.")
