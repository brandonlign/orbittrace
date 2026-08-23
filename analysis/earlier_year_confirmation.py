"""Report the annual confirmation counts."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from common import write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    table = pd.read_csv("data/derived/annual_membership.csv")
    write_stage(args.out, "earlier_year_confirmation", ["data/derived/canonical_95.csv", "data/derived/annual_membership.csv"], {"annual_counts": {str(row.year): int(row.members) for row in table.itertuples()}, "confirmed_members": int(table.members.sum()), "confirmation_years": [2022, 2023]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
