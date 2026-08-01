#!/usr/bin/env python3
"""Reconcile all GhostStream outputs with the linked-release integrity audit.

The linked annual files are readable and scientifically evaluable, but their
row counts and embedded versions show that they are not the complete advertised
EDMOND v6.01 release. This one-time migration removes stronger stale wording.
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


# Top-level results.
replace_once(
    "pilots/ghoststream/RESULTS.md",
    "- reproduces exactly those six and no additional members when the unchanged template is applied to every usable linked EDMOND v6.01 annual archive from 2001–2023; and",
    "- reproduces exactly those six and no additional members across all currently linked EDMOND annual files from 2001–2023, while a release-integrity audit shows those links are incomplete or stale relative to the advertised v6.01 release; and",
)
replace_once(
    "pilots/ghoststream/RESULTS.md",
    "The advertised public EDMOND 2024 annual attachment remains unavailable. A networked recovery audit tested 434 candidate URLs, direct and alternate site paths, the WordPress media API, Wayback, and recent Common Crawl indexes without finding a CRC-valid 2024 ZIP; the neighboring official 2023 archive passed ZIP, CRC, and schema validation in the same environment. The missing 2024 file was not inferred or reconstructed.\n\nThe unchanged zero-speed-drift template was then applied to all **23 usable linked annual archives from 2001–2023**. It selected exactly the same six 2014, 2016, 2017, and 2022 events already preserved from the Shober subset and no additional events. The full-series activity enrichment was strong (one-sided Fisher p = **3.3785×10⁻⁴**, odds ratio **7.455**) and the post-selection orbit remained decisive (median Southworth–Hawkins D = **0.03601**, q90 = **0.07344**, 20,000-trial orbit-null p = **4.99975×10⁻⁵**). The 48-position shifted-window audit gave p = **0.06122**. This is therefore supporting evidence rather than a standalone frozen pass: the sample remains below the preexisting N ≥ 8 rule and the supplemental localization audit is slightly above 0.05. No scientific inference is drawn from the absent 2024 attachment.",
    "The advertised public EDMOND 2024 annual attachment remains unavailable. The exhaustive recovery run recorded 434 probes, including 432 deterministic live and legacy asset paths; no CRC-valid 2024 ZIP was recovered, while the linked 2023 ZIP passed signature, CRC, and schema validation in the same environment. The missing 2024 file was not inferred or reconstructed.\n\nA separate release-integrity audit showed that the surviving annual links are **not the complete advertised v6.01 release**. The 23 linked CSVs for 2001–2023 contain **481,252 rows**, versus **614,758** advertised for those same years (**78.283%**); **0 of 23** annual counts match; and embedded `_Version` values are predominantly **513** and **516**, not 601. They are therefore described as the **currently linked files**, not as a complete v6.01 archive.\n\nThe unchanged zero-speed-drift template was applied to every currently linked annual file from 2001–2023. It selected exactly the same six 2014, 2016, 2017, and 2022 events already preserved from the Shober subset and no additional events. The activity enrichment was strong (one-sided Fisher p = **3.3785×10⁻⁴**, odds ratio **7.455**) and the post-selection orbit remained decisive (median Southworth–Hawkins D = **0.03601**, q90 = **0.07344**, 20,000-trial orbit-null p = **4.99975×10⁻⁵**). The 48-position shifted-window audit gave p = **0.06122**. This supports the six existing EDMOND events but is neither a new independent sample nor a complete v6.01 replication. It also remains below the preexisting N ≥ 8 rule. No scientific inference is drawn from the absent 2024 attachment.",
)

# Uniform external synthesis.
replace_once(
    "pilots/ghoststream/april_stream/ALL_EXTERNAL_ZERO_SPEED.md",
    "## Full linked EDMOND v6.01 annual audit\n\nThe unchanged zero-speed-drift template was also applied to every usable annual archive linked by the public EDMOND v6.01 page. Twenty-three annual ZIPs from 2001–2023 passed signature, CRC, schema, and finite-field checks; the linked 2024 ZIP returned HTTP 404. The evaluation selected exactly the same six EDMOND events already listed above and no additional events.\n\n- Members: **6**\n- Years: **2014, 2016, 2017, 2022**\n- One-sided activity p: **3.3785294 × 10⁻⁴**\n- Activity odds ratio: **7.4554**\n- Shifted-window p: **0.0612245**\n- Median Southworth–Hawkins D: **0.036005**\n- q90 Southworth–Hawkins D: **0.073441**\n- Orbit-null p: **4.99975 × 10⁻⁵**\n- Exact overlaps with the six Shober-selected events: **6/6**\n- Additional selected events: **0**\n\nThis strengthens the provenance and reproducibility of the six-event EDMOND support but does not turn it into a new independent sample. It remains below the frozen N ≥ 8 standalone gate, and its supplemental shifted-window audit is slightly above 0.05.",
    "## Currently linked EDMOND annual-file audit\n\nThe unchanged zero-speed-drift template was applied to all annual ZIPs currently linked by the EDMOND v6.01 page. Twenty-three ZIPs from 2001–2023 passed signature, CRC, schema, and finite-field checks; the linked 2024 ZIP returned HTTP 404. Release-integrity checks show that these links are incomplete or stale relative to the page: 481,252 linked rows versus 614,758 advertised for the same years, 0/23 annual count matches, and embedded versions 513/516 rather than 601. They are not represented as a complete v6.01 release. The evaluation selected exactly the same six EDMOND events already listed above and no additional events.\n\n- Members: **6**\n- Years: **2014, 2016, 2017, 2022**\n- One-sided activity p: **3.3785294 × 10⁻⁴**\n- Activity odds ratio: **7.4554**\n- Shifted-window p: **0.0612245**\n- Median Southworth–Hawkins D: **0.036005**\n- q90 Southworth–Hawkins D: **0.073441**\n- Orbit-null p: **4.99975 × 10⁻⁵**\n- Exact overlaps with the six Shober-selected events: **6/6**\n- Additional selected events: **0**\n\nThis strengthens the provenance and reproducibility of the six-event EDMOND support in the currently linked files but does not turn it into a new independent sample or a complete current-release replication. It remains below the frozen N ≥ 8 standalone gate, and its supplemental shifted-window audit is slightly above 0.05.",
)

# Manuscript data and results language.
replace_once(
    "pilots/ghoststream/april_stream/mdc/MANUSCRIPT_DRAFT.md",
    "The public EDMOND v6.01 page advertises a 2024 annual file containing 13,513 refined orbits, but its live attachment returned HTTP 404. A networked recovery audit tested 434 candidate URLs, direct and alternate site paths, the WordPress media API, Wayback, and recent Common Crawl indexes without locating a CRC-valid 2024 ZIP; the neighboring official 2023 attachment passed ZIP, CRC, and schema validation in the same environment. The missing 2024 file was not inferred or reconstructed. The frozen candidate was instead evaluated in every usable annual ZIP linked by the same page, covering 2001–2023. No result was inferred from the missing 2024 file.",
    "The public EDMOND v6.01 page advertises a 2024 annual file containing 13,513 refined orbits, but its live attachment returned HTTP 404. The exhaustive recovery run recorded 434 probes, including 432 deterministic live and legacy paths, without locating a CRC-valid 2024 ZIP; the linked 2023 attachment passed ZIP, CRC, and schema validation in the same environment. The missing 2024 file was not inferred or reconstructed. Release-integrity checks of the surviving links found 481,252 rows for 2001–2023 versus 614,758 advertised for those years, no annual row-count matches, and embedded `_Version` values 513/516 rather than 601. The frozen candidate was therefore evaluated in every currently linked annual file, but this was not represented as a complete v6.01 replication. No result was inferred from the missing 2024 file.",
)
replace_once(
    "pilots/ghoststream/april_stream/mdc/MANUSCRIPT_DRAFT.md",
    "#### Full linked EDMOND v6.01 audit\n\nThe unchanged zero-speed-drift template was subsequently applied to all 23 usable annual archives linked by the public EDMOND v6.01 page from 2001 through 2023; the linked 2024 archive remained unavailable. The full annual series selected exactly the same six UTC events as the Shober subset and no additional events. Within the expanded antihelion source, the frozen inside-versus-outside activity test gave p = 3.3785 × 10⁻⁴ and a Haldane–Anscombe odds ratio of 7.455. A 48-position shifted-window audit gave a plus-one empirical p = 0.06122. The six post-selection orbits had median Southworth–Hawkins D = 0.03601, q90 D = 0.07344, and a 20,000-trial source/time-matched orbit-null p = 4.99975 × 10⁻⁵. This full-series check confirms that the six selected events are reproducible in the public annual archives, but it does not create an independent sample and does not pass the frozen N ≥ 8 or shifted-window localization gates.",
    "#### Currently linked EDMOND annual-file audit\n\nThe unchanged zero-speed-drift template was subsequently applied to all 23 usable annual files currently linked by the public EDMOND v6.01 page from 2001 through 2023; the linked 2024 archive remained unavailable. The linked files are not the complete advertised v6.01 release: their combined row count is 78.283% of the page total for those years, none of the 23 annual counts matches, and embedded versions are 513/516. The currently linked files selected exactly the same six UTC events as the Shober subset and no additional events. Within the expanded antihelion source, the frozen inside-versus-outside activity test gave p = 3.3785 × 10⁻⁴ and a Haldane–Anscombe odds ratio of 7.455. A 48-position shifted-window audit gave a plus-one empirical p = 0.06122. The six post-selection orbits had median Southworth–Hawkins D = 0.03601, q90 D = 0.07344, and a 20,000-trial source/time-matched orbit-null p = 4.99975 × 10⁻⁵. This check confirms that the six selected events are reproducible in the currently linked files, but it does not create an independent sample, complete the v6.01 test, or pass the frozen N ≥ 8 or shifted-window localization gates.",
)

# Shober note.
replace_once(
    "pilots/ghoststream/april_stream/shober_edmond/SHOBER_EDMOND_VALIDATION.md",
    "## Later full linked-series audit\n\nThe unchanged zero-speed-drift template was later applied to all 23 usable annual ZIPs linked by the public EDMOND v6.01 page from 2001–2023. The linked 2024 ZIP remained unavailable. The full annual series selected exactly these same six UTC events and no additional events. Its one-sided activity p was 3.3785×10⁻⁴, the 48-position shifted-window p was 0.06122, and the 20,000-trial post-selection orbit-null p was 4.99975×10⁻⁵. This confirms the six-member extraction in the full usable public series without changing the interpretation: supportive, orbitally strong, provenance-limited evidence rather than an independent standalone pass.",
    "## Later currently linked-file audit\n\nThe unchanged zero-speed-drift template was later applied to all 23 usable annual ZIPs currently linked by the public EDMOND v6.01 page from 2001–2023. The linked 2024 ZIP remained unavailable. Integrity checks showed that these links are incomplete or stale relative to the advertised release: 78.283% of the advertised rows for those years, 0/23 annual count matches, and embedded versions 513/516. The linked files selected exactly these same six UTC events and no additional events. Their one-sided activity p was 3.3785×10⁻⁴, the 48-position shifted-window p was 0.06122, and the 20,000-trial post-selection orbit-null p was 4.99975×10⁻⁵. This confirms the six-member extraction in the currently linked files without changing the interpretation: supportive, orbitally strong, provenance-limited evidence rather than an independent standalone or complete v6.01 pass.",
)

# Candidate JSON.
candidate_path = ROOT / "pilots/ghoststream/april_stream/candidate_solution.json"
candidate = json.loads(candidate_path.read_text())
evidence = candidate["independent_archive_evidence"]
old = evidence.pop("full_linked_edmond_v601")
old.update({
    "advertised_release_version": "6.01",
    "complete_advertised_release_tested": False,
    "currently_linked_rows_2001_2023": 481252,
    "advertised_rows_2001_2023": 614758,
    "linked_coverage_fraction": 0.78283,
    "annual_row_count_matches": 0,
    "annual_files_checked": 23,
    "embedded_version_counts": {"513": 257305, "516": 223941, "malformed_control_character_rows": 6},
    "interpretation": "All currently linked annual files reproduce exactly the prior six EDMOND events, but the links are incomplete or stale relative to the advertised v6.01 release. This is supporting, provenance-limited evidence, not a complete current-release test or an additional independent sample."
})
evidence["currently_linked_edmond_annual_files"] = old
candidate_path.write_text(json.dumps(candidate, indent=2) + "\n")

# Canonical final summary.
summary_path = ROOT / "pilots/ghoststream/results/ghoststream_final_summary.json"
summary = json.loads(summary_path.read_text())
edmond = summary["supporting_edmond_evidence"]
edmond["currently_linked_annual_files_validated"] = edmond.pop("full_linked_annual_archives_validated")
edmond["currently_linked_years"] = edmond.pop("full_linked_years")
edmond.update({
    "advertised_release_version": "6.01",
    "complete_advertised_release_tested": False,
    "currently_linked_rows_2001_2023": 481252,
    "advertised_rows_2001_2023": 614758,
    "linked_coverage_fraction": 0.78283,
    "annual_row_count_matches": 0,
    "embedded_versions": [513, 516]
})
summary["claim_limit"] = "This supports a high-confidence uncatalogued annual April meteor-stream candidate. It is not official IAU recognition, an established shower, a complete current EDMOND v6.01 replication, a fully independent third-network replication, an absolute-flux measurement, or a parent-body identification."
summary_path.write_text(json.dumps(summary, indent=2) + "\n")

# Supersede the earlier overstrong linked-v6.01 report while retaining its run metrics.
linked_report = ROOT / "pilots/ghoststream/april_stream/edmond_2024/LINKED_V601_FROZEN_VALIDATION.md"
linked_report.write_text("""# Linked EDMOND frozen evaluation — integrity correction

