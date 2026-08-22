"""Memory-bounded blind hierarchy scan over overlapping solar-longitude windows."""
from __future__ import annotations

import hashlib
from typing import Any

import numpy as np

from .config import V2Config
from .features import circular_difference_deg
from .recurrent_tree import fit_recurrent_hierarchy


def _stable_cap(indices: np.ndarray, event_ids: np.ndarray, limit: int, salt: str) -> np.ndarray:
    """Select a deterministic, order-independent subset using event-ID hashes."""

    if len(indices) <= limit:
        return np.sort(indices)
    scored = sorted(
        (
            hashlib.sha256(f"{salt}|{event_ids[index]}".encode()).digest(),
            int(index),
        )
        for index in indices
    )
    return np.sort(np.asarray([index for _digest, index in scored[:limit]], dtype=np.int64))


def _candidate_score(candidate: dict[str, Any], quantile: float) -> float:
    recurrent = candidate.get("recurrent_stability")
    if recurrent is not None:
        return float(recurrent)
    annual = np.asarray(candidate.get("annual_normalized_stability", ()), dtype=float)
    if not len(annual):
        return 0.0
    try:
        return float(np.quantile(annual, quantile, method="lower"))
    except TypeError:  # numpy < 1.22
        return float(np.quantile(annual, quantile, interpolation="lower"))


def _deduplicate(
    candidates: list[dict[str, Any]],
    threshold: float,
    quantile: float,
) -> tuple[list[dict[str, Any]], int]:
    """Retain the highest-ranked representative of overlapping-window duplicates."""

    ordered = sorted(
        candidates,
        key=lambda item: (
            -_candidate_score(item, quantile),
            -int(item["member_count"]),
            item["family_id"],
        ),
    )
    kept: list[dict[str, Any]] = []
    kept_sets: list[set[str]] = []
    event_to_kept: dict[str, set[int]] = {}
    removed = 0
    for candidate in ordered:
        members = set(map(str, candidate["event_ids"]))
        possible: set[int] = set()
        for event_id in members:
            possible.update(event_to_kept.get(event_id, ()))
        duplicate_index: int | None = None
        for index in sorted(possible):
            other = kept_sets[index]
            union = len(members | other)
            if union and len(members & other) / union >= threshold:
                duplicate_index = index
                break
        if duplicate_index is not None:
            kept[duplicate_index].setdefault("supporting_windows", []).extend(
                candidate.get("supporting_windows", [])
            )
            kept[duplicate_index]["supporting_windows"] = sorted(
                set(float(value) for value in kept[duplicate_index]["supporting_windows"])
            )
            removed += 1
            continue
        index = len(kept)
        kept.append(candidate)
        kept_sets.append(members)
        for event_id in members:
            event_to_kept.setdefault(event_id, set()).add(index)
    for rank, candidate in enumerate(kept, start=1):
        candidate["rank"] = rank
        candidate["seed_score"] = _candidate_score(candidate, quantile)
    return kept, removed


def fit_partitioned_recurrent_hierarchy(
    matrix: np.ndarray,
    years: np.ndarray,
    event_ids: np.ndarray,
    solar_longitude_deg: np.ndarray,
    config: V2Config | None = None,
    *,
    include_leaves: bool = True,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Scan fixed overlapping windows and deduplicate candidates without labels.

    Every window is defined before seeing target membership.  Per-year caps are
    deterministic hashes of event IDs, avoiding both a global HDBSCAN memory
    spike and order-dependent random sampling.
    """

    config = config or V2Config()
    values = np.asarray(matrix, dtype=float)
    year_values = np.asarray(years, dtype=np.int64)
    ids = np.asarray(event_ids, dtype=str)
    solar = np.asarray(solar_longitude_deg, dtype=float)
    if values.ndim != 2 or values.shape[0] != len(year_values) or len(ids) != len(year_values):
        raise ValueError("matrix, years, and event_ids must align")
    if solar.shape != (len(year_values),) or not np.isfinite(solar).all():
        raise ValueError("solar_longitude_deg must be finite and align with rows")
    unique_years = tuple(sorted(int(value) for value in np.unique(year_values)))
    if len(unique_years) < 2:
        raise ValueError("at least two observing years are required")

    stride = float(config.hierarchy_window_stride_deg)
    centers = np.arange(0.0, 360.0, stride, dtype=float)
    half_width = float(config.hierarchy_window_width_deg) / 2.0
    parents_all: list[dict[str, Any]] = []
    leaves_all: list[dict[str, Any]] = []
    window_diagnostics: list[dict[str, Any]] = []
    for center in centers:
        within = np.abs(circular_difference_deg(solar, center)) <= half_width
        selected_parts: list[np.ndarray] = []
        raw_counts: dict[str, int] = {}
        used_counts: dict[str, int] = {}
        for year in unique_years:
            indices = np.flatnonzero(within & (year_values == year))
            raw_counts[str(year)] = int(len(indices))
            if len(indices) < config.min_cluster_size:
                selected_parts = []
                break
            chosen = _stable_cap(
                indices,
                ids,
                int(config.hierarchy_max_rows_per_year),
                f"{config.hierarchy_sample_seed}|{center:.6f}|{year}",
            )
            used_counts[str(year)] = int(len(chosen))
            selected_parts.append(chosen)
        if not selected_parts:
            continue
        selected = np.sort(np.concatenate(selected_parts))
        print(
            f"solar window {center:06.1f}: fitting {len(selected):,} rows "
            f"({', '.join(f'{year}:{used_counts[str(year)]}' for year in unique_years)})",
            flush=True,
        )
        parents, leaves, diagnostics = fit_recurrent_hierarchy(
            values[selected],
            year_values[selected],
            ids[selected],
            config,
            include_leaves=include_leaves,
        )
        for branch in (parents, leaves):
            for candidate in branch:
                candidate["window_center_deg"] = float(center)
                candidate["window_width_deg"] = float(config.hierarchy_window_width_deg)
                candidate["supporting_windows"] = [float(center)]
                candidate["seed_score"] = _candidate_score(candidate, config.recurrence_quantile)
        parents_all.extend(parents)
        leaves_all.extend(leaves)
        window_diagnostics.append(
            {
                "center_deg": float(center),
                "raw_rows_by_year": raw_counts,
                "used_rows_by_year": used_counts,
                "diagnostics": diagnostics,
            }
        )

    parents, removed_parents = _deduplicate(
        parents_all, config.hierarchy_dedup_jaccard, config.recurrence_quantile
    )
    leaves, removed_leaves = _deduplicate(
        leaves_all, config.hierarchy_dedup_jaccard, config.recurrence_quantile
    )
    return parents, leaves, {
        "mode": "partitioned_solar_longitude_hierarchy",
        "window_width_deg": float(config.hierarchy_window_width_deg),
        "window_stride_deg": float(config.hierarchy_window_stride_deg),
        "dedup_jaccard": float(config.hierarchy_dedup_jaccard),
        "windows_fit": int(len(window_diagnostics)),
        "raw_parent_candidates": int(len(parents_all)),
        "raw_leaf_candidates": int(len(leaves_all)),
        "deduplicated_parent_candidates": int(len(parents)),
        "deduplicated_leaf_candidates": int(len(leaves)),
        "duplicates_removed": int(removed_parents + removed_leaves),
        "windows": window_diagnostics,
    }


__all__ = ["fit_partitioned_recurrent_hierarchy"]
