"""Truth-after-ranking evaluation shared by v2 comparator adapters."""
from __future__ import annotations

from collections import Counter
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
from scipy.optimize import linear_sum_assignment


def _f1(actual: set[str], predicted: set[str]) -> float:
    overlap = len(actual & predicted)
    if not overlap:
        return 0.0
    precision = overlap / len(predicted)
    recall = overlap / len(actual)
    return float(2.0 * precision * recall / (precision + recall))


def evaluate_candidate_catalogue(
    candidates: Sequence[Mapping[str, Any]],
    truth: Mapping[str, str],
    budget: int,
    *,
    minimum_truth_size: int = 4,
) -> dict[str, Any]:
    """Match one ranked catalogue to truth with the archived Hungarian rule."""

    if budget < 1:
        raise ValueError("budget must be positive")
    counts = Counter(str(label) for label in truth.values() if str(label) != "SPORADIC")
    labels = sorted(label for label, count in counts.items() if count >= minimum_truth_size)
    label_sets = {
        label: {str(event_id) for event_id, value in truth.items() if str(value) == label}
        for label in labels
    }
    truth_ids = set(map(str, truth))
    active: list[set[str]] = []
    for candidate in list(candidates)[: int(budget)]:
        members = set(
            map(
                str,
                candidate.get(
                    "final_event_ids",
                    candidate.get("expanded_event_ids", candidate.get("event_ids", ())),
                ),
            )
        ) & truth_ids
        if members:
            active.append(members)
    matrix = np.zeros((len(labels), len(active)), dtype=float)
    for row, label in enumerate(labels):
        for column, predicted in enumerate(active):
            matrix[row, column] = _f1(label_sets[label], predicted)
    size = max(len(labels), len(active), 1)
    cost = np.zeros((size, size), dtype=float)
    cost[: len(labels), : len(active)] = -matrix
    rows, columns = linear_sum_assignment(cost)
    values = [
        float(matrix[row, column]) if column < len(active) else 0.0
        for row, column in zip(rows.tolist(), columns.tolist())
        if row < len(labels)
    ]
    return {
        "eligible_showers": int(len(labels)),
        "candidate_budget": int(budget),
        "candidate_used": int(len(active)),
        "macro_f1": float(np.mean(values)) if values else 0.0,
        "recovered_f1_gt_0_5": int(sum(value > 0.5 for value in values)),
        "matched_f1_values": values,
    }


def compare_to_literature(
    method: Mapping[str, Any],
    literature: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply the frozen strict panel pass rule."""

    passed = bool(
        float(method["macro_f1"]) > float(literature["macro_f1"])
        and int(method["recovered_f1_gt_0_5"]) >= int(literature["recovered"])
    )
    return {
        "method": dict(method),
        "literature": dict(literature),
        "macro_f1_delta": float(method["macro_f1"]) - float(literature["macro_f1"]),
        "recovered_delta": int(method["recovered_f1_gt_0_5"]) - int(literature["recovered"]),
        "passed": passed,
    }


__all__ = ["compare_to_literature", "evaluate_candidate_catalogue"]
