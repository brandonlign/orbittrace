"""Report the JPL parent-body screen."""
from __future__ import annotations
import argparse
from pathlib import Path
from common import read_json, write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = read_json("results/paper_headline_results.json")
    write_stage(args.out, "jpl_parent_body_screen", ["results/paper_headline_results.json", "configs/external_replication.json"], result["jpl_parent_body_screen"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
