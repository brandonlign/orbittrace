"""Regenerate Figure 3: frozen core-hyperparameter robustness."""
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
    data = pd.read_csv("results/acrf_core_hyperparameter_robustness.csv")
    fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
    tracked = data[data["tracked"] == True]
    ax.scatter(tracked["rank"], tracked["final_overlap"], c=tracked["final_f1"], cmap="plasma", s=22, alpha=0.8)
    ax.axvline(100, color="black", linestyle="--", linewidth=0.8)
    ax.axhline(95, color="black", linestyle=":", linewidth=0.8)
    ax.set(xscale="log", xlabel="Tracked rank (log scale)", ylabel="Canonical overlap", title="ACRF core-hyperparameter robustness")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=180)
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
