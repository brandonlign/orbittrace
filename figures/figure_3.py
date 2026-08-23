"""Regenerate Figure 3: independent and catalogue evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plot_style import COLORS, clean_axes, configure, panel_label, save_figure


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
OUT = ROOT / "figures" / "generated"


def panel_interval(ax: plt.Axes, comparison: dict) -> None:
    bars = [
        ("OrbitTrace", comparison["orbittrace_interval_deg"], COLORS["blue"]),
        ("NOP-004", comparison["nop004_interval_deg"], COLORS["gray"]),
    ]
    for y, (label, bounds, color) in enumerate(bars):
        lo, hi = bounds
        ax.plot([lo, hi], [y, y], color=color, lw=5, solid_capstyle="butt")
        ax.plot([lo, hi], [y, y], color=COLORS["ink"], lw=0.55, solid_capstyle="butt")
        ax.text((lo + hi) / 2, y + 0.16, f"{lo:.2f}-{hi:.2f}°", ha="center", va="bottom", fontsize=7, color=COLORS["ink"])
    ax.set_yticks([0, 1], ["OrbitTrace", "NOP-004"])
    ax.set_xlim(30, 80)
    ax.set_ylim(-0.55, 1.5)
    ax.set_xlabel("Activity interval in solar longitude, λ⊙ (deg)")
    ax.set_title("Activity intervals", loc="left")
    clean_axes(ax, grid=False)
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.45, alpha=0.6)


def panel_radiant_separation(ax: plt.Axes, comparison: dict) -> None:
    values = np.array([
        comparison["nop004_radiant_separation_deg"] / comparison["duplicate_radiant_gate_deg"],
        comparison["nop004_speed_difference_km_s"] / comparison["duplicate_speed_gate_km_s"],
    ])
    labels = ["Radiant", "Speed"]
    colors = [COLORS["red"], COLORS["gold"]]
    ax.barh([1, 0], values, color=colors, edgecolor=COLORS["ink"], linewidth=0.7, height=0.52)
    for y, value in zip([1, 0], values):
        ax.text(value + 0.035, y, f"{value:.2f}×", va="center", fontsize=7.5)
    ax.axvline(1.0, color=COLORS["ink"], ls=(0, (3, 2)), lw=0.8)
    ax.set_yticks([1, 0], labels)
    ax.set_xlim(0, 2.25)
    ax.set_xlabel("Separation / fixed duplicate threshold")
    ax.set_title("Radiant and speed separation", loc="left")
    clean_axes(ax)


def panel_orbit_population(ax: plt.Axes, comparison: dict) -> None:
    values = [
        comparison["nop_population_nn_dsh_99th_percentile"],
        comparison["closest_orbittrace_nop_dsh"],
        comparison["median_orbittrace_nop_dsh"],
    ]
    labels = ["NOP internal 99th pct.", "Nearest OT–NOP", "Median OT–NOP"]
    colors = [COLORS["gray"], COLORS["red"], COLORS["blue"]]
    y = np.arange(len(values))
    ax.hlines(y, 0, values, color=colors, linewidth=2.7)
    ax.scatter(values, y, color=colors, edgecolor=COLORS["ink"], linewidth=0.6, s=32, zorder=3)
    for yy, value in zip(y, values):
        ax.text(value + 0.006, yy, f"{value:.4f}", va="center", fontsize=7)
    ax.axvline(0.15, color=COLORS["red"], ls=(0, (3, 2)), lw=0.8)
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 0.205)
    ax.set_xlabel(r"Southworth–Hawkins $D_{\rm SH}$")
    ax.set_title("Orbital separation", loc="left")
    clean_axes(ax)


def panel_timeline(ax: plt.Axes) -> None:
    sources = {
        "CAMS": (DATA / "cams_match_table.csv", COLORS["blue"], "o"),
        "SonotaCo": (DATA / "sonotaco_match_table.csv", COLORS["green"], "s"),
        "EDMOND": (DATA / "edmond_match_table.csv", COLORS["gray"], "^"),
    }
    y_positions = {"CAMS": 2, "SonotaCo": 1, "EDMOND": 0}
    for source, (path, color, marker) in sources.items():
        table = pd.read_csv(path)
        rng = np.random.default_rng(20260822 + y_positions[source])
        y = y_positions[source] + rng.normal(0, 0.045, len(table))
        ax.scatter(table["year"], y, color=color, marker=marker, s=28, edgecolor="white", linewidth=0.45)
    ax.set_yticks([0, 1, 2], ["EDMOND (4)", "SonotaCo (11)", "CAMS (9)"])
    ax.set_xlim(2005, 2027)
    ax.set_xticks([2005, 2010, 2015, 2020, 2025])
    ax.set_ylim(-0.5, 2.5)
    ax.set_xlabel("Observation year")
    ax.set_title("External matches by year", loc="left")
    clean_axes(ax, grid=False)
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.45, alpha=0.6)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="optional output image path")
    args = parser.parse_args()
    configure()
    comparison = json.loads((DATA / "nop004_comparison.json").read_text())
    fig, axes = plt.subplots(2, 2, figsize=(7.35, 6.35))
    fig.subplots_adjust(left=0.12, right=0.985, bottom=0.12, top=0.91, wspace=0.38, hspace=0.34)
    panel_interval(axes[0, 0], comparison)
    panel_radiant_separation(axes[0, 1], comparison)
    panel_orbit_population(axes[1, 0], comparison)
    panel_timeline(axes[1, 1])
    for ax, label in zip(axes.flat, "ABCD"):
        panel_label(ax, label)
    if args.out:
        save_figure(fig, args.out.parent, args.out.stem)
    else:
        save_figure(fig, OUT, "figure3_catalogue_evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
