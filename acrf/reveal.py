"""Compare a target-free ACRF artifact with a canonical target table."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd


def timestamp_key(value: Any) -> str:
    return "".join(character for character in str(value) if character.isdigit())[:14]


def target_keys(path: Path) -> set[str]:
    frame = pd.read_csv(path)
    column = "Tobs" if "Tobs" in frame else "timestamp_key"
    return {timestamp_key(value) for value in frame[column].dropna()}


def run(artifact: Path, target: Path) -> dict[str, Any]:
    payload_bytes = artifact.read_bytes()
    payload = json.loads(payload_bytes)
    if payload.get("target_accessed_during_generation_or_ranking") is not False and payload.get(
        "target_accessed_during_generation_ranking_or_membership"
    ) is not False:
        raise ValueError("artifact does not certify target-free generation")
    target_set = target_keys(target)
    matches = []
    for candidate in payload.get("candidates", []):
        reported = {timestamp_key(value) for value in candidate.get("final_event_ids", [])}
        overlap = len(reported & target_set)
        if not overlap:
            continue
        precision = overlap / len(reported) if reported else 0.0
        recall = overlap / len(target_set) if target_set else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        matches.append({
            "rank": int(candidate.get("global_rank", candidate.get("rank", 0))),
            "family_id": candidate["family_id"],
            "reported_members": len(reported),
            "target_overlap": overlap,
            "target_count": len(target_set),
            "precision": precision,
            "recall": recall,
            "f1": f1,
        })
    matches.sort(key=lambda item: (-item["f1"], -item["target_overlap"], item["rank"]))
    return {
        "stage": "acrf_posthoc_target_reveal",
        "artifact_sha256": hashlib.sha256(payload_bytes).hexdigest(),
        "target_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "target_count": len(target_set),
        "best": matches[0] if matches else None,
        "matches": matches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.artifact, args.target)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["best"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
