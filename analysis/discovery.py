"""Validate the target-free ACRF discovery result."""
from __future__ import annotations
import argparse
from pathlib import Path
from common import read_json, write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    meta = read_json("data/derived/acrf_baseline_metadata.json")
    write_stage(args.out, "orbittrace_discovery", [
        "data/derived/acrf_discovery_family_123.csv",
        "data/derived/acrf_baseline_metadata.json",
        "configs/method.json",
    ], {"rank": meta["rank"], "reported_members": meta["reported_members"], "target_overlap": meta["target_overlap"], "precision": meta["precision"], "recall": meta["recall"], "f1": meta["f1"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
