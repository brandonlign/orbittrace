"""Report the source-matched orbital null."""
from __future__ import annotations
import argparse
from pathlib import Path
from common import read_json, write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    summary = read_json("results/paper_headline_results.json")
    write_stage(args.out, "orbital_null", ["results/paper_headline_results.json"], summary["orbital_null"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
