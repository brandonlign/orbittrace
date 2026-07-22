"""Rotation, noise, timing, reference-group, and feature-ablation robustness tools."""
from __future__ import annotations

import numpy as np
import pandas as pd
from .features import construct_features


def random_rotation(rng: np.random.Generator) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    q *= np.sign(np.diag(r))
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1
    return q


def rotate_vectors(values: np.ndarray, rotation: np.ndarray) -> np.ndarray:
    return np.asarray(values) @ rotation.T


def rotate_tensors(values: np.ndarray, rotation: np.ndarray) -> np.ndarray:
    return np.einsum("ij,...jk,lk->...il", rotation, np.asarray(values), rotation)


def relative_discrepancy(a: np.ndarray, b: np.ndarray, floor: float = 1e-14) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    finite = np.isfinite(a) & np.isfinite(b)
    if not finite.any():
        return 0.0
    return float(np.max(np.abs(a[finite] - b[finite]) / np.maximum(np.maximum(np.abs(a[finite]), np.abs(b[finite])), floor)))


def test_rotation_invariance(B: np.ndarray, E: np.ndarray, ve: np.ndarray, vi: np.ndarray, ne: np.ndarray,
                             Pe: np.ndarray, feature_names: list[str], trials: int, seed: int) -> pd.DataFrame:
    reference = construct_features(B, E, ve, vi, ne, Pe)
    rng = np.random.default_rng(seed); rows = []
    for trial in range(trials):
        R = random_rotation(rng)
        rotated = construct_features(rotate_vectors(B, R), rotate_vectors(E, R), rotate_vectors(ve, R),
                                     rotate_vectors(vi, R), ne, rotate_tensors(Pe, R))
        for feature in feature_names:
            rows.append({"trial": trial, "feature": feature,
                         "maximum_relative_discrepancy": relative_discrepancy(reference[feature], rotated[feature])})
    return pd.DataFrame(rows)


def add_relative_noise(values: np.ndarray, fraction: float, rng: np.random.Generator, symmetric: bool = False) -> np.ndarray:
    a = np.asarray(values, float)
    scale = fraction * np.maximum(np.abs(a), np.nanmedian(np.abs(a), axis=0))
    out = a + rng.normal(size=a.shape) * scale
    return 0.5 * (out + np.swapaxes(out, -1, -2)) if symmetric else out


FEATURE_ABLATIONS = {
    "pressure_only": ["Q", "pressure_anisotropy", "pressure_deviatoric_fraction", "eigenvalue_min_max_ratio", "eigenvalue_mid_max_ratio", "electron_beta"],
    "field_velocity_only": ["E_prime_normalized", "E_parallel_fraction", "J_parallel_fraction", "J_parallel_fraction_abs", "J_perpendicular_fraction", "thermal_current_fraction"],
    "established_only": ["Q", "D_e_normalized", "E_prime_magnitude", "E_parallel_abs", "J_magnitude", "pressure_anisotropy_abs"],
}

