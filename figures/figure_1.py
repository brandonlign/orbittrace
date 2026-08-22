"""Regenerate Figure 1: canonical members across solar longitude."""
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
    data = pd.read_csv("data/derived/canonical_95.csv")
    years = pd.to_datetime(data["Tobs"]).dt.year
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    scatter = axes[0].scatter(data["LS"], data["RA"], c=years, cmap="viridis", s=20, alpha=0.85)
    axes[0].set(xlabel="Solar longitude (deg)", ylabel="Geocentric RA (deg)", title="Canonical members")
    fig.colorbar(scatter, ax=axes[0], label="Year")
    axes[1].scatter(data["LS"], data["VG"], c=years, cmap="viridis", s=20, alpha=0.85)
    axes[1].set(xlabel="Solar longitude (deg)", ylabel="Geocentric speed (km/s)", title="Radiant-speed recurrence")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=180)
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
