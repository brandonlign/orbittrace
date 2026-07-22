"""SI conversion and gap-aware synchronization to an event-centered time grid."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

UNIT_FACTORS = {"B": 1e-9, "E": 1e-3, "velocity": 1e3, "density": 1e6, "pressure": 1e-9}


@dataclass(frozen=True)
class Synchronized:
    values: np.ndarray
    valid: np.ndarray
    source_cadence_seconds: float
    interpolated_fraction: float


def to_si(values: np.ndarray, quantity: str) -> np.ndarray:
    """Convert MMS conventional units to SI (T, V/m, m/s, m^-3, or Pa)."""
    if quantity not in UNIT_FACTORS:
        raise ValueError(f"Unknown physical quantity {quantity!r}")
    return np.asarray(values, dtype=float) * UNIT_FACTORS[quantity]


def centered_grid(half_width: float, cadence: float) -> np.ndarray:
    n = int(round(2 * half_width / cadence))
    return np.linspace(-half_width, half_width, n + 1)


def gap_aware_interpolate(
    source_time: np.ndarray, source_values: np.ndarray, target_time: np.ndarray, max_gap: float
) -> Synchronized:
    """Linearly interpolate only between finite neighbors separated by at most max_gap seconds."""
    x = np.asarray(source_time, float)
    y = np.asarray(source_values, float)
    target = np.asarray(target_time, float)
    if x.ndim != 1 or y.shape[0] != len(x) or len(x) < 2:
        raise ValueError("source_time must be 1-D and match at least two value rows")
    order = np.argsort(x)
    x, y = x[order], y[order]
    flat = y.reshape(len(x), -1)
    out = np.full((len(target), flat.shape[1]), np.nan)
    all_valid = np.all(np.isfinite(flat), axis=1) & np.isfinite(x)
    valid_indices = np.flatnonzero(all_valid)
    if len(valid_indices) >= 2:
        xv, yv = x[valid_indices], flat[valid_indices]
        right = np.searchsorted(xv, target, side="left")
        exact = (right < len(xv)) & np.isclose(xv[np.minimum(right, len(xv)-1)], target, atol=1e-9)
        for k in range(flat.shape[1]):
            out[:, k] = np.interp(target, xv, yv[:, k], left=np.nan, right=np.nan)
        left_idx = np.clip(right - 1, 0, len(xv) - 1)
        right_idx = np.clip(right, 0, len(xv) - 1)
        # CDF epoch conversion introduces sub-microsecond jitter (e.g. a nominal
        # 0.150000 s cadence may decode as 0.150000095 s). This tolerance does
        # not authorize interpolation over a physically longer gap.
        gap_tolerance = max(1e-6, max_gap * 1e-6)
        supported = exact | ((right > 0) & (right < len(xv)) & ((xv[right_idx] - xv[left_idx]) <= max_gap + gap_tolerance))
        out[~supported] = np.nan
    result = out.reshape((len(target),) + y.shape[1:])
    valid = np.all(np.isfinite(out), axis=1)
    native = float(np.nanmedian(np.diff(x)))
    direct = np.isclose(target[:, None], x[None, :], atol=max(native * 0.1, 1e-6)).any(axis=1)
    return Synchronized(result, valid, native, float(np.mean(valid & ~direct)))
