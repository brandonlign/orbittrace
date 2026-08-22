"""Known-shower controls for the selected periodic recurrent hierarchy."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import hdbscan
import numpy as np
from hdbscan._hdbscan_tree import compute_stability

from pipeline.pr56_runner.run_gate import load_window, prepare as prepare_gate

from .method import best_known_cluster, jsonable, largest_non_target_fraction
from .recurrent_application import install_hdbscan_compatibility, periodic_physical6_from_raw
from .recurrent_eom import eom_labels, leaf_labels

CONTROL_WINDOWS = {
    "Lyrids": ("2025-04-19", "2025-04-24", "LYR"),
    "Eta_Aquariids": ("2025-05-03", "2025-05-08", "ETA"),
    "Southern_Delta_Aquariids": ("2025-07-27", "2025-08-01", "SDA"),
}
MIN_CLUSTER_SIZE = 8
MIN_SAMPLES = 4


def hierarchy_clusters(matrix: np.ndarray) -> list[dict[str, Any]]:
    install_hdbscan_compatibility()
    model = hdbscan.HDBSCAN(
        min_cluster_size=MIN_CLUSTER_SIZE,
        min_samples=MIN_SAMPLES,
        cluster_selection_method="eom",
        allow_single_cluster=False,
        prediction_data=False,
    ).fit(matrix)
    tree = model.condensed_tree_._raw_tree
    stability = compute_stability(tree)
    outputs = []
    for method, labels in (
        ("eom", eom_labels(tree, stability)),
        ("leaf", leaf_labels(tree, stability)[0]),
    ):
        for label in sorted(int(value) for value in np.unique(labels) if int(value) >= 0):
            members = np.flatnonzero(labels == label)
            outputs.append(
                {
                    "method": method,
                    "global_cluster": (0 if method == "eom" else 1_000_000) + label,
                    "members": members,
                    "size": int(len(members)),
                }
            )
    return outputs


def run() -> dict[str, Any]:
    results = {}
    for index, (name, (start, end, target)) in enumerate(CONTROL_WINDOWS.items()):
        frame, download = load_window(name, start, end)
        data, raw, prep = prepare_gate(frame, 20260731 + index)
        clusters = hierarchy_clusters(periodic_physical6_from_raw(raw))
        score = best_known_cluster(data["label"], clusters, target)
        results[name] = {
            "score": score,
            "hierarchy_nodes": len(clusters),
            "largest_non_target_cluster_fraction": largest_non_target_fraction(data["label"], clusters, target),
            "metadata": {**download, **prep, "source_rows": int(len(frame))},
        }
        print(f"{name}: F1={score['f1']:.3f} recovered={score['recovered']}", flush=True)
    recovered = sum(bool(item["score"]["recovered"]) for item in results.values())
    largest = max(item["largest_non_target_cluster_fraction"] for item in results.values())
    return {
        "stage": "periodic_physical6_known_shower_controls",
        "min_cluster_size": MIN_CLUSTER_SIZE,
        "min_samples": MIN_SAMPLES,
        "labels_hidden_during_clustering": True,
        "eligible": len(results),
        "recovered": recovered,
        "largest_non_target_cluster_fraction": largest,
        "verdict": "CONTROL_GATE_PASS" if recovered == len(results) and largest <= 0.30 else "CONTROL_GATE_FAIL",
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "controls.json"
    path.write_text(json.dumps(jsonable(result), indent=2, sort_keys=True) + "\n")
    print(json.dumps({"verdict": result["verdict"], "out": str(path)}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
