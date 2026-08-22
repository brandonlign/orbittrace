"""Report the source-preserving and shifted-window activity nulls."""
from __future__ import annotations
import argparse
from pathlib import Path
from common import read_json, write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    summary = read_json("results/paper_headline_results.json")
    write_stage(args.out, "activity_null", ["results/paper_headline_results.json"], summary["activity_null"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
