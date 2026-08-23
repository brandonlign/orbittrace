"""Shared restrained journal-figure style for the OrbitTrace paper."""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


COLORS = {
    "ink": "#1f2933",
    "muted": "#5b6770",
    "grid": "#c8ced3",
    "blue": "#1f4e79",
    "red": "#a23b2a",
    "green": "#2f6f4e",
    "purple": "#6d4c8d",
    "gold": "#9a6b18",
    "gray": "#858e96",
    "light_gray": "#e6e9eb",
}


def configure() -> None:
    mpl.rcParams.update({
        "font.family": "DejaVu Serif",
        "font.size": 7.6,
        "axes.labelsize": 8.0,
        "axes.titlesize": 8.8,
        "axes.titleweight": "normal",
        "axes.linewidth": 0.75,
        "axes.edgecolor": COLORS["ink"],
        "axes.labelcolor": COLORS["ink"],
        "xtick.color": COLORS["ink"],
        "ytick.color": COLORS["ink"],
        "xtick.labelsize": 7.0,
        "ytick.labelsize": 7.0,
        "legend.fontsize": 6.5,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.edgecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })


def clean_axes(ax, *, grid: bool = True) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=3.0, width=0.7)
    if grid:
        ax.grid(True, color=COLORS["grid"], linewidth=0.45, alpha=0.6)
        ax.set_axisbelow(True)


def panel_label(ax, label: str) -> None:
    ax.text(
        -0.12,
        1.04,
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        va="bottom",
        ha="left",
        color=COLORS["ink"],
    )


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for suffix, kwargs in [("pdf", {}), ("svg", {}), ("png", {"dpi": 360})]:
        fig.savefig(output_dir / f"{stem}.{suffix}", bbox_inches="tight", pad_inches=0.04, **kwargs)
    plt.close(fig)
