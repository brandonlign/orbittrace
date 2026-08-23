"""Regenerate Figure 2: geographic and specification robustness."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plot_style import COLORS, clean_axes, configure, panel_label, save_figure


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
RESULTS = ROOT / "results"
OUT = ROOT / "figures" / "generated"


def panel_geographic(ax: plt.Axes) -> None:
    data = pd.read_csv(DATA / "geographic_replication.csv")
    labels = ["Americas", "Europe + W Asia", "Oceania + E Asia + Africa"]
    y = np.arange(len(data))
    bars = ax.barh(y, data["members"], color=COLORS["blue"], edgecolor=COLORS["ink"], linewidth=0.7, height=0.62)
    for bar, count in zip(bars, data["members"]):
        ax.text(float(count) + 0.8, bar.get_y() + bar.get_height() / 2, str(int(count)),
                ha="left", va="center", fontsize=7, color=COLORS["ink"])
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 53)
    ax.set_xlabel("Region-selected members")
    ax.set_title("Geographic replication", loc="left")
    clean_axes(ax)


def panel_core_robustness(ax: plt.Axes) -> None:
    data = pd.read_csv(RESULTS / "acrf_core_hyperparameter_robustness.csv")
    target_counts = data["target_count"].astype(int).unique()
    if len(target_counts) != 1 or target_counts[0] != 95:
        raise ValueError(f"expected one 95-member reference target, found {target_counts.tolist()}")
    target_count = int(target_counts[0])
    data["overlap_percent"] = 100.0 * data["final_overlap"] / target_count
    materialized = data["within_top100"].astype(bool).to_numpy()
    data["group"] = data["grid_sources"].map({
        "joint_extreme_interactions": "joint extremes",
        "scale_factorial": "physical scales",
        "hdbscan_factorial": "HDBSCAN settings",
        "hdbscan_factorial+scale_factorial": "baseline",
    }).fillna(data["grid_sources"])
    palette = {
        "joint extremes": COLORS["red"],
        "physical scales": COLORS["purple"],
        "HDBSCAN settings": COLORS["green"],
        "baseline": COLORS["blue"],
    }
    markers = {
        "joint extremes": "o",
        "physical scales": "s",
        "HDBSCAN settings": "^",
        "baseline": "D",
    }
    for group, subset in data.groupby("group", sort=False):
        color = palette.get(group, COLORS["gray"])
        selected = subset[subset["within_top100"].astype(bool)]
        ax.scatter(selected["setting_index"], selected["overlap_percent"], s=20,
                   color=color, alpha=0.86, marker=markers.get(group, "o"),
                   edgecolor="white", linewidth=0.3, label=group)
    baseline = data[data["setting_index"] == 76].iloc[0]
    ax.scatter([baseline["setting_index"]], [baseline["overlap_percent"]], s=70, marker="*", facecolor="white",
               edgecolor=COLORS["ink"], linewidth=0.9, zorder=5)
    ax.axhline(100.0, color=COLORS["muted"], ls=(0, (3, 2)), lw=0.7)
    ax.text(152.5, 100.0, "100% (95/95)", ha="right", va="bottom", fontsize=6.7, color=COLORS["muted"])
    ax.text(88, 20.0,
            f"post-ranking: 153/153 tracked\n{int(materialized.sum())}/153 top-100; 81/81 validation",
            ha="left", va="bottom", fontsize=6.5, color=COLORS["ink"])

    ax.set_xlim(-3, 155)
    ax.set_ylim(0, 110)
    ax.set_xlabel("Frozen parameter-setting index")
    ax.set_ylabel("Canonical overlap (%)")
    ax.set_title("ACRF core robustness", loc="left")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 0.02), ncol=2, fontsize=6.0, handletextpad=0.3, columnspacing=0.6)
    clean_axes(ax)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="optional output image path")
    args = parser.parse_args()
    configure()
    fig, axes = plt.subplots(1, 2, figsize=(7.35, 3.55))
    fig.subplots_adjust(left=0.13, right=0.985, bottom=0.22, top=0.87, wspace=0.36)
    panel_geographic(axes[0])
    panel_core_robustness(axes[1])
    for ax, label in zip(axes, "AB"):
        panel_label(ax, label)
    if args.out:
        save_figure(fig, args.out.parent, args.out.stem)
    else:
        save_figure(fig, OUT, "figure2_robustness")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
