"""Report the NOP-004 population-level comparison."""
from __future__ import annotations
import argparse
from pathlib import Path
from common import read_json, write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = read_json("results/mdc_duplicate_screen.json")
    write_stage(args.out, "nop004_population_comparison", ["results/mdc_duplicate_screen.json", "data/derived/canonical_95.csv"], result["population_followup"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
