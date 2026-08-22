"""Frozen known-shower regression controls for the v3.5 global backbone."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

import numpy as np

from pipeline.pr56_runner.run_gate import load_window, prepare as prepare_gate
from pipeline.unified_v2.controls import (
    CONTROL_WINDOWS,
    _largest_non_target_fraction,
    _score,
)
from pipeline.unified_v2.features import periodic_physical6_from_raw
from pipeline.unified_v2.recurrent_tree import fit_recurrent_hierarchy

from .config import V3Config


def run(config: V3Config | None = None) -> dict[str, Any]:
    config = config or V3Config()
    results: dict[str, Any] = {}
    for index, (name, (start, end, target)) in enumerate(CONTROL_WINDOWS.items()):
        frames = []
        matrices = []
        years = []
        ids = []
        metadata: dict[str, Any] = {}
        for year in (2024, 2025):
            frame, download = load_window(
                f"{name}-{year}",
                start.replace("2025", str(year)),
                end.replace("2025", str(year)),
            )
            data, raw, preparation = prepare_gate(frame, 20260822 + index * 10 + year)
            frames.append(data)
            matrices.append(periodic_physical6_from_raw(raw, config.feature_scales))
            years.append(np.full(len(data), year, dtype=np.int64))
            ids.extend([f"{year}:{value}" for value in data.index.astype(str).tolist()])
            metadata[str(year)] = {**download, **preparation, "rows": int(len(data))}
        matrix = np.vstack(matrices)
        year_array = np.concatenate(years)
        event_ids = np.asarray(ids, dtype=str)
        parents, _leaves, diagnostics = fit_recurrent_hierarchy(
            matrix,
            year_array,
            event_ids,
            config,
            include_leaves=False,
        )
        anchors = parents[: int(config.global_anchor_count)]
        labels = np.concatenate([frame["label"].astype(str).to_numpy() for frame in frames])
        score = _score(labels, anchors, target)
        results[name] = {
            "score": score,
            "largest_non_target_cluster_fraction": _largest_non_target_fraction(
                labels, anchors, target
            ),
            "diagnostics": diagnostics,
            "metadata": metadata,
            "global_anchor_count": int(len(anchors)),
        }
        print(f"{name}: F1={score['f1']:.3f} recall={score['recall']:.3f}", flush=True)
    recovered = sum(
        item["score"]["f1"] >= 0.35
        and item["score"]["precision"] >= 0.35
        and item["score"]["recall"] >= 0.35
        for item in results.values()
    )
    largest = max(item["largest_non_target_cluster_fraction"] for item in results.values())
    return {
        "stage": "acrf_v3_5_global_backbone_known_shower_controls",
        "labels_hidden_until_after_anchor_ranking": True,
        "config": asdict(config),
        "control_windows": CONTROL_WINDOWS,
        "eligible": int(len(results)),
        "recovered": int(recovered),
        "largest_non_target_cluster_fraction": float(largest),
        "verdict": (
            "CONTROL_GATE_PASS"
            if recovered == len(results) and largest <= 0.30
            else "CONTROL_GATE_FAIL"
        ),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "controls_v3_5.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(path), "verdict": result["verdict"]}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
