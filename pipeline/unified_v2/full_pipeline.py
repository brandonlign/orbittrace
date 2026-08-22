"""Shared target-free Unified v2 full-catalogue candidate pipeline.

The OrbitTrace recovery application and fair benchmark must use the same
candidate construction.  This module owns the post-hierarchy filtering,
cross-fitted expansion, orbital coherence gate, and deterministic ranking so
that a benchmark cannot silently evaluate a reduced v2 variant.
"""
from __future__ import annotations

from typing import Any, Sequence

import numpy as np

from pipeline.pr57_novel import run_novel_search as base

from .config import V2Config
from .crossfit_membership import expand_candidate


def seed_score(candidate: dict[str, Any], quantile: float) -> float:
    """Return the deterministic score used for seed eligibility and ranking."""

    if candidate.get("seed_score") is not None:
        return float(candidate["seed_score"])
    if candidate.get("recurrent_stability") is not None:
        return float(candidate["recurrent_stability"])
    annual = np.asarray(candidate.get("annual_normalized_stability", ()), dtype=float)
    if not len(annual):
        return 0.0
    try:
        return float(np.quantile(annual, quantile, method="lower"))
    except TypeError:  # numpy < 1.22
        return float(np.quantile(annual, quantile, interpolation="lower"))


def apply_orbit_gate(
    candidate: dict[str, Any],
    orbit_matrix: np.ndarray | None,
    event_ids: np.ndarray,
    config: V2Config,
) -> dict[str, Any]:
    """Apply the fixed post-halo orbit-coherence gate when orbits are present."""

    result = dict(candidate)
    expanded = np.asarray(candidate.get("expanded_members", ()), dtype=int)
    if orbit_matrix is None:
        result["final_members"] = [int(value) for value in expanded.tolist()]
        result["final_event_ids"] = [str(value) for value in event_ids[expanded].tolist()]
        result["final_member_count"] = int(len(expanded))
        result["orbit_coherence"] = {"applied": False, "reason": "orbit_fields_unavailable"}
        return result

    values = np.asarray(orbit_matrix, dtype=float)
    core = np.asarray(candidate.get("core_members", candidate.get("members", ())), dtype=int)
    valid_core = np.isfinite(values[core]).all(axis=1)
    if int(valid_core.sum()) < config.halo_min_training_members:
        result["final_members"] = [int(value) for value in expanded.tolist()]
        result["final_event_ids"] = [str(value) for value in event_ids[expanded].tolist()]
        result["final_member_count"] = int(len(expanded))
        result["orbit_coherence"] = {
            "applied": False,
            "reason": "insufficient_valid_core_orbits",
            "valid_core": int(valid_core.sum()),
        }
        return result

    core_orbits = values[core][valid_core]
    medoid = base.orbit_summary(core_orbits)["medoid"]
    valid_rows = np.isfinite(values[expanded]).all(axis=1)
    distances = np.full(len(expanded), np.inf, dtype=float)
    if bool(valid_rows.any()):
        distances[valid_rows] = base.orbit_distance_matrix(
            values[expanded][valid_rows], medoid[None, :]
        )[:, 0]
    keep = valid_rows & (distances <= float(config.halo_orbit_distance_max))
    final = expanded[keep]
    result["final_members"] = [int(value) for value in final.tolist()]
    result["final_event_ids"] = [str(value) for value in event_ids[final].tolist()]
    result["final_member_count"] = int(len(final))
    result["orbit_coherence"] = {
        "applied": True,
        "valid_core": int(valid_core.sum()),
        "valid_expanded": int(valid_rows.sum()),
        "distance_max": float(config.halo_orbit_distance_max),
        "medoid": medoid.tolist(),
        "kept": int(len(final)),
        "removed": int(len(expanded) - len(final)),
    }
    return result


def compact_expanded_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    """Drop redundant index copies while retaining auditable event IDs."""

    result = dict(candidate)
    for key in (
        "members",
        "core_members",
        "expanded_members",
        "final_members",
        "expanded_event_ids",
    ):
        result.pop(key, None)
    return result


def build_full_catalogue(
    raw_candidates: Sequence[dict[str, Any]],
    matrix: np.ndarray,
    years: np.ndarray,
    event_ids: np.ndarray,
    orbit_matrix: np.ndarray | None,
    config: V2Config,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Expand, gate, and rank the exact Unified v2-Full candidate catalogue."""

    values = np.asarray(matrix, dtype=float)
    year_values = np.asarray(years, dtype=np.int64)
    ids = np.asarray(event_ids, dtype=str)
    if values.ndim != 2 or values.shape[0] != len(year_values) or len(ids) != len(year_values):
        raise ValueError("matrix, years, and event_ids must align")
    if orbit_matrix is not None and np.asarray(orbit_matrix).shape[0] != len(values):
        raise ValueError("orbit_matrix must align with matrix rows")

    normalized = [dict(candidate) for candidate in raw_candidates]
    for candidate in normalized:
        candidate["seed_score"] = seed_score(candidate, config.recurrence_quantile)
    eligible = [
        candidate
        for candidate in normalized
        if float(candidate["seed_score"]) > 0.0
        and int(candidate["member_count"]) <= int(config.hierarchy_max_candidate_members)
    ]
    eligible.sort(
        key=lambda item: (
            -float(item["seed_score"]),
            -int(item["member_count"]),
            item["family_id"],
        )
    )
    for rank, candidate in enumerate(eligible, start=1):
        candidate["seed_rank"] = int(rank)

    candidates: list[dict[str, Any]] = []
    for candidate in eligible:
        expanded = expand_candidate(
            candidate,
            values,
            year_values,
            ids,
            config,
            retain_member_diagnostics=False,
        )
        gated = apply_orbit_gate(expanded, orbit_matrix, ids, config)
        candidates.append(compact_expanded_candidate(gated))
    candidates.sort(
        key=lambda item: (
            -seed_score(item, config.recurrence_quantile),
            int(item.get("seed_rank", 0)),
            -int(item.get("final_member_count", item.get("expanded_member_count", 0))),
            item["family_id"],
        )
    )
    for rank, candidate in enumerate(candidates, start=1):
        candidate["global_rank"] = int(rank)
    diagnostics = {
        "raw_candidates": int(len(normalized)),
        "eligible_candidates": int(len(eligible)),
        "excluded_nonrecurrent": int(
            sum(float(item["seed_score"]) <= 0.0 for item in normalized)
        ),
        "excluded_too_large": int(
            sum(int(item["member_count"]) > config.hierarchy_max_candidate_members for item in normalized)
        ),
        "maximum_seed_members": int(config.hierarchy_max_candidate_members),
        "orbit_gate_available": bool(orbit_matrix is not None),
        "pipeline": "unified_v2_full_partitioned_parent_leaf_halo_orbit_gate",
    }
    return candidates, diagnostics


__all__ = [
    "apply_orbit_gate",
    "build_full_catalogue",
    "compact_expanded_candidate",
    "seed_score",
]
