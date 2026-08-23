"""Regenerate Figure 1: physical detection and recurrence."""
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


def panel_activity(ax: plt.Axes) -> None:
    activity = pd.read_csv(DATA / "activity_profile_year_summary.csv")
    metadata = json.loads((DATA / "activity_profile_metadata.json").read_text())
    interval_lo, interval_hi = metadata["supported_interval_deg"]
    colors = [COLORS["blue"], COLORS["red"], COLORS["green"], COLORS["purple"], COLORS["gold"]]
    markers = ["o", "s", "^", "D", "P"]
    line_styles = ["-", "--", ":", "-.", (0, (5, 1))]
    x_outside = 0.0
    x_inside = 1.0
    offsets = np.linspace(-0.12, 0.12, len(activity))
    for color, marker, line_style, offset, (_, row) in zip(colors, markers, line_styles, offsets, activity.iterrows()):
        outside = float(row["outside_rate_per_1000"])
        inside = float(row["inside_rate_per_1000"])
        # The activity table contains interval aggregates, not the
        # unrecovered half-degree bins. Paired points show the measured
        # aggregates; the line connects the two windows within each year.
        ax.plot([x_outside + offset, x_inside + offset], [outside, inside],
                color=color, lw=0.85, ls=line_style, alpha=0.72,
                marker=marker, markersize=4.2, markerfacecolor=color,
                markeredgecolor="white", markeredgewidth=0.4,
                label=str(int(row["year"])))
        ax.scatter([x_outside + offset], [outside], color="white", edgecolor=COLORS["muted"],
                   linewidth=0.8, s=22, marker=marker, zorder=3)
    ax.axhline(metadata["baseline_rate_per_1000"], color=COLORS["muted"], ls=(0, (3, 2)), lw=0.8)
    ax.errorbar(
        1.18,
        metadata["peak_rate_per_1000"],
        yerr=[[metadata["peak_rate_per_1000"] - metadata["peak_rate_ci95_per_1000"][0]],
              [metadata["peak_rate_ci95_per_1000"][1] - metadata["peak_rate_per_1000"]]],
        fmt="D",
        ms=4.3,
        color=COLORS["ink"],
        ecolor=COLORS["ink"],
        elinewidth=0.8,
        capsize=2.0,
        zorder=5,
    )
    ax.text(1.18, 16.0, "pooled peak bin", ha="center", va="bottom", fontsize=6.2, color=COLORS["ink"])
    ax.set_xlim(-0.42, 1.52)
    ax.set_ylim(0, 25.5)
    ax.set_xticks([x_outside, x_inside], ["Outside\ninterval", "Supported\ninterval"])
    ax.set_xlabel(f"Activity window (supported λ⊙ = {interval_lo:.2f}–{interval_hi:.2f}°)")
    ax.set_ylabel("Stream / 1,000 background")
    ax.set_title("Exposure-normalized activity", loc="left")
    ax.legend(ncol=5, loc="upper left", bbox_to_anchor=(0, 1.01), handlelength=1.4, columnspacing=0.7)
    clean_axes(ax)


def panel_recurrence(ax: plt.Axes) -> None:
    recurrence = pd.read_csv(DATA / "annual_recurrence_2019_2026.csv")
    confirmed = recurrence["year"] >= 2022
    colors = np.where(confirmed, COLORS["blue"], COLORS["light_gray"])
    edge = np.where(confirmed, COLORS["blue"], COLORS["gray"])
    ax.bar(recurrence["year"], recurrence["members"], color=colors, edgecolor=edge, linewidth=0.8, width=0.72)
    ax.axvline(2021.5, color=COLORS["muted"], ls=(0, (3, 2)), lw=0.8)
    ax.set_xticks(recurrence["year"])
    ax.set_ylim(0, 48)
    ax.set_xlabel("Year")
    ax.set_ylabel("Selected meteors")
    ax.set_title("Annual recurrence", loc="left")
    clean_axes(ax)


def panel_radiant(ax: plt.Axes) -> None:
    centroids = pd.read_csv(DATA / "gmn_radiant_centroids.csv")
    cmap = plt.get_cmap("viridis")
    norm = plt.Normalize(centroids["year"].min(), centroids["year"].max())
    ax.errorbar(
        centroids["ra_deg"],
        centroids["dec_deg"],
        xerr=centroids["ra_se_deg"],
        yerr=centroids["dec_se_deg"],
        fmt="none",
        color=COLORS["muted"],
        lw=0.75,
        capsize=2.0,
        zorder=1,
    )
    for _, row in centroids.iterrows():
        color = cmap(norm(row["year"]))
        ax.scatter(row["ra_deg"], row["dec_deg"], s=34, color=color, edgecolor="white", linewidth=0.55, zorder=3)
        ax.text(row["ra_deg"] + 0.035, row["dec_deg"] + 0.008, str(int(row["year"])), fontsize=6.2, color=COLORS["ink"])
    ax.set_xlabel("Right ascension (deg)")
    ax.set_ylabel("Declination (deg)")
    ax.set_title("Annual radiant centroids", loc="left")
    clean_axes(ax)


def panel_orbit(ax: plt.Axes) -> None:
    orbit = pd.read_csv(DATA / "orbit_coherence.csv")
    metadata = json.loads((DATA / "orbit_coherence_metadata.json").read_text())
    sources = ["GMN", "CAMS", "SonotaCo", "EDMOND"]
    positions = {source: index for index, source in enumerate(sources)}
    rng = np.random.default_rng(20260822)
    for source in sources[1:]:
        values = orbit.loc[orbit["source"] == source, "orbit_d"].to_numpy(float)
        jitter = rng.normal(0, 0.045, size=len(values))
        ax.scatter(np.full(len(values), positions[source]) + jitter, values, s=19, color=COLORS["green"], alpha=0.85,
                   edgecolor="white", linewidth=0.35)
    gmn = positions["GMN"]
    ax.errorbar(gmn, metadata["gmn_internal_median_d"],
                yerr=[[0], [metadata["gmn_internal_q90_d"] - metadata["gmn_internal_median_d"]]],
                fmt="o", color=COLORS["blue"], ms=5, capsize=3, lw=1.2, label="GMN median–q90")
    ax.axhline(0.15, color=COLORS["red"], ls=(0, (3, 2)), lw=0.8)
    ax.text(3.98, 0.152, "0.15", ha="right", va="bottom", fontsize=6.2, color=COLORS["red"])
    ax.set_xticks(range(len(sources)), sources)
    ax.set_ylim(0, 0.27)
    ax.set_ylabel(r"Southworth–Hawkins $D_{\rm SH}$")
    ax.set_title(r"Orbital $D_{\rm SH}$ comparison", loc="left")
    clean_axes(ax)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="optional output image path")
    args = parser.parse_args()
    configure()
    fig, axes = plt.subplots(2, 2, figsize=(7.35, 6.35))
    fig.subplots_adjust(left=0.09, right=0.985, bottom=0.09, top=0.91, wspace=0.30, hspace=0.34)
    panel_activity(axes[0, 0])
    panel_recurrence(axes[0, 1])
    panel_radiant(axes[1, 0])
    panel_orbit(axes[1, 1])
    for ax, label in zip(axes.flat, "ABCD"):
        panel_label(ax, label)
    if args.out:
        save_figure(fig, args.out.parent, args.out.stem)
    else:
        save_figure(fig, OUT, "figure1_physical_detection")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
