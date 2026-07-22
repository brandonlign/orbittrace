"""Dimensionless, coordinate-rotation-invariant candidate feature construction."""
from __future__ import annotations

import numpy as np
import pandas as pd
from .diagnostics import ELECTRON_MASS, MU0, current_density, norm, pressure_diagnostics, safe_divide, vector_diagnostics


INVARIANT_FEATURES = [
    "D_e_normalized", "D_e_normalized_abs", "E_prime_normalized",
    "E_parallel_fraction", "J_parallel_fraction", "J_parallel_fraction_abs",
    "J_perpendicular_fraction", "Q", "pressure_anisotropy",
    "pressure_deviatoric_fraction", "eigenvalue_min_max_ratio",
    "eigenvalue_mid_max_ratio", "electron_beta", "thermal_current_fraction",
]

BASELINE_SCORES = ["Q", "D_e_positive", "D_e_abs", "D_e_normalized", "E_prime_magnitude", "E_parallel_abs", "J_magnitude", "pressure_anisotropy_abs"]


def construct_features(B: np.ndarray, E: np.ndarray, ve: np.ndarray, vi: np.ndarray, ne: np.ndarray, Pe: np.ndarray, epsilon: float = 1e-30) -> pd.DataFrame:
    """Return invariant scalar features; inputs must be SI and in one Cartesian frame."""
    J = current_density(ne, vi, ve)
    vd = vector_diagnostics(B, E, ve, J, epsilon)
    pdx = pressure_diagnostics(Pe, B, epsilon)
    p = pdx.values
    bmag, emag, jmag = norm(B), norm(E), vd["J_magnitude"]
    ep_scale = emag + norm(np.cross(ve, B))
    pscalar = p["pressure_trace"] / 3.0
    vthermal = np.sqrt(np.maximum(2.0 * pscalar / (np.asarray(ne) * ELECTRON_MASS + epsilon), 0.0))
    dev_fraction = safe_divide(p["pressure_deviatoric_norm"], p["pressure_frobenius"], epsilon)
    emin, emid, emax = p["pressure_eigenvalue_min"], p["pressure_eigenvalue_mid"], p["pressure_eigenvalue_max"]
    data = {
        "D_e": vd["D_e"], "D_e_positive": np.maximum(vd["D_e"], 0), "D_e_abs": np.abs(vd["D_e"]),
        "D_e_normalized": vd["D_e_normalized"], "D_e_normalized_abs": np.abs(vd["D_e_normalized"]),
        "E_prime_magnitude": vd["E_prime_magnitude"], "E_prime_normalized": safe_divide(vd["E_prime_magnitude"], ep_scale, epsilon),
        "E_parallel": vd["E_parallel"], "E_parallel_abs": np.abs(vd["E_parallel"]),
        "E_parallel_fraction": safe_divide(np.abs(vd["E_parallel"]), emag, epsilon),
        "J_magnitude": jmag, "J_parallel": vd["J_parallel"],
        "J_parallel_fraction": safe_divide(vd["J_parallel"], jmag, epsilon),
        "J_parallel_fraction_abs": safe_divide(np.abs(vd["J_parallel"]), jmag, epsilon),
        "J_perpendicular_fraction": safe_divide(vd["J_perpendicular_magnitude"], jmag, epsilon),
        "Q": p["Q"], "pressure_anisotropy": p["pressure_anisotropy"],
        "pressure_anisotropy_abs": np.abs(p["pressure_anisotropy"]),
        "pressure_deviatoric_fraction": dev_fraction,
        "eigenvalue_min_max_ratio": safe_divide(emin, emax, epsilon),
        "eigenvalue_mid_max_ratio": safe_divide(emid, emax, epsilon),
        "electron_beta": safe_divide(2.0 * MU0 * pscalar, bmag * bmag, epsilon),
        "thermal_current_fraction": safe_divide(jmag, 1.602176634e-19 * ne * vthermal, epsilon),
        "pressure_psd": pdx.positive_semidefinite.astype(float),
    }
    frame = pd.DataFrame(data)
    frame.replace([np.inf, -np.inf], np.nan, inplace=True)
    return frame


def construct_targets(delta_t: np.ndarray, positive_half_width: float, ambiguous_half_width: float) -> pd.DataFrame:
    """Create hard class/ambiguity labels and a Gaussian soft localization target."""
    dt = np.asarray(delta_t, float)
    return pd.DataFrame({
        "target": (np.abs(dt) <= positive_half_width).astype(int),
        "ambiguous": ((np.abs(dt) > positive_half_width) & (np.abs(dt) <= ambiguous_half_width)),
        "soft_target": np.exp(-0.5 * (dt / positive_half_width) ** 2),
    })

