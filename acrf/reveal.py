"""Compare a target-free ACRF artifact with a canonical target table."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd


TARGET_FREE_FIELDS = (
    "target_accessed_during_generation_or_ranking",
    "target_accessed_during_generation_ranking_or_membership",
)


def timestamp_key(value: Any) -> str:
    digits = "".join(character for character in str(value) if character.isdigit())
    return digits[:14]


def _validated_timestamp_key(value: Any, *, source: str) -> str:
    key = timestamp_key(value)
    if len(key) != 14:
        raise ValueError(f"{source} contains a value without a 14-digit timestamp: {value!r}")
    return key


def target_keys(path: Path) -> set[str]:
    frame = pd.read_csv(path)
    if "Tobs" in frame.columns:
        column = "Tobs"
    elif "timestamp_key" in frame.columns:
        column = "timestamp_key"
    else:
        raise ValueError("target table must contain Tobs or timestamp_key")

    keys = {
        _validated_timestamp_key(value, source="target table")
        for value in frame[column].dropna()
    }
    if not keys:
        raise ValueError("target table contains no valid timestamps")
    if len(keys) != int(frame[column].notna().sum()):
        raise ValueError("target table contains duplicate timestamps")
    return keys


def _certify_target_free(payload: dict[str, Any]) -> None:
    present = [payload[field] for field in TARGET_FREE_FIELDS if field in payload]
    if not present:
        raise ValueError("artifact does not contain a target-access certification field")
    if any(value is True for value in present) or not any(value is False for value in present):
        raise ValueError("artifact does not certify target-free generation")


def run(artifact: Path, target: Path) -> dict[str, Any]:
    payload_bytes = artifact.read_bytes()
    payload = json.loads(payload_bytes)
    if not isinstance(payload, dict):
        raise ValueError("artifact must be a JSON object")
    _certify_target_free(payload)

    target_set = target_keys(target)
    matches = []
    for candidate in payload.get("candidates", []):
        raw_ids = candidate.get("final_event_ids", [])
        reported = {
            _validated_timestamp_key(value, source="candidate final_event_ids")
            for value in raw_ids
        }
        if len(reported) != len(raw_ids):
            raise ValueError("candidate final_event_ids contain duplicate timestamps")

        overlap = len(reported & target_set)
        if not overlap:
            continue
        precision = overlap / len(reported) if reported else 0.0
        recall = overlap / len(target_set)
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        matches.append(
            {
                "rank": int(candidate.get("global_rank", candidate.get("rank", 0))),
                "family_id": candidate["family_id"],
                "reported_members": len(reported),
                "target_overlap": overlap,
                "target_count": len(target_set),
                "precision": precision,
                "recall": recall,
                "f1": f1,
            }
        )
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
