"""Build synchronized, SI, event-identified Parquet datasets from cached MMS arrays."""
from __future__ import annotations

from pathlib import Path
import json
import logging
import numpy as np
import pandas as pd

from .config import PilotConfig
from .features import construct_features, construct_targets
from .guide_field import estimate_guide_proxy
from .synchronization import centered_grid, gap_aware_interpolate, to_si

LOGGER = logging.getLogger(__name__)
QUANTITIES = {"B": "B", "E": "E", "ve": "velocity", "vi": "velocity", "ne": "density", "ni": "density", "Pe": "pressure"}


def synchronize_event(event: pd.Series, cfg: PilotConfig, root: Path) -> tuple[np.ndarray, dict[str, np.ndarray], np.ndarray, dict[str, object]]:
    """Load one immutable cache and return event-centered synchronized SI arrays."""
    cache = root / "data/cache/events" / f"{event.event_id}.npz"
    if not cache.exists():
        raise FileNotFoundError(f"No cached acquisition for {event.event_id}: {cache}")
    raw = np.load(cache)
    grid = centered_grid(cfg.event_window_seconds, cfg.target_cadence_seconds)
    center_unix = pd.Timestamp(event.timestamp).timestamp()
    synced: dict[str, np.ndarray] = {}
    decisions = {}
    masks = []
    for product, quantity in QUANTITIES.items():
        times = raw[f"{product}_time"] - center_unix
        values = to_si(raw[f"{product}_values"], quantity)
        result = gap_aware_interpolate(times, values, grid, cfg.maximum_interpolation_gap_seconds)
        synced[product] = result.values
        masks.append(result.valid)
        decisions[product] = {
            "native_cadence_seconds": result.source_cadence_seconds,
            "interpolated_fraction": result.interpolated_fraction,
            "valid_fraction": float(result.valid.mean()),
            "maximum_gap_seconds": cfg.maximum_interpolation_gap_seconds,
        }
    valid = np.logical_and.reduce(masks)
    return grid, synced, valid, decisions


def build_event(event: pd.Series, cfg: PilotConfig, root: Path) -> tuple[pd.DataFrame, dict[str, object]]:
    grid, synced, valid, decisions = synchronize_event(event, cfg, root)
    final_fraction = float(valid.mean())
    if final_fraction < cfg.minimum_valid_fraction:
        raise ValueError(f"Final valid fraction {final_fraction:.3f} is below {cfg.minimum_valid_fraction:.3f}")
    X = construct_features(synced["B"], synced["E"], synced["ve"], synced["vi"], synced["ne"].squeeze(), synced["Pe"], cfg.epsilon)
    targets = construct_targets(grid, cfg.positive_half_width_seconds, cfg.ambiguous_half_width_seconds)
    frame = pd.concat([pd.DataFrame({"delta_t": grid, "valid": valid}), X, targets], axis=1)
    frame.insert(0, "event_id", str(event.event_id))
    frame["sample_weight"] = np.where(valid & ~frame.ambiguous, 1.0 / max(int((valid & ~frame.ambiguous).sum()), 1), 0.0)
    proxy = estimate_guide_proxy(grid, synced["B"], cfg.mva_half_width_seconds, cfg.ambiguous_half_width_seconds, cfg.epsilon)
    metadata = {
        "event_id": str(event.event_id), "timestamp": str(event.timestamp), "spacecraft": str(event.spacecraft),
        "reference_paper": str(event.reference_paper),
        "literature_label": "" if pd.isna(event.literature_label) else str(event.literature_label),
        "valid_fraction": final_fraction, "interpolation_decisions": json.dumps(decisions),
        **{k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in proxy.__dict__.items() if k != "basis_LMN"},
        "basis_LMN": json.dumps(proxy.basis_LMN.tolist()), "success": True, "failure_reason": "",
    }
    return frame, metadata


def build_dataset(events: pd.DataFrame, cfg: PilotConfig, root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    frames, metadata = [], []
    for _, event in events.iterrows():
        try:
            frame, meta = build_event(event, cfg, root)
            frames.append(frame)
            metadata.append(meta)
        except Exception as exc:
            LOGGER.exception("Dataset build failed for %s", event.event_id)
            metadata.append({"event_id": event.event_id, "timestamp": str(event.timestamp), "spacecraft": event.spacecraft,
                             "reference_paper": event.reference_paper,
                             "literature_label": "" if pd.isna(event.literature_label) else event.literature_label,
                             "success": False, "failure_reason": f"{type(exc).__name__}: {exc}"})
    data = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    meta = pd.DataFrame(metadata)
    data.to_parquet(root / "data/processed/samples.parquet", index=False)
    meta.to_parquet(root / "data/processed/events.parquet", index=False)
    return data, meta
