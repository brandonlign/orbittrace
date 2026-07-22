"""Approximate event-level guide-field proxy based on magnetic minimum variance analysis."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class GuideProxy:
    guide_ratio_proxy: float
    B_L_before: float
    B_L_after: float
    B_M_center: float
    eigenvalue_ratio_max_mid: float
    eigenvalue_ratio_mid_min: float
    reversal_quality: float
    reliable: bool
    basis_LMN: np.ndarray


def estimate_guide_proxy(time: np.ndarray, B: np.ndarray, mva_half_width: float = 1.5, ambiguous_half_width: float = 0.6, epsilon: float = 1e-30) -> GuideProxy:
    """Estimate |B_M|/[0.5|B_L,before-B_L,after|] from B in any Cartesian frame."""
    time, B = np.asarray(time, float), np.asarray(B, float)
    valid = np.isfinite(time) & np.all(np.isfinite(B), axis=1)
    mva = valid & (np.abs(time) <= mva_half_width)
    if mva.sum() < 10:
        raise ValueError("At least ten valid points are required for MVA")
    cov = np.cov(B[mva], rowvar=False)
    vals, vecs = np.linalg.eigh(cov)
    N = vecs[:, 0]
    L = vecs[:, 2]
    M = np.cross(N, L)
    M /= np.linalg.norm(M)
    N = np.cross(L, M)
    basis = np.column_stack((L, M, N))
    proj = B @ basis
    before = valid & (time < -ambiguous_half_width)
    after = valid & (time > ambiguous_half_width)
    center = valid & (np.abs(time) <= ambiguous_half_width)
    if min(before.sum(), after.sum(), center.sum()) < 3:
        raise ValueError("Insufficient upstream/center samples for guide proxy")
    bl0, bl1 = float(np.median(proj[before, 0])), float(np.median(proj[after, 0]))
    bm = float(np.median(np.abs(proj[center, 1])))
    reversal = abs(bl0 - bl1) / (abs(bl0) + abs(bl1) + epsilon)
    r1 = float(vals[2] / (vals[1] + epsilon))
    r2 = float(vals[1] / (vals[0] + epsilon))
    reliable = bool(np.isfinite([r1, r2, reversal]).all() and r1 >= 2.0 and reversal >= 0.5)
    return GuideProxy(float(bm / (0.5 * abs(bl0 - bl1) + epsilon)), bl0, bl1, bm, r1, r2, float(reversal), reliable, basis)
