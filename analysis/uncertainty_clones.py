"""Report the trajectory-uncertainty clone audit."""
from __future__ import annotations
import argparse
from pathlib import Path
from common import read_json, write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    summary = read_json("results/paper_headline_results.json")
    write_stage(args.out, "uncertainty_clones", ["results/paper_headline_results.json", "data/derived/canonical_95.csv"], summary["uncertainty_clones"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