**Status:** `SUPERSEDED_BY_EDMOND_CURRENT_RELEASE_AUDIT`

The frozen statistical evaluation in this file's original version was numerically valid for the files that were downloaded, but its description of those files as the complete usable EDMOND v6.01 series was too strong.

The authoritative interpretation is now in `EDMOND_CURRENT_RELEASE_AUDIT.md`:

- 23 currently linked annual ZIPs for 2001–2023 are readable and pass ZIP/CRC/schema checks;
- the 2024 link returns HTTP 404;
- linked rows for 2001–2023 total 481,252 versus 614,758 advertised (78.283%);
- 0 of 23 annual row counts matches the page table;
- embedded `_Version` values are predominantly 513 and 516, not 601;
- the frozen selector recovers exactly the prior six Shober-EDMOND events and no additional events;
- activity p = 3.3785×10⁻⁴, shifted-window p = 0.06122, and orbit-null p = 4.99975×10⁻⁵; and
- the result remains supporting evidence, not a new independent sample, a standalone pass, or a complete v6.01 replication.

The original CI evidence remains preserved in workflow run `30677912275` and artifact `8811142249`; its statistics apply only to the currently linked files.
""")

# Machine-readable linked evaluation summary, corrected without deleting historical metrics.
linked_summary_path = ROOT / "pilots/ghoststream/april_stream/edmond_2024/linked_v601_frozen_summary.json"
linked_summary = json.loads(linked_summary_path.read_text())
linked_summary["verdict"] = "CURRENTLY_LINKED_EDMOND_FILES_SUPPORT_BUT_NOT_COMPLETE_V601_OR_STANDALONE_PASS"
linked_summary["release_integrity"] = {
    "advertised_release_version": "6.01",
    "complete_advertised_release_tested": False,
    "currently_linked_files_validated": 23,
    "currently_linked_rows_2001_2023": 481252,
    "advertised_rows_2001_2023": 614758,
    "coverage_fraction": 0.78283,
    "annual_row_count_matches": 0,
    "embedded_version_counts": {"513": 257305, "516": 223941, "malformed_control_character_rows": 6},
    "unavailable_years": [2024]
}
linked_summary["claim_boundary"] = "Statistics apply to all currently linked annual files, which are incomplete or stale relative to the advertised v6.01 release. They do not constitute a complete current-release replication."
linked_summary_path.write_text(json.dumps(linked_summary, indent=2) + "\n")

print("Reconciled all EDMOND linked-release integrity claims.")
