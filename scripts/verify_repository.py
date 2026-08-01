#!/usr/bin/env python3
"""Verify the final GhostStream repository structure and frozen result metadata."""

from __future__ import annotations

import compileall
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    ROOT / "RESULTS.md",
    ROOT / "requirements.txt",
    ROOT / "pipeline" / "SOURCE_MANIFEST.json",
    ROOT / "pipeline" / "pr57_novel" / "run_novel_search.py",
    ROOT / "pipeline" / "pr57_novel" / "validate_april_candidate.py",
    ROOT / "candidate" / "candidate_solution.json",
    ROOT / "candidate" / "mdc" / "GhostStream_April_95_GMN_lookup.csv",
    ROOT / "validation" / "exact_recovered" / "exact_reproduction.json",
    ROOT / "validation" / "exact_blind_rediscovery" / "blind_rediscovery.json",
    ROOT / "results" / "ghoststream_final_summary.json",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"Expected a JSON object: {path}")
    return value


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.is_file()]
    if missing:
        raise SystemExit("Missing required files:\n- " + "\n- ".join(missing))

    candidate = load_json(ROOT / "candidate" / "candidate_solution.json")
    summary = load_json(ROOT / "results" / "ghoststream_final_summary.json")
    reproduction = load_json(
        ROOT / "validation" / "exact_recovered" / "exact_reproduction.json"
    )
    blind = load_json(
        ROOT / "validation" / "exact_blind_rediscovery" / "blind_rediscovery.json"
    )

    assert candidate["internal_id"] == "GhostStream-April-36.9"
    assert candidate["official_iau_designation"] is None
    assert summary["primary_result"]["confirmed_gmn_members"] == 95
    assert summary["primary_result"]["hard_iau_matches"] == 0
    assert reproduction["status"] == "EXACT_REPRODUCTION"
    assert blind["status"] == "EXACT_2026_BLIND_REDISCOVERY"
    assert blind["full_gate_survivors_across_matrix"] == 1

    if not compileall.compile_dir(ROOT / "pipeline", quiet=1):
        raise SystemExit("Python compilation failed under pipeline/")

    print("GhostStream repository verification passed.")
    print("Scientific status: high-confidence candidate; independent review pending.")


if __name__ == "__main__":
    main()
