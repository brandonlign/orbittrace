"""Configuration loading and repository path management."""
from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any
import os
import yaml


@dataclass(frozen=True)
class PilotConfig:
    random_seed: int = 2026
    event_window_seconds: float = 6.0
    positive_half_width_seconds: float = 0.15
    ambiguous_half_width_seconds: float = 0.60
    target_cadence_seconds: float = 0.03
    maximum_interpolation_gap_seconds: float = 0.15
    minimum_valid_fraction: float = 0.70
    maximum_events: int = 24
    minimum_events_required: int = 12
    bootstrap_iterations: int = 2000
    permutation_iterations: int = 500
    rotation_trials: int = 100
    noise_trials: int = 50
    high_guide_quantile: float = 0.67
    low_guide_quantile: float = 0.33
    mva_half_width_seconds: float = 1.5
    epsilon: float = 1e-30
    zenodo_record: int = 8319481

    @classmethod
    def load(cls, path: str | Path) -> "PilotConfig":
        raw: dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
        allowed = {f.name for f in fields(cls)}
        unknown = sorted(set(raw) - allowed)
        if unknown:
            raise ValueError(f"Unknown configuration keys: {unknown}")
        cfg = cls(**raw)
        if not (0 < cfg.positive_half_width_seconds < cfg.ambiguous_half_width_seconds < cfg.event_window_seconds):
            raise ValueError("Target windows must satisfy 0 < positive < ambiguous < event window")
        if not (0 < cfg.minimum_valid_fraction <= 1):
            raise ValueError("minimum_valid_fraction must lie in (0, 1]")
        return cfg


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_directories(root: Path | None = None) -> None:
    root = root or repository_root()
    for rel in (
        "data/raw", "data/cache", "data/processed", "data/event_metadata",
        "results/figures", "results/tables", "results/logs",
    ):
        (root / rel).mkdir(parents=True, exist_ok=True)


def load_project_config(root: Path) -> PilotConfig:
    """Load the CLI-selected config, resolving relative paths from the repository."""
    selected = Path(os.environ.get("RECONNECTID_CONFIG", "configs/pilot.yaml"))
    if not selected.is_absolute():
        selected = root / selected
    return PilotConfig.load(selected)
