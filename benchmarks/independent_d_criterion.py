"""Label-free EDMOND-style D-criterion comparator.

This is an independent implementation of Rudawska et al. (2015), not the
authors' original implementation. It uses their published D_SH=0.05 seed grouping,
geocentric D_x=0.15 merging, and five-member catalogue threshold.
"""
from __future__ import annotations

import hashlib
from typing import Any, Mapping, Sequence

import numpy as np
from scipy.spatial import cKDTree


D_SH_THRESHOLD = 0.05
D_X_THRESHOLD = 0.15
MIN_MEMBERS = 5
DX_WEIGHTS = (0.17, 1.20, 1.20, 0.20)


def _wrap_radians(values: np.ndarray) -> np.ndarray:
    return (np.asarray(values, dtype=float) + np.pi) % (2.0 * np.pi) - np.pi


def southworth_hawkins_pairs(orbits: np.ndarray, pairs: np.ndarray) -> np.ndarray:
    """Evaluate the published Southworth-Hawkins D criterion for row pairs."""

    values = np.asarray(orbits, dtype=float)
    indices = np.asarray(pairs, dtype=np.int64)
    if values.ndim != 2 or values.shape[1] != 5:
        raise ValueError("orbits must have columns (e, q, i, peri, node)")
    if indices.ndim != 2 or indices.shape[1] != 2:
        raise ValueError("pairs must have shape (m, 2)")
    if not len(indices):
        return np.asarray([], dtype=float)
    left = values[indices[:, 0]]
    right = values[indices[:, 1]]
    i_left = np.radians(left[:, 2])
    i_right = np.radians(right[:, 2])
    node_delta = _wrap_radians(np.radians(left[:, 4] - right[:, 4]))
    cos_plane = (
        np.cos(i_left) * np.cos(i_right)
        + np.sin(i_left) * np.sin(i_right) * np.cos(node_delta)
    )
    plane = np.arccos(np.clip(cos_plane, -1.0, 1.0))
    denominator = np.maximum(np.cos(plane / 2.0), np.finfo(float).eps)
    common_node_term = (
        np.cos((i_left + i_right) / 2.0) * np.sin(node_delta / 2.0) / denominator
    )
    peri_delta = _wrap_radians(
        np.radians(left[:, 3] - right[:, 3])
        + 2.0 * np.arcsin(np.clip(common_node_term, -1.0, 1.0))
    )
    eccentricity_mean = (left[:, 0] + right[:, 0]) / 2.0
    squared = (
        (left[:, 0] - right[:, 0]) ** 2
        + (left[:, 1] - right[:, 1]) ** 2
        + (2.0 * np.sin(plane / 2.0)) ** 2
        + (eccentricity_mean * 2.0 * np.sin(peri_delta / 2.0)) ** 2
    )
    return np.sqrt(np.maximum(squared, 0.0))


def _orbital_lower_bound_embedding(orbits: np.ndarray) -> np.ndarray:
    inclination = np.radians(orbits[:, 2])
    node = np.radians(orbits[:, 4])
    pole = np.column_stack(
        (
            np.sin(inclination) * np.sin(node),
            -np.sin(inclination) * np.cos(node),
            np.cos(inclination),
        )
    )
    return np.column_stack((orbits[:, 0], orbits[:, 1], pole))


def _d_sh_graph(orbits: np.ndarray, threshold: float) -> tuple[list[list[tuple[int, float]]], int]:
    """Build exact D_SH neighbors after a no-false-negative lower-bound query."""

    embedding = _orbital_lower_bound_embedding(orbits)
    possible = cKDTree(embedding).query_pairs(float(threshold), output_type="ndarray")
    distances = southworth_hawkins_pairs(orbits, possible)
    keep = distances <= float(threshold)
    pairs = possible[keep]
    distances = distances[keep]
    adjacency: list[list[tuple[int, float]]] = [[] for _ in range(len(orbits))]
    for (left, right), distance in zip(pairs.tolist(), distances.tolist()):
        adjacency[left].append((right, float(distance)))
        adjacency[right].append((left, float(distance)))
    return adjacency, int(len(possible))


