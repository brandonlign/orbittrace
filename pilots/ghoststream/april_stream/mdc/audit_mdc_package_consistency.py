#!/usr/bin/env python3
"""Mechanically audit the complete GhostStream MDC pre-submission package.

This audit recomputes every quantity available from the 95-row lookup table,
checks the arithmetic-mean JSON, calculation audit, legacy record, exact official
checker input, candidate/final summaries, live catalogue provenance, external
claim boundary, and checksums every submission-facing file.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[4]
MDC = ROOT / "pilots/ghoststream/april_stream/mdc"
APRIL = ROOT / "pilots/ghoststream/april_stream"
GHOST = ROOT / "pilots/ghoststream"

LOOKUP = MDC / "GhostStream_April_95_GMN_lookup.csv"
MEAN_JSON = MDC / "GhostStream_April_mean_submission.json"
LEGACY = MDC / "GhostStream_April_mean_legacy.txt"
CALC = MDC / "calculation_audit.json"
CHECKER_SUMMARY = MDC / "exact_official_checker_summary.json"
CHECKER_REPORT = MDC / "MDC_OFFICIAL_CHECKER_REPORT.md"
LIVE_MDC = MDC / "live_mdc_novelty_refresh_summary.json"
CANDIDATE = APRIL / "candidate_solution.json"
LINKED_EDMOND = APRIL / "edmond_2024/linked_v601_frozen_summary.json"
FINAL = GHOST / "results/ghoststream_final_summary.json"
RESULTS = GHOST / "RESULTS.md"
MANUSCRIPT = MDC / "MANUSCRIPT_DRAFT.md"
README = MDC / "README.md"
CHECKLIST = MDC / "SUBMISSION_CHECKLIST.md"

EXPECTED_LOOKUP_FIELDS = ["CurNum", "Tobs", "RA", "DE", "VG", "LS", "LO", "LA", "SCLO", "Sode"]
EXPECTED_N = 95


@dataclass
class Check:
    name: str
    passed: bool
    observed: Any
    expected: Any
    tolerance: Any = None
    note: str | None = None


checks: list[Check] = []


def check(name: str, condition: bool, observed: Any, expected: Any, tolerance: Any = None, note: str | None = None) -> None:
    checks.append(Check(name, bool(condition), observed, expected, tolerance, note))


def close(name: str, observed: float, expected: float, tolerance: float, note: str | None = None) -> None:
    check(name, math.isclose(float(observed), float(expected), rel_tol=0.0, abs_tol=tolerance), observed, expected, tolerance, note)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def arithmetic_mean(rows: list[dict[str, str]], key: str) -> float:
    return statistics.fmean(float(row[key]) for row in rows)


def ols_slope(rows: list[dict[str, str]], x_key: str, y_key: str) -> float:
    xs = [float(row[x_key]) for row in rows]
    ys = [float(row[y_key]) for row in rows]
    xbar = statistics.fmean(xs)
    ybar = statistics.fmean(ys)
    denominator = math.fsum((x - xbar) ** 2 for x in xs)
    if denominator == 0:
        raise RuntimeError(f"zero variance in {x_key}")
    return math.fsum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / denominator


def parse_legacy(path: Path) -> list[str]:
    with path.open(newline="") as handle:
        rows = list(csv.reader(handle, delimiter="|", quotechar='"'))
    if len(rows) != 1:
        raise RuntimeError(f"legacy file should contain one record, found {len(rows)}")
    if len(rows[0]) != 36:
        raise RuntimeError(f"legacy record should contain 36 fields, found {len(rows[0])}")
    return rows[0]


def phrase(path: Path, text: str) -> bool:
    return text in path.read_text()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    with LOOKUP.open(newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = reader.fieldnames or []

    check("lookup header", fields == EXPECTED_LOOKUP_FIELDS, fields, EXPECTED_LOOKUP_FIELDS)
    check("lookup row count", len(rows) == EXPECTED_N, len(rows), EXPECTED_N)

    current_numbers = [int(row["CurNum"]) for row in rows]
    check("lookup CurNum sequence", current_numbers == list(range(1, EXPECTED_N + 1)), current_numbers, "1..95")
    timestamps = [row["Tobs"] for row in rows]
    parsed_times = [datetime.strptime(value, "%Y-%m-%d-%H:%M:%S") for value in timestamps]
    check("lookup timestamps unique", len(set(timestamps)) == EXPECTED_N, len(set(timestamps)), EXPECTED_N)
    check("lookup timestamps chronological", parsed_times == sorted(parsed_times), timestamps[:2] + timestamps[-2:], "sorted ascending")
    check("lookup source label", {row["Sode"] for row in rows} == {"GMN trajectory catalogue"}, sorted({row["Sode"] for row in rows}), ["GMN trajectory catalogue"])

    recomputed = {
        "LoSb": min(float(row["LS"]) for row in rows),
        "LoSe": max(float(row["LS"]) for row in rows),
        "LoS": arithmetic_mean(rows, "LS"),
        "Ra": arithmetic_mean(rows, "RA"),
        "De": arithmetic_mean(rows, "DE"),
        "Vg": arithmetic_mean(rows, "VG"),
        "LoR": arithmetic_mean(rows, "LO"),
        "S_LoR": arithmetic_mean(rows, "SCLO"),
        "LaR": arithmetic_mean(rows, "LA"),
        "dRa": ols_slope(rows, "LS", "RA"),
        "dDe": ols_slope(rows, "LS", "DE"),
        "N": len(rows),
    }

    mean_payload = load_json(MEAN_JSON)
    mean_solutions = mean_payload["data"]["solution"]
    check("mean JSON single solution", len(mean_solutions) == 1, len(mean_solutions), 1)
    mean = mean_solutions[0]
    calc = load_json(CALC)
    calc_means = calc["means"]

    for key in ("LoSb", "LoSe", "LoS", "Ra", "De", "Vg", "LoR", "S_LoR", "LaR", "dRa", "dDe"):
        close(f"lookup recomputation -> calculation audit {key}", recomputed[key], calc_means[key], 5e-10)
        close(f"lookup recomputation -> mean JSON {key}", recomputed[key], mean[key], 5e-6)
    check("lookup recomputation -> N", recomputed["N"] == calc_means["N"] == mean["N"] == EXPECTED_N, [recomputed["N"], calc_means["N"], mean["N"]], [95, 95, 95])
    check("calculation audit first timestamp", calc["first_time"] == timestamps[0], calc["first_time"], timestamps[0])
    check("calculation audit last timestamp", calc["last_time"] == timestamps[-1], calc["last_time"], timestamps[-1])
    check("calculation audit lookup rows", calc["lookup_rows"] == EXPECTED_N, calc["lookup_rows"], EXPECTED_N)

    for calc_key, mean_key in (("q", "q"), ("e", "e"), ("peri", "peri"), ("node", "node"), ("incl", "inc"), ("a", "a")):
        close(f"calculation audit -> mean JSON {calc_key}", calc_means[calc_key], mean[mean_key], 5e-6)
    derived_a = float(mean["q"]) / (1.0 - float(mean["e"]))
    close("mean JSON semimajor identity q/(1-e)", float(mean["a"]), derived_a, 5e-6)
    close("calculation audit semimajor identity q/(1-e)", float(calc_means["a"]), float(calc_means["q"]) / (1.0 - float(calc_means["e"])), 5e-12)

    legacy = parse_legacy(LEGACY)
    legacy_map = {
        "LoSb": 8, "LoSe": 9, "LoS": 10, "Ra": 11, "De": 12,
        "dRa": 13, "dDe": 14, "Vg": 15, "LoR": 16, "S_LoR": 17,
        "LaR": 18, "a": 22, "q": 23, "e": 24, "peri": 25,
        "node": 26, "incl": 27,
    }
    for key, index in legacy_map.items():
        tolerance = 5e-4 if key not in {"a", "q", "e"} else 5e-7
        mean_key = "inc" if key == "incl" else key
        close(f"legacy rounded value {key}", float(legacy[index]), float(mean[mean_key]), tolerance)
    check("legacy N", int(legacy[28]) == EXPECTED_N, int(legacy[28]), EXPECTED_N)
    check("legacy lookup filename", legacy[34] == LOOKUP.name, legacy[34], LOOKUP.name)
    check("legacy provisional IAU", legacy[0] == "PENDING" and legacy[1] == "-" and legacy[2] == "000", legacy[:3], ["PENDING", "-", "000"])

    checker = load_json(CHECKER_SUMMARY)
    exact = checker["exact_committed_mean"]
    checker_key_map = {
        "LS": "LoS", "RA": "Ra", "Dec": "De", "Vg": "Vg",
        "q": "q", "e": "e", "peri": "peri", "node": "node", "inc": "incl",
    }
    for checker_key, mean_key in checker_key_map.items():
        close(f"exact official checker input {checker_key}", exact[checker_key], mean[mean_key], 5e-7)
    check("exact official checker N", exact["N"] == mean["N"] == EXPECTED_N, [exact["N"], mean["N"]], [95, 95])
    check("exact official checker verdict", checker["verdict"] == "PASS_ZERO_ERRORS_EXACT_COMMITTED_MEAN", checker["verdict"], "PASS_ZERO_ERRORS_EXACT_COMMITTED_MEAN")
    check("exact official checker distributed zero errors", checker["distributed_static_binary_run"]["zero_orbital_errors"] and checker["distributed_static_binary_run"]["zero_geocentric_errors"], checker["distributed_static_binary_run"], "both true")
    check("exact official checker fresh-build zero errors", checker["fresh_official_source_build_run"]["zero_orbital_errors"] and checker["fresh_official_source_build_run"]["zero_geocentric_errors"], checker["fresh_official_source_build_run"], "both true")
    check("exact official checker executable agreement", checker["static_and_fresh_build_outputs_identical"] is True, checker["static_and_fresh_build_outputs_identical"], True)

    candidate = load_json(CANDIDATE)
    final = load_json(FINAL)
    live = load_json(LIVE_MDC)
    linked = load_json(LINKED_EDMOND)

    gmn = candidate["gmn_evidence"]
    primary = final["primary_result"]
    check("candidate significant GMN membership", gmn["members_in_significant_years_2022_2026"] == EXPECTED_N, gmn["members_in_significant_years_2022_2026"], EXPECTED_N)
    check("final summary significant GMN membership", primary["confirmed_gmn_members"] == EXPECTED_N, primary["confirmed_gmn_members"], EXPECTED_N)
    check("candidate selected GMN total", gmn["deduplicated_selected_members_2019_2026"] == 101, gmn["deduplicated_selected_members_2019_2026"], 101)
    check("final selected GMN total", primary["deduplicated_selected_gmn_members_2019_2026"] == 101, primary["deduplicated_selected_gmn_members_2019_2026"], 101)

    novelty = candidate["novelty_audit"]
    live_cat = live["catalogue"]
    for key in ("iau_catalogue_version", "iau_catalogue_shower_records", "iau_solutions_parsed", "iau_catalogue_sha256"):
        live_key = {
            "iau_catalogue_version": "version",
            "iau_catalogue_shower_records": "parsed_shower_records",
            "iau_solutions_parsed": "parsed_solutions",
            "iau_catalogue_sha256": "sha256",
        }[key]
        check(f"candidate live MDC provenance {key}", novelty[key] == live_cat[live_key], novelty[key], live_cat[live_key])
        check(f"final live MDC provenance {key}", primary[key] == live_cat[live_key], primary[key], live_cat[live_key])
    for key in ("hard_iau_matches", "radiant_speed_activity_near_matches", "orbit_incomplete_near_matches"):
        live_key = {
            "hard_iau_matches": "hard_duplicate_match_count",
            "radiant_speed_activity_near_matches": "radiant_speed_activity_match_count",
            "orbit_incomplete_near_matches": "orbit_incomplete_near_match_count",
        }[key]
        check(f"candidate live MDC result {key}", novelty[key] == live[live_key] == 0, [novelty[key], live[live_key]], [0, 0])
        check(f"final live MDC result {key}", primary[key] == live[live_key] == 0, [primary[key], live[live_key]], [0, 0])

    candidate_edmond = candidate["independent_archive_evidence"]["currently_linked_edmond_annual_files"]
    final_edmond = final["supporting_edmond_evidence"]
    integrity = linked["release_integrity"]
    check("EDMOND complete release not tested", candidate_edmond["complete_advertised_release_tested"] is False and final_edmond["complete_advertised_release_tested"] is False and integrity["complete_advertised_release_tested"] is False, [candidate_edmond["complete_advertised_release_tested"], final_edmond["complete_advertised_release_tested"], integrity["complete_advertised_release_tested"]], [False, False, False])
    check("EDMOND selected members consistent", candidate_edmond["selected_members"] == final_edmond["members"] == linked["frozen_activity_test"]["selected_members"] == 6, [candidate_edmond["selected_members"], final_edmond["members"], linked["frozen_activity_test"]["selected_members"]], [6, 6, 6])
    check("EDMOND additional events consistent", candidate_edmond["additional_selected_events"] == final_edmond["additional_selected_events"] == 0, [candidate_edmond["additional_selected_events"], final_edmond["additional_selected_events"]], [0, 0])
    check("EDMOND linked rows consistent", candidate_edmond["currently_linked_rows_2001_2023"] == final_edmond["currently_linked_rows_2001_2023"] == integrity["currently_linked_rows_2001_2023"] == 481252, [candidate_edmond["currently_linked_rows_2001_2023"], final_edmond["currently_linked_rows_2001_2023"], integrity["currently_linked_rows_2001_2023"]], [481252] * 3)
    check("EDMOND advertised rows consistent", candidate_edmond["advertised_rows_2001_2023"] == final_edmond["advertised_rows_2001_2023"] == integrity["advertised_rows_2001_2023"] == 614758, [candidate_edmond["advertised_rows_2001_2023"], final_edmond["advertised_rows_2001_2023"], integrity["advertised_rows_2001_2023"]], [614758] * 3)

    phrase_checks = {
        "results current candidate claim": (RESULTS, "uncatalogued annual April meteor-stream candidate"),
        "results live catalogue boundary": (RESULTS, "zero hard duplicates and zero radiant–speed–activity near matches"),
        "results EDMOND integrity boundary": (RESULTS, "not the complete advertised v6.01 release"),
        "manuscript candidate claim": (MANUSCRIPT, "uncatalogued annual meteor-stream candidate"),
        "manuscript live catalogue version": (MANUSCRIPT, "catalogue version 2026-06-25"),
        "manuscript EDMOND integrity boundary": (MANUSCRIPT, "not represented as a complete v6.01 replication"),
        "checker report exact record": (CHECKER_REPORT, "peri=333.636995 node=37.157321 i=24.370030 N=95"),
        "checker report claim boundary": (CHECKER_REPORT, "does **not** validate shower novelty"),
        "README draft boundary": (README, "draft package"),
        "README no submission": (README, "Nothing has been submitted"),
        "checklist external review boundary": (CHECKLIST, "expert"),
    }
    for name, (path, text) in phrase_checks.items():
        check(name, phrase(path, text), text if phrase(path, text) else "missing", text)

    package_files = [
        LOOKUP, MEAN_JSON, LEGACY, CALC, CHECKER_SUMMARY, CHECKER_REPORT,
        LIVE_MDC, CANDIDATE, LINKED_EDMOND, FINAL, RESULTS, MANUSCRIPT,
        README, CHECKLIST,
    ]
    manifest = {
        str(path.relative_to(ROOT)): {
            "byte_count": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in package_files
    }

    failed = [item for item in checks if not item.passed]
    report = {
        "verdict": "PASS_MDC_PACKAGE_INTERNALLY_CONSISTENT" if not failed else "FAIL_MDC_PACKAGE_INCONSISTENT",
        "lookup_rows": len(rows),
        "recomputed_from_lookup": recomputed,
        "check_count": len(checks),
        "passed_checks": len(checks) - len(failed),
        "failed_checks": len(failed),
        "checks": [asdict(item) for item in checks],
        "manifest": manifest,
    }
    json_path = args.output_dir / "mdc_package_consistency_audit.json"
    json_path.write_text(json.dumps(report, indent=2) + "\n")

    md = [
        "# GhostStream MDC package consistency audit",
        "",
        f"**Verdict:** `{report['verdict']}`",
        "",
        f"- Checks: **{len(checks)}**",
        f"- Passed: **{len(checks) - len(failed)}**",
        f"- Failed: **{len(failed)}**",
        f"- Lookup rows: **{len(rows)}**",
        "",
        "## Recomputed lookup quantities",
        "",
        "```json",
        json.dumps(recomputed, indent=2),
        "```",
        "",
    ]
    if failed:
        md.extend(["## Failures", ""])
        for item in failed:
            md.append(f"- **{item.name}** — observed `{item.observed}`, expected `{item.expected}`, tolerance `{item.tolerance}`")
        md.append("")
    md.extend([
        "## Package hashes",
        "",
        "| File | Bytes | SHA-256 |",
        "|---|---:|---|",
    ])
    for name, values in manifest.items():
        md.append(f"| `{name}` | {values['byte_count']} | `{values['sha256']}` |")
    md.extend([
        "",
        "## Claim boundary",
        "",
        "This is an internal-consistency and provenance audit. It does not constitute IAU submission, official recognition, external scientific review, or a new independent replication.",
        "",
    ])
    (args.output_dir / "MDC_PACKAGE_CONSISTENCY_AUDIT.md").write_text("\n".join(md))

    print(json.dumps({
        "verdict": report["verdict"],
        "check_count": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "failure_names": [item.name for item in failed],
        "recomputed": recomputed,
        "json_report": str(json_path),
    }, indent=2))
    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
