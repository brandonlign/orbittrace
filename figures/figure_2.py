"""Regenerate Figure 2: annual GMN and external archive membership."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    annual = pd.read_csv("data/derived/annual_membership.csv")
    external = {"CAMS": len(pd.read_csv("data/derived/cams_match_table.csv")), "SonotaCo": len(pd.read_csv("data/derived/sonotaco_match_table.csv")), "EDMOND": len(pd.read_csv("data/derived/edmond_match_table.csv"))}
    fig, axes = plt.subplots(1, 2, figsize=(9, 4), constrained_layout=True)
    axes[0].bar(annual["year"].astype(str), annual["members"], color="#4267a8")
    axes[0].set(xlabel="Year", ylabel="Canonical members", title="GMN confirmation")
    axes[1].bar(list(external), list(external.values()), color=["#bf6b3f", "#4f8a65", "#8b6ba8"])
    axes[1].set(xlabel="Archive", ylabel="Matched members", title="External archive matches")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=180)
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
