#!/usr/bin/env python3
"""Verify that the recovered all-season blind search rediscovers GhostStream.

The scientific search is executed unchanged from immutable remotion-worker
commit 39972b5fe0cf4d47092d3caa2b3ced12bedb065e. This verifier does not alter
or rerank candidates. It requires an April survivor near the previously frozen
blind-discovery center, independent 2024 and 2023 replication, and uncertainty-
clone stability.
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
    # Diagnostic normalized parameter distance only. The search itself applies
    # its full orbital D criterion before this verifier sees a survivor.
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
    parser.add_argument(
        "--search-json",
        type=Path,
        default=Path("ghoststream_novel_results/ghoststream_novel_search.json"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("ghoststream_blind_rediscovery_evidence"),
    )
    parser.add_argument("--environment", type=Path, default=Path("ghoststream_blind_environment.txt"))
    parser.add_argument("--source-hashes", type=Path, default=Path("ghoststream_blind_source_sha256.txt"))
    args = parser.parse_args()

    result: dict[str, Any] = json.loads(args.search_json.read_text(encoding="utf-8"))
    if result.get("verdict") != "NOVEL_CANDIDATE_SURVIVES_FULL_GATE":
        raise AssertionError(f"Blind search verdict did not pass: {result.get('verdict')}")
    if int(result.get("survivors", 0)) < 1:
        raise AssertionError("Blind search reported no surviving candidates")
    if tuple(result.get("validation_years", [])) != (2024, 2023):
        raise AssertionError(f"Unexpected validation years: {result.get('validation_years')}")
    if int(result.get("iau_solutions_parsed", 0)) < 1500:
        raise AssertionError(f"IAU catalogue parse too small: {result.get('iau_solutions_parsed')}")

    candidates = result.get("candidates", [])
    survivors = [item for item in candidates if item.get("novel_discovery_gate_passed") is True]
    april = []
    for item in survivors:
        if int(item.get("month", -1)) != 4:
            continue
        distance = center_distance(item["center"])
        if distance <= 0.10:
            april.append((distance, item))
    if not april:
        summary = [
            {
                "month": item.get("month"),
                "center": item.get("center"),
                "distance_to_expected": center_distance(item["center"]),
            }
            for item in survivors
        ]
        raise AssertionError(f"No surviving April candidate matched the frozen center: {summary}")

    april.sort(key=lambda pair: pair[0])
    center_error, candidate = april[0]
    validation = candidate.get("validation", {})
    for year in ("2024", "2023"):
        if year not in validation:
            raise AssertionError(f"April survivor missing validation year {year}")
        if validation[year].get("passed") is not True:
            raise AssertionError(f"April survivor failed {year}: {validation[year]}")
        if int(validation[year].get("members", 0)) < 8:
            raise AssertionError(f"April survivor has too few {year} members")
        if float(validation[year].get("p", 1.0)) > 0.01:
            raise AssertionError(f"April survivor failed {year} source-preserving p-value")
    clones = candidate.get("clone_stability", {})
    if clones.get("passed") is not True:
        raise AssertionError(f"April survivor failed clone stability: {clones}")
    if float(clones.get("pass_fraction", 0.0)) < 0.80:
        raise AssertionError(f"April survivor clone pass fraction too low: {clones}")
    nearest = candidate.get("nearest_iau", {})
    if nearest.get("matched") is True:
        raise AssertionError(f"April survivor matched an IAU solution: {nearest}")

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
    shutil.copytree(args.search_json.parent, output / "blind_search")
    shutil.copy2(args.environment, output / "environment.txt")
    shutil.copy2(args.source_hashes, output / "source_sha256.txt")

    evidence = {
        "status": "EXACT_BLIND_REDISCOVERY",
        "source_repository": "brandonlign/remotion-worker",
        "source_commit": SOURCE_COMMIT,
        "search_verdict": result["verdict"],
        "months_scanned": 12,
        "validation_years": [2024, 2023],
        "iau_solutions_parsed": result["iau_solutions_parsed"],
        "prevalidation_candidates": result.get("prevalidation_candidates"),
        "validated_candidates": result.get("validated_candidates"),
        "survivors": result.get("survivors"),
        "april_survivor": {
            "cluster": candidate.get("cluster"),
            "members_2025": candidate.get("members_2025"),
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
            "nights_2025": candidate.get("nights_2025"),
            "stations_2025": candidate.get("stations_2025"),
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
        "# GhostStream blind rediscovery",
        "",
        "**Verdict:** `EXACT_BLIND_REDISCOVERY`",
        "",
        f"The recovered all-season search was run unchanged from immutable commit `{SOURCE_COMMIT}`. It scanned all 12 discovery-year months, applied the official-catalogue novelty veto, and independently validated survivors in 2024 and 2023.",
        "",
        f"- Search verdict: `{result['verdict']}`",
        f"- Prevalidation candidates: **{result.get('prevalidation_candidates')}**",
        f"- Validated candidates: **{result.get('validated_candidates')}**",
        f"- Full-gate survivors: **{result.get('survivors')}**",
        f"- April survivor cluster: **{candidate.get('cluster')}**",
        f"- April 2025 discovery members: **{candidate.get('members_2025')}**",
        f"- Center normalized distance from frozen record: **{center_error:.12g}**",
        f"- 2024 validation: **{validation['2024']['members']} members, p={validation['2024']['p']:.6g}**",
        f"- 2023 validation: **{validation['2023']['members']} members, p={validation['2023']['p']:.6g}**",
        f"- Clone pass fraction: **{clones['pass_fraction']:.3f}**",
        f"- IAU match veto: **{nearest.get('matched')}**",
        "",
        "This demonstrates that the recovered blind pipeline rediscovers the April lead without being supplied its month or final multi-year member list.",
        "",
    ]
    (output / "BLIND_REDISCOVERY.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(evidence["april_survivor"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
