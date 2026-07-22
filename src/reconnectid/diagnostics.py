"""Coordinate-invariant plasma diagnostics in SI units.

Swisdak Q follows Eq. (5) of Swisdak, Geophys. Res. Lett. 43, 43-49 (2016),
doi:10.1002/2015GL066980: Q = 1 - 4 I2 / ((I1-P_parallel)(I1+3P_parallel)).
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

ELEMENTARY_CHARGE = 1.602176634e-19
ELECTRON_MASS = 9.1093837139e-31
MU0 = 1.25663706212e-6


def norm(x: np.ndarray) -> np.ndarray:
    return np.linalg.norm(x, axis=-1)


def safe_divide(a: np.ndarray, b: np.ndarray, epsilon: float = 1e-30) -> np.ndarray:
    return np.asarray(a) / (np.asarray(b) + epsilon)


def current_density(ne: np.ndarray, vi: np.ndarray, ve: np.ndarray) -> np.ndarray:
    """Approximate moment current J=e*n_e*(v_i-v_e), in A/m^2.

    This is a single-spacecraft quasi-neutral moment estimate, not a four-spacecraft curlometer current.
    """
    return ELEMENTARY_CHARGE * np.asarray(ne)[..., None] * (np.asarray(vi) - np.asarray(ve))


def vector_diagnostics(B: np.ndarray, E: np.ndarray, ve: np.ndarray, J: np.ndarray, epsilon: float = 1e-30) -> dict[str, np.ndarray]:
    """Compute E'=E+v_e x B (V/m) and scalar current/energy diagnostics."""
    B, E, ve, J = map(lambda z: np.asarray(z, float), (B, E, ve, J))
    if not (B.shape == E.shape == ve.shape == J.shape and B.shape[-1] == 3):
        raise ValueError("B, E, ve, and J must share shape (..., 3)")
    ep = E + np.cross(ve, B)
    bhat = safe_divide(B, norm(B)[..., None], epsilon)
    jpar = np.sum(J * bhat, axis=-1)
    jperp = norm(J - jpar[..., None] * bhat)
    de = np.sum(J * ep, axis=-1)
    return {
        "E_prime": ep, "D_e": de,
        "D_e_normalized": safe_divide(de, norm(J) * norm(ep), epsilon),
        "E_parallel": np.sum(E * bhat, axis=-1),
        "E_prime_magnitude": norm(ep), "J_magnitude": norm(J),
        "J_parallel": jpar, "J_perpendicular_magnitude": jperp,
    }


def symmetric_tensor(values: np.ndarray) -> np.ndarray:
    """Convert pressure components (..., 6/9/3x3) to a symmetric (...,3,3) tensor."""
    a = np.asarray(values, float)
    if a.shape[-2:] == (3, 3):
        return 0.5 * (a + np.swapaxes(a, -1, -2))
    if a.shape[-1] == 6:  # xx, yy, zz, xy, xz, yz (MMS FPI convention)
        xx, yy, zz, xy, xz, yz = np.moveaxis(a, -1, 0)
        return np.stack((xx, xy, xz, xy, yy, yz, xz, yz, zz), axis=-1).reshape(a.shape[:-1] + (3, 3))
    if a.shape[-1] == 9:
        return symmetric_tensor(a.reshape(a.shape[:-1] + (3, 3)))
    raise ValueError("Pressure tensor must end in 6, 9, or 3x3 components")


@dataclass(frozen=True)
class PressureResults:
    values: dict[str, np.ndarray]
    positive_semidefinite: np.ndarray


def pressure_diagnostics(P: np.ndarray, B: np.ndarray, epsilon: float = 1e-30, psd_tolerance: float = 1e-12) -> PressureResults:
    """Compute tensor invariants and field-relative electron pressures in Pa."""
    P = symmetric_tensor(P)
    B = np.asarray(B, float)
    if P.shape[:-2] != B.shape[:-1] or B.shape[-1] != 3:
        raise ValueError("P (...,3,3) and B (...,3) leading shapes must agree")
    leading = P.shape[:-2]
    flat = P.reshape((-1, 3, 3))
    finite_tensor = np.all(np.isfinite(flat), axis=(1, 2))
    eig_flat = np.full((len(flat), 3), np.nan)
    det_flat = np.full(len(flat), np.nan)
    if finite_tensor.any():
        eig_flat[finite_tensor] = np.linalg.eigvalsh(flat[finite_tensor])
        det_flat[finite_tensor] = np.linalg.det(flat[finite_tensor])
    eig = eig_flat.reshape(leading + (3,))
    scale = np.maximum(np.max(np.abs(eig), axis=-1), epsilon)
    psd = np.min(eig, axis=-1) >= -psd_tolerance * scale
    tr = np.trace(P, axis1=-2, axis2=-1)
    det = det_flat.reshape(leading)
    fro = np.sqrt(np.sum(P * P, axis=(-2, -1)))
    bhat = safe_divide(B, norm(B)[..., None], epsilon)
    ppar = np.einsum("...i,...ij,...j->...", bhat, P, bhat)
    pperp_total = tr - ppar
    isotropic = tr / 3.0
    dev = P - isotropic[..., None, None] * np.eye(3)
    dev_norm = np.sqrt(np.sum(dev * dev, axis=(-2, -1)))
    i2 = 0.5 * (tr * tr - np.trace(P @ P, axis1=-2, axis2=-1))
    q = 1.0 - safe_divide(4.0 * i2, (tr - ppar) * (tr + 3.0 * ppar), epsilon)
    q = np.where(psd, np.clip(q, 0.0, 1.0), np.nan)
    anisotropy = safe_divide(ppar, 0.5 * pperp_total, epsilon) - 1.0
    vals = {
        "pressure_trace": tr, "pressure_determinant": det, "pressure_frobenius": fro,
        "pressure_eigenvalue_min": eig[..., 0], "pressure_eigenvalue_mid": eig[..., 1],
        "pressure_eigenvalue_max": eig[..., 2], "pressure_parallel": ppar,
        "pressure_perpendicular_total": pperp_total, "pressure_anisotropy": anisotropy,
        "pressure_deviatoric_norm": dev_norm, "Q": q,
    }
    for key, value in vals.items():
        if key != "Q":
            vals[key] = np.where(psd, value, np.nan)
    return PressureResults(vals, psd)
