"""Known-shower controls for the v2 recurrent tree branch."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from pipeline.pr56_runner.run_gate import load_window, prepare as prepare_gate

from .config import V2Config
from .features import periodic_physical6_from_raw
from .recurrent_tree import fit_recurrent_hierarchy

CONTROL_WINDOWS = {
    "Lyrids": ("2025-04-19", "2025-04-24", "LYR"),
    "Eta_Aquariids": ("2025-05-03", "2025-05-08", "ETA"),
    "Southern_Delta_Aquariids": ("2025-07-27", "2025-08-01", "SDA"),
}


def _score(labels: np.ndarray, candidates: list[dict[str, Any]], target: str) -> dict[str, Any]:
    actual = labels == str(target)
    total = int(actual.sum())
    best: dict[str, Any] | None = None
    for candidate in candidates:
        members = np.asarray(candidate["members"], dtype=int)
        predicted = np.zeros(len(labels), dtype=bool)
        predicted[members] = True
        overlap = int(np.sum(actual & predicted))
        if not overlap:
            continue
        precision = overlap / len(members)
        recall = overlap / total if total else 0.0
        f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
        item = {
            "family_id": candidate["family_id"],
            "hierarchy_method": candidate["hierarchy_method"],
            "member_count": int(len(members)),
            "true_count": total,
            "overlap": overlap,
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
        }
        if best is None or item["f1"] > best["f1"]:
            best = item
    return best or {
        "family_id": None,
        "hierarchy_method": None,
        "member_count": 0,
        "true_count": total,
        "overlap": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    }


def _largest_non_target_fraction(labels: np.ndarray, candidates: list[dict[str, Any]], target: str) -> float:
    output = 0.0
    for candidate in candidates:
        members = np.asarray(candidate["members"], dtype=int)
        if len(members) and not bool(np.any(labels[members] == str(target))):
            output = max(output, len(members) / len(labels))
    return float(output)


def run(config: V2Config | None = None) -> dict[str, Any]:
    config = config or V2Config()
    results: dict[str, Any] = {}
    for index, (name, (start, end, target)) in enumerate(CONTROL_WINDOWS.items()):
        frames = []
        matrices = []
        years = []
        ids = []
        metadata: dict[str, Any] = {}
        for year in (2024, 2025):
            frame, download = load_window(f"{name}-{year}", start.replace("2025", str(year)), end.replace("2025", str(year)))
            data, raw, prep = prepare_gate(frame, 20260731 + index * 10 + year)
            frames.append(data)
            matrices.append(periodic_physical6_from_raw(raw, config.feature_scales))
            years.append(np.full(len(data), year, dtype=np.int64))
            ids.extend([f"{year}:{value}" for value in data.index.astype(str).tolist()])
            metadata[str(year)] = {**download, **prep, "rows": int(len(data))}
        matrix = np.vstack(matrices)
        year_array = np.concatenate(years)
        event_ids = np.asarray(ids, dtype=str)
        parents, leaves, diagnostics = fit_recurrent_hierarchy(matrix, year_array, event_ids, config)
        candidates = parents + leaves
        labels = np.concatenate([frame["label"].astype(str).to_numpy() for frame in frames])
        score = _score(labels, candidates, target)
        results[name] = {
            "score": score,
            "largest_non_target_cluster_fraction": _largest_non_target_fraction(labels, candidates, target),
            "diagnostics": diagnostics,
            "metadata": metadata,
            "candidate_count": int(len(candidates)),
        }
        print(f"{name}: F1={score['f1']:.3f} recall={score['recall']:.3f}", flush=True)
    recovered = sum(item["score"]["f1"] >= 0.35 and item["score"]["precision"] >= 0.35 and item["score"]["recall"] >= 0.35 for item in results.values())
    largest = max(item["largest_non_target_cluster_fraction"] for item in results.values())
    return {
        "stage": "unified_v2_two_year_known_shower_controls",
        "labels_hidden_during_clustering": True,
        "control_windows": CONTROL_WINDOWS,
        "eligible": len(results),
        "recovered": int(recovered),
        "largest_non_target_cluster_fraction": float(largest),
        "verdict": "CONTROL_GATE_PASS" if recovered == len(results) and largest <= 0.30 else "CONTROL_GATE_FAIL",
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "controls_v2.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(path), "verdict": result["verdict"]}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