def _circular_mean_deg(values: np.ndarray, weights: np.ndarray) -> float:
    radians = np.radians(values)
    sine = float(np.sum(weights * np.sin(radians)))
    cosine = float(np.sum(weights * np.cos(radians)))
    return float(np.degrees(np.arctan2(sine, cosine)) % 360.0)


def _group_mean(
    members: np.ndarray,
    seed: int,
    orbits: np.ndarray,
    geo: np.ndarray,
    threshold: float,
) -> dict[str, Any]:
    pairs = np.column_stack((np.full(len(members), int(seed), dtype=np.int64), members))
    distances = southworth_hawkins_pairs(orbits, pairs)
    weights = np.maximum(0.0, 1.0 - (distances / float(threshold)) ** 2)
    weights[members == seed] = 1.0
    if not float(weights.sum()):
        weights = np.ones(len(members), dtype=float)
    orbit_mean = np.empty(5, dtype=float)
    orbit_mean[0:3] = np.average(orbits[members, 0:3], axis=0, weights=weights)
    for column in (3, 4):
        orbit_mean[column] = _circular_mean_deg(orbits[members, column], weights)
    geo_mean = np.empty(4, dtype=float)
    geo_mean[0] = _circular_mean_deg(geo[members, 0], weights)
    geo_mean[1] = _circular_mean_deg(geo[members, 1], weights)
    geo_mean[2:] = np.average(geo[members, 2:], axis=0, weights=weights)
    return {
        "members": np.asarray(sorted(int(value) for value in members), dtype=np.int64),
        "orbit_mean": orbit_mean,
        "geo_mean": geo_mean,
        "weight_sum": float(weights.sum()),
    }


def _aggregate_group(groups: list[dict[str, Any]], group_indices: np.ndarray) -> dict[str, Any]:
    members = np.unique(
        np.concatenate([np.asarray(groups[index]["members"], dtype=np.int64) for index in group_indices])
    )
    weights = np.asarray(
        [max(float(groups[index]["weight_sum"]), 1.0) for index in group_indices], dtype=float
    )
    orbit_values = np.vstack([groups[index]["orbit_mean"] for index in group_indices])
    geo_values = np.vstack([groups[index]["geo_mean"] for index in group_indices])
    orbit_mean = np.empty(5, dtype=float)
    orbit_mean[0:3] = np.average(orbit_values[:, 0:3], axis=0, weights=weights)
    for column in (3, 4):
        orbit_mean[column] = _circular_mean_deg(orbit_values[:, column], weights)
    geo_mean = np.empty(4, dtype=float)
    geo_mean[0] = _circular_mean_deg(geo_values[:, 0], weights)
    geo_mean[1] = _circular_mean_deg(geo_values[:, 1], weights)
    geo_mean[2:] = np.average(geo_values[:, 2:], axis=0, weights=weights)
    return {
        "members": members,
        "orbit_mean": orbit_mean,
        "geo_mean": geo_mean,
        "weight_sum": float(weights.sum()),
    }


