"""Report the exhaustive MDC duplicate screen."""
from __future__ import annotations
import argparse
from pathlib import Path
from common import read_json, write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = read_json("results/mdc_duplicate_screen.json")
    write_stage(args.out, "exhaustive_mdc_duplicate_screen", ["results/mdc_duplicate_screen.json", "configs/validation_thresholds.json"], {"current_catalogue_rows": result["catalogue"]["submitted_rows_screened"], "previous_snapshot_rows": result["previous_snapshot_crosscheck"]["submitted_solutions"], "hard_duplicate_matches": result["hard_duplicate_matches"], "nearest_complete_orbit": result["nearest_complete_orbit"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
