"""Report the CAMS, SonotaCo, and EDMOND archive comparisons."""
from __future__ import annotations
import argparse
from pathlib import Path
from common import read_json, write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = read_json("results/external_replication.json")
    write_stage(args.out, "external_archive_replication", ["results/external_replication.json", "configs/external_replication.json", "data/derived/cams_match_table.csv", "data/derived/sonotaco_match_table.csv", "data/derived/edmond_match_table.csv"], {"verdict": result.get("verdict"), "independent_networks_passing": result.get("independent_networks_passing"), "catalog_coverage": result.get("catalog_coverage")})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