def _dx_pairs(means: np.ndarray, pairs: np.ndarray) -> np.ndarray:
    if not len(pairs):
        return np.asarray([], dtype=float)
    left = means[pairs[:, 0]]
    right = means[pairs[:, 1]]
    solar = 2.0 * np.sin(_wrap_radians(np.radians(left[:, 0] - right[:, 0])) / 2.0)
    ra = 2.0 * np.sin(_wrap_radians(np.radians(left[:, 1] - right[:, 1])) / 2.0)
    dec = 2.0 * np.sin(np.radians(left[:, 2] - right[:, 2]) / 2.0)
    velocity_delta = np.abs(left[:, 3] - right[:, 3])
    w_solar, w_ra, w_dec, w_velocity = DX_WEIGHTS

    def directed(a: np.ndarray, solar_term: np.ndarray, ra_term: np.ndarray, dec_term: np.ndarray) -> np.ndarray:
        squared = (
            w_solar * solar_term**2
            + w_ra * (velocity_delta + 1.0) * (ra_term * np.cos(np.radians(a[:, 2]))) ** 2
            + w_dec * (velocity_delta + 1.0) * dec_term**2
            + w_velocity * (velocity_delta / np.maximum(a[:, 3], np.finfo(float).eps)) ** 2
        )
        return np.sqrt(np.maximum(squared, 0.0))

    forward = directed(left, solar, ra, dec)
    reverse = directed(right, -solar, -ra, -dec)
    return np.maximum(forward, reverse)


def _merge_dx(groups: list[dict[str, Any]], threshold: float) -> tuple[list[dict[str, Any]], int]:
    """Centroid-link groups by deterministic mutual-nearest rounds.

    Merging an entire threshold graph by connected components creates the
    classic single-linkage chaining failure in dense sporadic data.  The paper
    instead recomputes weighted means and repeats its association step.  Mutual
    nearest centroid rounds make that recomputation explicit and deterministic.
    """

    iterations = 0
    while len(groups) > 1:
        means = np.vstack([group["geo_mean"] for group in groups])
        w_solar, _w_ra, w_dec, _w_velocity = DX_WEIGHTS
        embedding = np.column_stack(
            (
                np.sqrt(w_solar) * np.cos(np.radians(means[:, 0])),
                np.sqrt(w_solar) * np.sin(np.radians(means[:, 0])),
                np.sqrt(w_dec) * np.cos(np.radians(means[:, 2])),
                np.sqrt(w_dec) * np.sin(np.radians(means[:, 2])),
            )
        )
        possible = cKDTree(embedding).query_pairs(float(threshold), output_type="ndarray")
        distances = _dx_pairs(means, possible)
        keep = distances <= float(threshold)
        linked = possible[keep]
        linked_distances = distances[keep]
        if not len(linked):
            break
        best_neighbor = np.full(len(groups), -1, dtype=np.int64)
        best_distance = np.full(len(groups), np.inf, dtype=float)
        for (left, right), distance in zip(linked.tolist(), linked_distances.tolist()):
            for source, target in ((int(left), int(right)), (int(right), int(left))):
                if distance < best_distance[source] or (
                    distance == best_distance[source]
                    and (best_neighbor[source] < 0 or target < best_neighbor[source])
                ):
                    best_distance[source] = float(distance)
                    best_neighbor[source] = target
        paired: set[int] = set()
        components: list[np.ndarray] = []
        for left in range(len(groups)):
            right = int(best_neighbor[left])
            if right <= left or right in paired:
                continue
            if int(best_neighbor[right]) == left:
                components.append(np.asarray([left, right], dtype=np.int64))
                paired.update((left, right))
        if not components:
            break
        components.extend(
            np.asarray([index], dtype=np.int64)
            for index in range(len(groups))
            if index not in paired
        )
        components.sort(key=lambda values: int(values[0]))
        groups = [_aggregate_group(groups, component) for component in components]
        iterations += 1
    return groups, iterations


