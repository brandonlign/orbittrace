"""Validate and summarize the fair comparator results."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from comparators import literature_comparator_registry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(Path("benchmarks/benchmark_results.json").read_text())
    controls = json.loads(Path("benchmarks/known_shower_controls.json").read_text())
    summary = {
        "stage": "fair_benchmarks",
        "comparators": [item.__dict__ for item in literature_comparator_registry()],
        "literature_verdict": result.get("verdict"),
        "expanded_verdict": result.get("expanded_verdict"),
        "known_shower_control_verdict": controls.get("verdict", controls.get("status")),
        "scope": "ACRF, Sugar, catalogue-HDBSCAN, independent D-criterion, and three known-shower controls",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
