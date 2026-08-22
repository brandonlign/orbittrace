"""Reveal OrbitTrace only against a frozen ACRF-v3.5 application artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd


def _timestamp_key(value: Any) -> str:
    digits = "".join(character for character in str(value) if character.isdigit())
    return digits[:14]


def _target_keys(target: Path, years: tuple[int, ...]) -> set[str]:
    frame = pd.read_csv(target)
    timestamps = pd.to_datetime(frame["Tobs"], format="%Y-%m-%d-%H:%M:%S", errors="coerce")
    return {
        value.strftime("%Y%m%d%H%M%S")
        for value in timestamps.dropna()
        if int(value.year) in years
    }


def run(artifact: Path, target: Path) -> dict[str, Any]:
    frozen_bytes = artifact.read_bytes()
    payload = json.loads(frozen_bytes)
    if payload.get("target_accessed_during_generation_ranking_or_membership") is not False:
        raise RuntimeError("artifact does not certify target-free generation")
    years = tuple(int(value) for value in payload["years"])
    target_ids = _target_keys(target, years)
    matches = []
    for candidate in payload["candidates"]:
        if "final_event_ids" not in candidate:
            continue
        reported = {_timestamp_key(value) for value in candidate["final_event_ids"]}
        overlap = len(reported & target_ids)
        if not overlap:
            continue
        precision = overlap / len(reported) if reported else 0.0
        recall = overlap / len(target_ids) if target_ids else 0.0
        f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
        matches.append(
            {
                "rank": int(candidate["global_rank"]),
                "family_id": candidate["family_id"],
                "scale": candidate.get("scale"),
                "hierarchy_method": candidate.get("hierarchy_method"),
                "membership_mode": candidate.get("membership_mode"),
                "core_member_count": int(candidate["member_count"]),
                "final_member_count": int(len(reported)),
                "target_count": int(len(target_ids)),
                "target_overlap": int(overlap),
                "precision": float(precision),
                "recall": float(recall),
                "f1": float(f1),
            }
        )
    matches.sort(key=lambda item: (-item["f1"], -item["target_overlap"], item["rank"]))
    best = matches[0] if matches else None
    gate_passed = bool(
        best
        and best["target_overlap"] == len(target_ids) == 95
        and best["precision"] >= 0.75
        and best["f1"] >= 0.85
        and best["rank"] <= 100
    )
    return {
        "stage": "acrf_v3_5_posthoc_orbittrace_reveal",
        "frozen_artifact": str(artifact),
        "frozen_artifact_sha256": hashlib.sha256(frozen_bytes).hexdigest(),
        "target": str(target),
        "target_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "target_accessed_after_frozen_ranking_and_membership": True,
        "target_count": int(len(target_ids)),
        "gate": {
            "required_overlap": 95,
            "minimum_precision": 0.75,
            "minimum_f1": 0.85,
            "maximum_rank": 100,
            "passed": gate_passed,
        },
        "best": best,
        "matches": matches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.artifact, args.target)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "reveal_v3_5.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(path), "gate": result["gate"], "best": result["best"]}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
