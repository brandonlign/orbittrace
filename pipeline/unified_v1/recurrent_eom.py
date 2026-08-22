"""Exact recurrent-EOM extraction used by the frozen paper method.

This module is copied into the main scientific repository so target application
does not depend on historical implementation files in the Actions runner.
The condensed hierarchy is built once.  Only the EOM stability objective is
replaced by the minimum annual, catalogue-size-normalized stability.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import numpy as np
from hdbscan._hdbscan_tree import compute_stability, get_clusters


def _birth_lambdas(tree: np.ndarray) -> dict[int, float]:
    root = int(tree["parent"].min())
    births: dict[int, float] = {}
    for child, value in zip(tree["child"], tree["lambda_val"]):
        child_id = int(child)
        lam = float(value)
        births[child_id] = min(births.get(child_id, lam), lam)
    births[root] = 0.0
    return births


def _descendant_year_counts(tree: np.ndarray, years: np.ndarray) -> dict[int, np.ndarray]:
    root = int(tree["parent"].min())
    if years.shape != (root,):
        raise ValueError("year vector must align with condensed-tree input points")
    values = tuple(sorted(int(value) for value in np.unique(years)))
    if len(values) != 2:
        raise ValueError(f"recurrent-EOM v1 requires exactly two years, got {values}")
    year_index = {year: index for index, year in enumerate(values)}

    children: dict[int, list[int]] = defaultdict(list)
    nodes: set[int] = set()
    for parent, child in zip(tree["parent"], tree["child"]):
        parent_id = int(parent)
        child_id = int(child)
        children[parent_id].append(child_id)
        nodes.add(parent_id)
        if child_id >= root:
            if child_id <= parent_id:
                raise RuntimeError("HDBSCAN condensed-tree topological order changed")
            nodes.add(child_id)

    counts: dict[int, np.ndarray] = {}
    for node in sorted(nodes, reverse=True):
        total = np.zeros(2, dtype=np.int64)
        for child in children.get(node, []):
            if child < root:
                total[year_index[int(years[child])]] += 1
            else:
                if child not in counts:
                    raise RuntimeError(f"missing descendant count for cluster child {child}")
                total += counts[child]
        counts[node] = total
    return counts


def recurrent_stability(
    tree: np.ndarray,
    years: Iterable[int],
) -> tuple[dict[float, float], dict[int, tuple[float, float]]]:
    """Return frozen recurrent stability and annual normalized contributions."""

    years_array = np.asarray(list(years), dtype=np.int64)
    root = int(tree["parent"].min())
    if years_array.shape != (root,):
        raise ValueError("year vector must align exactly with input points")
    year_values = tuple(sorted(int(value) for value in np.unique(years_array)))
    if len(year_values) != 2:
        raise ValueError("exactly two observing years are required")
    totals = np.asarray([(years_array == year).sum() for year in year_values], dtype=float)
    if np.any(totals <= 0):
        raise ValueError("both observing years must contain events")

    births = _birth_lambdas(tree)
    descendant_counts = _descendant_year_counts(tree, years_array)
    parents = sorted(set(int(value) for value in tree["parent"]))
    annual = {parent: np.zeros(2, dtype=float) for parent in parents}

    for parent, child, lam, child_size in tree:
        parent_id = int(parent)
        child_id = int(child)
        if child_id < root:
            branch = np.asarray(
                [int(years_array[child_id] == year) for year in year_values],
                dtype=np.int64,
            )
        else:
            branch = descendant_counts[child_id]
        if int(branch.sum()) != int(child_size):
            raise RuntimeError("condensed-tree descendant accounting mismatch")
        annual[parent_id] += (float(lam) - births[parent_id]) * branch

    normalized: dict[int, tuple[float, float]] = {}
    recurrent: dict[float, float] = {}
    for parent in parents:
        values = annual[parent] / totals
        normalized[parent] = (float(values[0]), float(values[1]))
        recurrent[float(parent)] = float(min(values[0], values[1]))
    return recurrent, normalized


def eom_labels(tree: np.ndarray, stability: dict[float, float]) -> np.ndarray:
    labels, _probabilities, _stabilities = get_clusters(
        tree,
        dict(stability),
        cluster_selection_method="eom",
        allow_single_cluster=False,
        match_reference_implementation=False,
        cluster_selection_epsilon=0.0,
        max_cluster_size=0,
    )
    return np.asarray(labels, dtype=np.int64)


def leaf_labels(tree: np.ndarray, stability: dict[float, float]) -> tuple[np.ndarray, np.ndarray]:
    """Extract compact leaves from the same condensed hierarchy."""

    labels, probabilities, _stabilities = get_clusters(
        tree,
        dict(stability),
        cluster_selection_method="leaf",
        allow_single_cluster=False,
        match_reference_implementation=False,
        cluster_selection_epsilon=0.0,
        max_cluster_size=0,
    )
    return np.asarray(labels, dtype=np.int64), np.asarray(probabilities, dtype=float)


def parent_labels_through_custom_path(tree: np.ndarray) -> np.ndarray:
    return eom_labels(tree, compute_stability(tree))


def selected_eom_nodes(tree: np.ndarray, stability: dict[float, float]) -> tuple[int, ...]:
    """Mirror HDBSCAN's zero-epsilon EOM node selection for provenance."""

    work = {int(key): float(value) for key, value in stability.items()}
    node_list = sorted(work, reverse=True)[:-1]
    cluster_tree = tree[tree["child_size"] > 1]
    children: dict[int, list[int]] = defaultdict(list)
    for parent, child in zip(cluster_tree["parent"], cluster_tree["child"]):
        children[int(parent)].append(int(child))
    selected = {node: True for node in node_list}

    def descendants(root: int) -> list[int]:
        output: list[int] = []
        queue = [root]
        while queue:
            current = queue.pop(0)
            output.append(current)
            queue.extend(children.get(current, []))
        return output

    for node in node_list:
        subtree = sum(work[child] for child in children.get(node, []))
        if subtree > work[node]:
            selected[node] = False
            work[node] = subtree
        else:
            for child in descendants(node):
                if child != node:
                    selected[child] = False
    return tuple(sorted(node for node, keep in selected.items() if keep))


__all__ = [
    "eom_labels",
    "leaf_labels",
    "parent_labels_through_custom_path",
    "recurrent_stability",
    "selected_eom_nodes",
]
