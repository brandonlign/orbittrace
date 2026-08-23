"""Summarize the 81-setting nearby validation sensitivity."""
from __future__ import annotations
import argparse
from pathlib import Path
from common import read_json, write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    summary = read_json("results/paper_headline_results.json")
    write_stage(args.out, "81_setting_validation_sensitivity", ["results/paper_headline_results.json", "configs/validation_thresholds.json"], summary["validation_sensitivity"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
