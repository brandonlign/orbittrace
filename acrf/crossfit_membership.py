"""Numerical helpers for cross-fitted ACRF membership."""
from __future__ import annotations

import numpy as np


def _robust_center_scale(values: np.ndarray, floor: float) -> tuple[np.ndarray, np.ndarray]:
    center = np.median(values, axis=0)
    mad = np.median(np.abs(values - center[None, :]), axis=0) * 1.4826
    q25, q75 = np.percentile(values, [25.0, 75.0], axis=0)
    iqr_scale = (q75 - q25) / 1.349
    scale = np.maximum(np.maximum(mad, iqr_scale), float(floor))
    return center, scale


def _distances(
    values: np.ndarray,
    center: np.ndarray,
    scale: np.ndarray,
    uncertainties: np.ndarray | None,
) -> np.ndarray:
    if uncertainties is None:
        denominator = scale[None, :]
    else:
        uncertainty_values = np.asarray(uncertainties, dtype=float)
        denominator = np.sqrt(scale[None, :] ** 2 + uncertainty_values**2)
    return np.sqrt(np.sum(((values - center[None, :]) / denominator) ** 2, axis=1))


def _bh_qvalues(p_values: np.ndarray) -> np.ndarray:
    values = np.asarray(p_values, dtype=float)
    if values.ndim != 1 or np.any(~np.isfinite(values)) or np.any((values < 0.0) | (values > 1.0)):
        raise ValueError("p_values must be a finite vector in [0, 1]")
    if values.size == 0:
        return values.copy()
    order = np.argsort(values, kind="mergesort")
    ranked = values[order]
    adjusted = np.minimum.accumulate(
        (ranked * values.size / np.arange(1, values.size + 1))[::-1]
    )[::-1]
    result = np.empty_like(adjusted)
    result[order] = np.minimum(adjusted, 1.0)
    return result


def _membership_pvalues(core_scores: np.ndarray, scores: np.ndarray) -> np.ndarray:
    """Return conformal similarity p-values; larger values mean closer to the core."""
    core = np.asarray(core_scores, dtype=float)
    query = np.asarray(scores, dtype=float)
    if core.ndim != 1 or query.ndim != 1 or not len(core):
        raise ValueError("core_scores must be non-empty and both inputs must be one-dimensional")
    if np.any(~np.isfinite(core)) or np.any(~np.isfinite(query)):
        raise ValueError("score vectors must be finite")
    sorted_core = np.sort(core)
    less_than = np.searchsorted(sorted_core, query, side="left")
    greater_equal = len(core) - less_than
    return (1.0 + greater_equal.astype(float)) / (len(core) + 1.0)


__all__: list[str] = []
