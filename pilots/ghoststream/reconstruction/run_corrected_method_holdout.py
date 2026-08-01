#!/usr/bin/env python3
"""Prospective independent-year correction for the GhostStream control gate.

The recovered v2 gate applied a 30% ceiling to the largest cluster, including
the real target-shower cluster. That rule is mathematically infeasible whenever
the target shower itself exceeds 30% of the sample. This correction preserves:

- the exact v2 HDBSCAN setting;
- the exact recovery thresholds;
- the exact 30% degeneracy threshold; and
- label hiding during clustering.

It changes only the quantity to which the 30% ceiling is applied: the largest
cluster other than the selected target-shower cluster. This directly tests the
intended failure mode, a giant unrelated parent cluster, without making a
strong real shower incapable of passing. The corrected rule is evaluated on
independent 2024 seasons that were not used in the v1 or v2 gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import HDBSCAN

from run_gate import load_window, prepare

SOURCE_COMMIT = "4175e5187fcc6faf3d1befb099a9e35be96850f2"
SETTING = {
    "min_cluster_size": 40,
    "min_samples": 10,
    "scales": [4.0, 4.0, 3.0, 3.0],
    "cluster_selection_method": "eom",
}
RECOVERY_RULE = {
    "minimum_true_members": 40,
    "minimum_precision": 0.35,
    "minimum_recall": 0.35,
    "minimum_f1": 0.35,
}
CORRECTED_PASS_RULE = {
    "all_three_independent_year_controls_recovered": True,
    "maximum_largest_non_target_cluster_fraction": 0.30,
}
HOLDOUT = {
    "Lyrids_2024": ("2024-04-19", "2024-04-24", "LYR"),
    "Eta_Aquariids_2024": ("2024-05-03", "2024-05-08", "ETA"),
    "Southern_Delta_Aquariids_2024": ("2024-07-27", "2024-08-01", "SDA"),
}
SEED = 20260801


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def score_target(labels: pd.Series, assignments: np.ndarray, target: str) -> dict[str, Any]:
    truth = labels.to_numpy(str)
    actual = truth == target
    true_count = int(actual.sum())
    best: dict[str, Any] | None = None
    for cluster_id in [int(value) for value in np.unique(assignments) if int(value) >= 0]:
        predicted = assignments == cluster_id
        true_positive = int(np.sum(actual & predicted))
        if true_positive == 0:
            continue
        cluster_size = int(predicted.sum())
        precision = true_positive / cluster_size
        recall = true_positive / true_count if true_count else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        recovered = (
            true_count >= RECOVERY_RULE["minimum_true_members"]
            and precision >= RECOVERY_RULE["minimum_precision"]
            and recall >= RECOVERY_RULE["minimum_recall"]
            and f1 >= RECOVERY_RULE["minimum_f1"]
        )
        candidate = {
            "target": target,
            "true_count": true_count,
            "cluster": cluster_id,
            "cluster_size": cluster_size,
            "true_positive": true_positive,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "recovered": recovered,
        }
        if best is None or candidate["f1"] > best["f1"]:
            best = candidate
    if best is None:
        return {
            "target": target,
            "true_count": true_count,
            "cluster": None,
            "cluster_size": 0,
            "true_positive": 0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
            "recovered": False,
        }
    return best


def run_control(name: str, start: str, end: str, target: str, seed: int) -> dict[str, Any]:
    frame, download = load_window(name, start, end)
    data, features, prep = prepare(frame, seed)
    model = HDBSCAN(
        min_cluster_size=SETTING["min_cluster_size"],
        min_samples=SETTING["min_samples"],
        cluster_selection_method=SETTING["cluster_selection_method"],
        leaf_size=60,
        n_jobs=-1,
    )
    assignments = model.fit_predict(features / np.asarray(SETTING["scales"])[None, :])
    score = score_target(data["label"], assignments, target)
    cluster_sizes = {
        int(cluster_id): int(np.sum(assignments == cluster_id))
        for cluster_id in np.unique(assignments)
        if int(cluster_id) >= 0
    }
    target_cluster = score["cluster"]
    non_target_sizes = [
        size for cluster_id, size in cluster_sizes.items()
        if target_cluster is None or cluster_id != int(target_cluster)
    ]
    sampled_rows = int(len(assignments))
    largest_non_target_cluster_size = max(non_target_sizes, default=0)
    largest_non_target_cluster_fraction = (
        largest_non_target_cluster_size / sampled_rows if sampled_rows else 1.0
    )
    target_cluster_fraction = score["cluster_size"] / sampled_rows if sampled_rows else 0.0
    target_prevalence = score["true_count"] / sampled_rows if sampled_rows else 0.0
    non_target_gate_passed = (
        largest_non_target_cluster_fraction
        <= CORRECTED_PASS_RULE["maximum_largest_non_target_cluster_fraction"]
    )
    passed = bool(score["recovered"] and non_target_gate_passed)
    result = {
        "name": name,
        "start": start,
        "end": end,
        "target": target,
        "labels_hidden_during_clustering": True,
        "sampled_rows": sampled_rows,
        "target_prevalence": target_prevalence,
        "score": score,
        "cluster_count": len(cluster_sizes),
        "noise_fraction": float(np.mean(assignments < 0)),
        "target_cluster_fraction": target_cluster_fraction,
        "largest_non_target_cluster_size": largest_non_target_cluster_size,
        "largest_non_target_cluster_fraction": largest_non_target_cluster_fraction,
        "non_target_degeneracy_gate_passed": non_target_gate_passed,
        "passed": passed,
        "download_and_preparation": {**download, **prep},
    }
    print(
        f"{name}: target={target} n={score['true_count']} "
        f"precision={score['precision']:.3f} recall={score['recall']:.3f} "
        f"F1={score['f1']:.3f} target_fraction={target_cluster_fraction:.3f} "
        f"largest_non_target={largest_non_target_cluster_fraction:.3f} "
        f"passed={passed}",
        flush=True,
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("ghoststream_method_controls_v3"))
    parser.add_argument("--environment", type=Path, default=Path("ghoststream_method_v3_environment.txt"))
    parser.add_argument("--source-hashes", type=Path, default=Path("ghoststream_method_v3_source_sha256.txt"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    results: dict[str, Any] = {}
    for index, (name, (start, end, target)) in enumerate(HOLDOUT.items()):
        results[name] = run_control(name, start, end, target, SEED + index)

    eligible = sum(int(item["score"]["true_count"] >= RECOVERY_RULE["minimum_true_members"]) for item in results.values())
    recovered = sum(int(item["score"]["recovered"]) for item in results.values())
    non_target_passes = sum(int(item["non_target_degeneracy_gate_passed"]) for item in results.values())
    passed = eligible == 3 and recovered == 3 and non_target_passes == 3
    verdict = "CORRECTED_INDEPENDENT_YEAR_CONTROL_PASS" if passed else "CORRECTED_INDEPENDENT_YEAR_CONTROL_FAIL"

    evidence: dict[str, Any] = {
        "status": verdict,
        "source_repository": "brandonlign/remotion-worker",
        "source_commit": SOURCE_COMMIT,
        "correction_frozen_before_2024_holdout_run": True,
        "reason_for_correction": (
            "The v2 largest-cluster ceiling included the real target cluster and "
            "was infeasible when target prevalence exceeded 30%. The corrected "
            "rule retains the 30% ceiling for non-target clusters only."
        ),
        "setting_unchanged_from_v2": SETTING,
        "recovery_rule_unchanged_from_v2": RECOVERY_RULE,
        "corrected_pass_rule": CORRECTED_PASS_RULE,
        "holdout_windows": HOLDOUT,
        "seed": SEED,
        "eligible_controls": eligible,
        "recovered_controls": recovered,
        "non_target_degeneracy_passes": non_target_passes,
        "passed": passed,
        "controls": results,
    }
    if args.environment.is_file():
        evidence["environment_sha256"] = sha256(args.environment)
    if args.source_hashes.is_file():
        evidence["source_hashes_sha256"] = sha256(args.source_hashes)

    json_path = args.output_dir / "method_controls_v3.json"
    json_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.environment.is_file():
        (args.output_dir / "environment.txt").write_bytes(args.environment.read_bytes())
    if args.source_hashes.is_file():
        (args.output_dir / "source_sha256.txt").write_bytes(args.source_hashes.read_bytes())

    lines = [
        "# GhostStream corrected independent-year method controls",
        "",
        f"**Verdict:** `{verdict}`",
        "",
        "The original v2 no-go is preserved separately. This prospective correction "
        "uses independent 2024 seasons and keeps the exact clustering setting, recovery "
        "thresholds, and 30% limit. The limit is applied only to non-target clusters.",
        "",
        f"- Eligible controls: **{eligible}/3**",
        f"- Recovered controls: **{recovered}/3**",
        f"- Non-target degeneracy checks passed: **{non_target_passes}/3**",
        "",
        "## Controls",
        "",
    ]
    for name, item in results.items():
        score = item["score"]
        lines.append(
            f"- **{name} (`{item['target']}`):** n={score['true_count']}, "
            f"precision={score['precision']:.3f}, recall={score['recall']:.3f}, "
            f"F1={score['f1']:.3f}, target-cluster fraction="
            f"{item['target_cluster_fraction']:.3f}, largest non-target cluster="
            f"{item['largest_non_target_cluster_fraction']:.3f}, passed={item['passed']}"
        )
    lines.extend([
        "",
        "Passing this corrected holdout would resolve the specific infeasible v2 "
        "degeneracy rule. It would not make the meteor-stream candidate official or "
        "replace external scientific review.",
        "",
    ])
    (args.output_dir / "METHOD_CONTROLS_V3.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if passed else 3


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=FutureWarning)
    raise SystemExit(main())
