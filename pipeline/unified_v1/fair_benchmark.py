"""Equal-information SonotaCo benchmark for a recurrent hierarchy."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment

from pipeline.pr57_novel import run_novel_search as base

from .method import UnifiedConfig, jsonable
from .recurrent_application import recurrent_candidates

YEARS = (2013, 2014)
ROUTES = ("sugar", "hdbscan")
ROW_SHA = {
    ("sugar", 2013): "47fb0b700fbf710c7b061eead343016bd8d182756eb0c7f406507c5739e4c4f8",
    ("sugar", 2014): "bc83c113e9a14b1c6e1ef460ca9a40e05df77f3a449fec6064f8910add04c912",
    ("hdbscan", 2013): "2433b556d4a859580ef5431d2307ef34c8fa4c15d42841a2ec7b0c11e5f1f158",
    ("hdbscan", 2014): "206692292b2ca252777e40c13c367880740d8e2576d27615f7ea94b7790e3f55",
}
LITERATURE = {
    ("sugar", 2013): {"budget": 40, "macro_f1": 0.27274487210578285, "recovered": 17},
    ("sugar", 2014): {"budget": 43, "macro_f1": 0.2937898653825594, "recovered": 16},
    ("hdbscan", 2013): {"budget": 14, "macro_f1": 0.2020644054110187, "recovered": 12},
    ("hdbscan", 2014): {"budget": 14, "macro_f1": 0.20960560272614628, "recovered": 11},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def feature_matrix(
    rows: list[dict[str, Any]],
    config: UnifiedConfig,
    representation: str,
) -> np.ndarray:
    solar = np.asarray([float(row["sol"]) for row in rows], dtype=float)
    longitude = np.asarray([float(row["sun_lon"]) for row in rows], dtype=float)
    latitude = np.asarray([float(row["ecl_lat"]) for row in rows], dtype=float)
    speed = np.asarray([float(row["vg"]) for row in rows], dtype=float)
    if representation == "physical4":
        center = base.circ_center(solar)
        raw = np.column_stack((longitude, latitude, speed, base.circ_diff(solar, center)))
        return raw / np.asarray(config.feature_scales, dtype=float)[None, :]
    if representation == "periodic_physical6":
        solar_radians = np.radians(solar)
        longitude_radians = np.radians(longitude)
        solar_scale = 180.0 / (np.pi * config.feature_scales[3])
        longitude_scale = 180.0 / (np.pi * config.feature_scales[0])
        return np.column_stack(
            (
                np.cos(solar_radians) * solar_scale,
                np.sin(solar_radians) * solar_scale,
                np.cos(longitude_radians) * longitude_scale,
                np.sin(longitude_radians) * longitude_scale,
                latitude / config.feature_scales[1],
                speed / config.feature_scales[2],
            )
        )
    raise ValueError(f"unknown representation: {representation}")


def evaluate(candidates: list[dict[str, Any]], truth: dict[str, str], budget: int) -> dict[str, Any]:
    counts = Counter(label for label in truth.values() if label != "SPORADIC")
    labels = sorted(label for label, count in counts.items() if count >= 4)
    truth_ids = set(truth)
    active = []
    for candidate in candidates[:budget]:
        members = set(map(str, candidate["event_ids"])) & truth_ids
        if members:
            active.append((candidate["rank"], candidate["family_id"], members))
    label_sets = {label: {event_id for event_id, value in truth.items() if value == label} for label in labels}
    matrix = np.zeros((len(labels), len(active)), dtype=float)
    for row_index, label in enumerate(labels):
        actual = label_sets[label]
        for column_index, (_rank, _family_id, predicted) in enumerate(active):
            overlap = len(actual & predicted)
            if overlap:
                precision = overlap / len(predicted)
                recall = overlap / len(actual)
                matrix[row_index, column_index] = 2 * precision * recall / (precision + recall)
    size = max(len(labels), len(active))
    cost = np.zeros((size, size), dtype=float)
    cost[: len(labels), : len(active)] = -matrix
    rows, columns = linear_sum_assignment(cost)
    values = [
        float(matrix[row, column]) if column < len(active) else 0.0
        for row, column in zip(rows.tolist(), columns.tolist())
        if row < len(labels)
    ]
    return {
        "eligible_showers": len(labels),
        "candidate_used": len(active),
        "macro_f1": float(np.mean(values)) if values else 0.0,
        "recovered_f1_gt_0_5": int(sum(value > 0.5 for value in values)),
    }


def run(
    rows_root: Path,
    truth_root: Path,
    min_cluster_size: int = 12,
    min_samples: int = 4,
    representation: str = "physical4",
) -> dict[str, Any]:
    config = UnifiedConfig()
    pretruth: dict[str, Any] = {
        "method": f"{representation} recurrent-EOM parent branch",
        "min_cluster_size": int(min_cluster_size),
        "min_samples": int(min_samples),
        "representation": representation,
        "truth_accessed": False,
        "routes": {},
    }
    candidate_payloads: dict[str, list[dict[str, Any]]] = {}
    for route in ROUTES:
        pooled: list[dict[str, Any]] = []
        for year in YEARS:
            path = rows_root / f"{route}_{year}.json"
            if sha256(path) != ROW_SHA[(route, year)]:
                raise RuntimeError(f"{route} {year} row bytes changed")
            pooled.extend(json.loads(path.read_text()))
        years = np.asarray([int(row["year"]) for row in pooled], dtype=np.int64)
        ids = np.asarray([str(row["id"]) for row in pooled], dtype=str)
        candidates, diagnostics = recurrent_candidates(
            feature_matrix(pooled, config, representation),
            years,
            ids,
            include_leaf=False,
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
        )
        candidate_payloads[route] = candidates
        order_hash = hashlib.sha256(
            "\n".join("|".join(candidate["event_ids"]) for candidate in candidates).encode()
        ).hexdigest()
        pretruth["routes"][route] = {
            "diagnostics": diagnostics,
            "candidate_count": len(candidates),
            "candidate_order_membership_sha256": order_hash,
        }

    panels = []
    wins = 0
    for route in ROUTES:
        for year in YEARS:
            literature = LITERATURE[(route, year)]
            truth = json.loads((truth_root / f"truth_{route}_{year}.json").read_text())
            method = evaluate(candidate_payloads[route], truth, literature["budget"])
            passed = bool(
                method["macro_f1"] > literature["macro_f1"]
                and method["recovered_f1_gt_0_5"] >= literature["recovered"]
            )
            wins += int(passed)
            panels.append(
                {
                    "route": route,
                    "year": year,
                    "budget": literature["budget"],
                    "method": method,
                    "literature": literature,
                    "macro_f1_delta": method["macro_f1"] - literature["macro_f1"],
                    "passed": passed,
                }
            )
    representation_name = representation.upper()
    return {
        "verdict": f"{'PASS' if wins == 4 else 'FAIL'}_{representation_name}_RECURRENT_HIERARCHY_LITERATURE_{wins}_OF_4",
        "panel_wins": wins,
        "pretruth": pretruth,
        "panels": panels,
        "temporal_information": "all methods receive pooled 2013+2014 label-free rows before truth",
        "candidate_order": "recurrent-EOM parent ranking; the novel-stream leaf branch is not used on this established-shower benchmark",
        "scope": "established-shower parent branch of the same fitted hierarchy used by the novel-stream leaf branch",
        "truth_loaded_only_after_method_candidates": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows-root", type=Path, required=True)
    parser.add_argument("--truth-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--min-cluster-size", type=int, default=12)
    parser.add_argument("--min-samples", type=int, default=4)
    parser.add_argument("--representation", choices=("physical4", "periodic_physical6"), default="physical4")
    args = parser.parse_args()
    result = run(
        args.rows_root,
        args.truth_root,
        args.min_cluster_size,
        args.min_samples,
        args.representation,
    )
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "fair_benchmark.json"
    path.write_text(json.dumps(jsonable(result), indent=2, sort_keys=True) + "\n")
    print(json.dumps({"verdict": result["verdict"], "panels": result["panels"], "out": str(path)}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
