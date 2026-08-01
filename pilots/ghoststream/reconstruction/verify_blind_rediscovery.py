#!/usr/bin/env python3
"""Verify the recovered January–July 2026 blind discovery matrix.

The actual April lead was produced by the recovered arbitrary-year/month wrapper,
not by the separate 2025 all-season search. This verifier combines seven
independently executed monthly outputs, requires the April survivor near the
frozen discovery center, and checks its untouched 2025 and 2024 validation,
uncertainty-clone stability, and IAU novelty veto.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path
from typing import Any

SOURCE_COMMIT = "39972b5fe0cf4d47092d3caa2b3ced12bedb065e"
EXPECTED_CENTER = [-149.297555, 7.45007, 37.42224, 36.901963]
EXPECTED_SIGMA = [0.881190723, 0.579296298, 1.099081032, 1.329624591]
EXPECTED_ORBIT = [0.950783, 0.073747, 25.286643, 334.338586, 37.363391]
EXPECTED_MONTHS = tuple(range(1, 8))


def circular_delta(left: float, right: float) -> float:
    return (left - right + 180.0) % 360.0 - 180.0


def center_distance(candidate: list[float]) -> float:
    deltas = [
        circular_delta(float(candidate[0]), EXPECTED_CENTER[0]) / 3.5,
        (float(candidate[1]) - EXPECTED_CENTER[1]) / 3.0,
        (float(candidate[2]) - EXPECTED_CENTER[2]) / 2.5,
        circular_delta(float(candidate[3]), EXPECTED_CENTER[3]) / 2.5,
    ]
    return math.sqrt(sum(value * value for value in deltas))


def orbit_distance(candidate: list[float]) -> float:
    scales = [0.10, 0.10, 10.0, 20.0, 10.0]
    deltas = [
        float(candidate[0]) - EXPECTED_ORBIT[0],
        float(candidate[1]) - EXPECTED_ORBIT[1],
        float(candidate[2]) - EXPECTED_ORBIT[2],
        circular_delta(float(candidate[3]), EXPECTED_ORBIT[3]),
        circular_delta(float(candidate[4]), EXPECTED_ORBIT[4]),
    ]
    return math.sqrt(sum((delta / scale) ** 2 for delta, scale in zip(deltas, scales)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--search-root", type=Path, default=Path("ghoststream_blind_2026"))
    parser.add_argument("--output-dir", type=Path, default=Path("ghoststream_blind_rediscovery_evidence"))
    parser.add_argument("--environment", type=Path, default=Path("ghoststream_blind_environment.txt"))
    parser.add_argument("--source-hashes", type=Path, default=Path("ghoststream_blind_source_sha256.txt"))
    args = parser.parse_args()

    monthly: dict[int, dict[str, Any]] = {}
    all_candidates: list[dict[str, Any]] = []
    month_summaries: dict[str, Any] = {}
    iau_counts: list[int] = []
    for month in EXPECTED_MONTHS:
        path = args.search_root / f"2026-{month:02d}" / "ghoststream_novel_search.json"
        if not path.is_file():
            raise AssertionError(f"Missing 2026-{month:02d} blind-search output: {path}")
        result = json.loads(path.read_text(encoding="utf-8"))
        if int(result.get("discovery_year", -1)) != 2026:
            raise AssertionError(f"2026-{month:02d}: unexpected discovery year {result.get('discovery_year')}")
        if tuple(result.get("validation_years", [])) != (2025, 2024):
            raise AssertionError(f"2026-{month:02d}: unexpected validation years {result.get('validation_years')}")
        iau_count = int(result.get("iau_solutions_parsed", 0))
        if iau_count < 1500:
            raise AssertionError(f"2026-{month:02d}: IAU catalogue parse too small: {iau_count}")
        iau_counts.append(iau_count)
        candidates = result.get("candidates", [])
        for item in candidates:
            tagged = dict(item)
            tagged["source_month_output"] = month
            all_candidates.append(tagged)
        monthly[month] = result
        month_summaries[f"2026-{month:02d}"] = {
            "verdict": result.get("verdict"),
            "prevalidation_candidates": result.get("prevalidation_candidates"),
            "validated_candidates": result.get("validated_candidates"),
            "survivors": result.get("survivors"),
            "month_record": result.get("months", {}).get(f"2026-{month:02d}"),
        }

    survivors = [item for item in all_candidates if item.get("novel_discovery_gate_passed") is True]
    april_matches: list[tuple[float, dict[str, Any]]] = []
    for item in survivors:
        if int(item.get("month", -1)) != 4:
            continue
        distance = center_distance(item["center"])
        if distance <= 0.10:
            april_matches.append((distance, item))
    if not april_matches:
        summary = [
            {
                "month": item.get("month"),
                "center": item.get("center"),
                "distance_to_expected": center_distance(item["center"]),
            }
            for item in survivors
        ]
        raise AssertionError(f"No 2026 April survivor matched the frozen discovery center: {summary}")

    april_matches.sort(key=lambda pair: pair[0])
    center_error, candidate = april_matches[0]
    validation = candidate.get("validation", {})
    for year in ("2025", "2024"):
        item = validation.get(year)
        if item is None:
            raise AssertionError(f"April survivor missing validation year {year}")
        if item.get("passed") is not True:
            raise AssertionError(f"April survivor failed {year}: {item}")
        if int(item.get("members", 0)) < 8:
            raise AssertionError(f"April survivor has too few {year} members: {item}")
        if float(item.get("p", 1.0)) > 0.01:
            raise AssertionError(f"April survivor failed {year} source-preserving p-value: {item}")
    clones = candidate.get("clone_stability", {})
    if clones.get("passed") is not True or float(clones.get("pass_fraction", 0.0)) < 0.80:
        raise AssertionError(f"April survivor failed clone stability: {clones}")
    nearest = candidate.get("nearest_iau", {})
    if nearest.get("matched") is True:
        raise AssertionError(f"April survivor matched an IAU solution: {nearest}")

    non_april_survivors = [
        {"month": item.get("month"), "cluster": item.get("cluster"), "center": item.get("center")}
        for item in survivors
        if item is not candidate and int(item.get("month", -1)) != 4
    ]
    if non_april_survivors:
        raise AssertionError(
            "January–July 2026 scan produced additional full-gate survivors that "
            f"require scientific review: {non_april_survivors}"
        )

    center_deltas = [
        circular_delta(candidate["center"][0], EXPECTED_CENTER[0]),
        float(candidate["center"][1]) - EXPECTED_CENTER[1],
        float(candidate["center"][2]) - EXPECTED_CENTER[2],
        circular_delta(candidate["center"][3], EXPECTED_CENTER[3]),
    ]
    sigma_deltas = [float(value) - expected for value, expected in zip(candidate["sigma_raw"], EXPECTED_SIGMA)]
    orbit_error = orbit_distance(candidate["orbit_medoid"])

    output = args.output_dir
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree(args.search_root, output / "blind_search_2026")
    shutil.copy2(args.environment, output / "environment.txt")
    shutil.copy2(args.source_hashes, output / "source_sha256.txt")

    evidence: dict[str, Any] = {
        "status": "EXACT_2026_BLIND_REDISCOVERY",
        "source_repository": "brandonlign/remotion-worker",
        "source_commit": SOURCE_COMMIT,
        "entrypoint": "ghoststream_novel/run_month_year_v3.py",
        "discovery_year": 2026,
        "months_scanned": list(EXPECTED_MONTHS),
        "validation_years": [2025, 2024],
        "iau_solutions_parsed_range": [min(iau_counts), max(iau_counts)],
        "month_summaries": month_summaries,
        "full_gate_survivors_across_matrix": len(survivors),
        "additional_non_april_survivors": non_april_survivors,
        "april_survivor": {
            "cluster": candidate.get("cluster"),
            "discovery_members": candidate.get("members_2025"),
            "center": candidate["center"],
            "expected_center": EXPECTED_CENTER,
            "center_deltas": center_deltas,
            "normalized_center_distance": center_error,
            "sigma_raw": candidate["sigma_raw"],
            "expected_sigma": EXPECTED_SIGMA,
            "sigma_deltas": sigma_deltas,
            "orbit_medoid": candidate["orbit_medoid"],
            "expected_orbit_medoid": EXPECTED_ORBIT,
            "diagnostic_normalized_orbit_distance": orbit_error,
            "discovery_nights": candidate.get("nights_2025"),
            "discovery_stations": candidate.get("stations_2025"),
            "orbit_median_d": candidate.get("orbit_median_d"),
            "orbit_q90_d": candidate.get("orbit_q90_d"),
            "orbit_null": candidate.get("orbit_null"),
            "validation": validation,
            "clone_stability": clones,
            "nearest_iau": nearest,
        },
    }
    files = []
    for path in sorted(item for item in output.rglob("*") if item.is_file()):
        files.append({
            "path": path.relative_to(output).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    evidence["files"] = files
    (output / "blind_rediscovery.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# GhostStream January–July 2026 blind rediscovery",
        "",
        "**Verdict:** `EXACT_2026_BLIND_REDISCOVERY`",
        "",
        f"The recovered arbitrary-year/month scanner was run from immutable commit `{SOURCE_COMMIT}` for every month from January through July 2026. Each monthly search used the two prior years, 2025 and 2024, for validation.",
        "",
        f"- Months scanned: **7**",
        f"- Full-gate survivors across the matrix: **{len(survivors)}**",
        f"- Additional non-April survivors: **{len(non_april_survivors)}**",
        f"- April survivor cluster: **{candidate.get('cluster')}**",
        f"- April 2026 discovery members: **{candidate.get('members_2025')}**",
        f"- Center normalized distance from frozen discovery record: **{center_error:.12g}**",
        f"- 2025 validation: **{validation['2025']['members']} members, p={validation['2025']['p']:.6g}**",
        f"- 2024 validation: **{validation['2024']['members']} members, p={validation['2024']['p']:.6g}**",
        f"- Clone pass fraction: **{clones['pass_fraction']:.3f}**",
        f"- IAU match veto: **{nearest.get('matched')}**",
        "",
        "This is the recovered discovery lineage for the April candidate. The separate 2025 all-season search is retained as a negative/other-candidate result and is not misidentified as the April discovery run.",
        "",
    ]
    (output / "BLIND_REDISCOVERY.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(evidence["april_survivor"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