def edmond_d_criterion_candidates(
    rows: Sequence[Mapping[str, Any]],
    *,
    d_sh_threshold: float = D_SH_THRESHOLD,
    d_x_threshold: float = D_X_THRESHOLD,
    minimum_members: int = MIN_MEMBERS,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return a ranked target-free catalogue using the published EDMOND recipe."""

    required = ("id", "e", "q", "inc", "peri", "node", "sol", "ra", "dec", "vg")
    usable_rows: list[Mapping[str, Any]] = []
    dropped = 0
    for row in rows:
        try:
            values = np.asarray([float(row[key]) for key in required[1:]], dtype=float)
        except (KeyError, TypeError, ValueError):
            dropped += 1
            continue
        if not np.isfinite(values).all() or not (0.0 <= values[0] < 1.5 and 0.0 < values[1] < 2.0):
            dropped += 1
            continue
        usable_rows.append(row)
    if len(usable_rows) < minimum_members:
        return [], {"usable_rows": int(len(usable_rows)), "dropped_rows": int(dropped)}

    event_ids = np.asarray([str(row["id"]) for row in usable_rows], dtype=str)
    orbits = np.asarray(
        [[float(row[key]) for key in ("e", "q", "inc", "peri", "node")] for row in usable_rows],
        dtype=float,
    )
    geo = np.asarray(
        [[float(row[key]) for key in ("sol", "ra", "dec", "vg")] for row in usable_rows],
        dtype=float,
    )
    adjacency, lower_bound_pairs = _d_sh_graph(orbits, d_sh_threshold)
    density = np.asarray(
        [1.0 + sum(1.0 - (distance / d_sh_threshold) ** 2 for _other, distance in neighbors) for neighbors in adjacency],
        dtype=float,
    )
    order = sorted(range(len(orbits)), key=lambda index: (-density[index], event_ids[index]))
    assigned = np.zeros(len(orbits), dtype=bool)
    seed_groups: list[dict[str, Any]] = []
    for seed in order:
        if assigned[seed]:
            continue
        members = [seed]
        members.extend(other for other, _distance in adjacency[seed] if not assigned[other])
        member_array = np.asarray(sorted(set(members)), dtype=np.int64)
        assigned[member_array] = True
        seed_groups.append(_group_mean(member_array, seed, orbits, geo, d_sh_threshold))
    merged_groups, merge_iterations = _merge_dx(seed_groups, d_x_threshold)

    candidates: list[dict[str, Any]] = []
    for group in merged_groups:
        members = np.asarray(group["members"], dtype=np.int64)
        if len(members) < minimum_members:
            continue
        ids = sorted(event_ids[members].tolist())
        family_id = "DSH" + hashlib.sha256("|".join(ids).encode()).hexdigest()[:20]
        candidates.append(
            {
                "family_id": family_id,
                "hierarchy_method": "edmond_dsh_dx_independent_implementation",
                "event_ids": ids,
                "member_count": int(len(ids)),
                "orbit_mean": [float(value) for value in group["orbit_mean"]],
                "geocentric_mean": [float(value) for value in group["geo_mean"]],
                "density_weight_sum": float(group["weight_sum"]),
            }
        )
    candidates.sort(
        key=lambda item: (-int(item["member_count"]), -float(item["density_weight_sum"]), item["family_id"])
    )
    for rank, candidate in enumerate(candidates, start=1):
        candidate["rank"] = rank
    return candidates, {
        "method": "Rudawska_et_al_EDMOND_independent_implementation",
        "truth_accessed": False,
        "input_rows": int(len(rows)),
        "usable_rows": int(len(usable_rows)),
        "dropped_rows": int(dropped),
        "d_sh_threshold": float(d_sh_threshold),
        "d_x_threshold": float(d_x_threshold),
        "minimum_members": int(minimum_members),
        "lower_bound_candidate_pairs": int(lower_bound_pairs),
        "exact_d_sh_edges": int(sum(len(values) for values in adjacency) // 2),
        "seed_groups": int(len(seed_groups)),
        "dx_merge_iterations": int(merge_iterations),
        "catalogue_candidates": int(len(candidates)),
        "ranking": "member_count_desc_then_density_weight_sum_desc",
        "implementation_status": "independent_reimplementation_not_authors_code",
    }


__all__ = [
    "D_SH_THRESHOLD",
    "D_X_THRESHOLD",
    "edmond_d_criterion_candidates",
    "southworth_hawkins_pairs",
]
