"""CLI for the unified recurrent hierarchy detector."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from pipeline.pr57_novel import run_novel_search as base
from pipeline.pr56_runner.run_gate import load_window, prepare as prepare_gate

from .method import (
    UnifiedConfig,
    best_known_cluster,
    cluster_hierarchy,
    jsonable,
    largest_non_target_fraction,
    reveal_target_overlap,
    reveal_full_history_overlap,
    scan_month,
    serializable_candidate,
)


CONTROL_WINDOWS = {
    "Lyrids": ("2025-04-19", "2025-04-24", "LYR"),
    "Eta_Aquariids": ("2025-05-03", "2025-05-08", "ETA"),
    "Southern_Delta_Aquariids": ("2025-07-27", "2025-08-01", "SDA"),
}
INJECTION_BACKGROUNDS = {
    "February": ("2025-02-10", "2025-02-16"),
    "June": ("2025-06-10", "2025-06-16"),
    "September": ("2025-09-10", "2025-09-16"),
}
INJECTION_SIZES = (20, 40, 80)
INJECTION_SEEDS = (11, 29, 47)
INJECTION_SIGMA = np.asarray([1.2, 0.8, 1.2, 1.2], dtype=float)
MAX_BACKGROUND = 12000


def run_controls(config: UnifiedConfig) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for index, (name, (start, end, target)) in enumerate(CONTROL_WINDOWS.items()):
        frame, download = load_window(name, start, end)
        data, raw_features, prep = prepare_gate(frame, 20260731 + index)
        clusters = cluster_hierarchy(raw_features, config)
        score = best_known_cluster(data["label"], clusters, target)
        results[name] = {
            "score": score,
            "hierarchy_nodes": len(clusters),
            "largest_non_target_cluster_fraction": largest_non_target_fraction(data["label"], clusters, target),
            "metadata": {
                **download,
                **prep,
                "source_rows": int(len(frame)),
            },
        }
        print(
            f"{name}: method={score['method']} precision={score['precision']:.3f} "
            f"recall={score['recall']:.3f} F1={score['f1']:.3f} recovered={score['recovered']}",
            flush=True,
        )
    eligible = len(results)
    recovered = sum(bool(item["score"]["recovered"]) for item in results.values())
    largest = max((item["largest_non_target_cluster_fraction"] for item in results.values()), default=1.0)
    return {
        "stage": "unified_hierarchy_known_shower_controls",
        "labels_hidden_during_clustering": True,
        "control_windows": CONTROL_WINDOWS,
        "frozen_recovery_rule": {"precision": 0.35, "recall": 0.35, "f1": 0.35},
        "frozen_non_target_rule": {"maximum_largest_non_target_cluster_fraction": 0.30},
        "eligible": eligible,
        "recovered": recovered,
        "largest_non_target_cluster_fraction": largest,
        "verdict": "CONTROL_GATE_PASS" if recovered == eligible and largest <= 0.30 else "CONTROL_GATE_FAIL",
        "results": results,
    }


def valid_injection_centers(features: np.ndarray) -> np.ndarray:
    return (
        (np.abs(features[:, 0]) < 170.0)
        & (np.abs(features[:, 1]) < 80.0)
        & (features[:, 2] > 10.0)
        & (features[:, 2] < 70.0)
        & (np.abs(features[:, 3]) < 2.0)
    )


def inject(background: np.ndarray, size: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    candidates = np.flatnonzero(valid_injection_centers(background))
    if candidates.size == 0:
        raise RuntimeError("no valid injection centers")
    center = background[int(rng.choice(candidates))].copy()
    stream = rng.normal(center, INJECTION_SIGMA, size=(size, 4))
    stream[:, 0] = (stream[:, 0] + 180.0) % 360.0 - 180.0
    stream[:, 1] = np.clip(stream[:, 1], -89.0, 89.0)
    stream[:, 2] = np.clip(stream[:, 2], 5.1, 74.9)
    combined = np.vstack([background, stream])
    truth = np.zeros(len(combined), dtype=bool)
    truth[-size:] = True
    return combined, truth


def best_member_set(clusters: list[dict[str, Any]], truth: np.ndarray) -> dict[str, Any]:
    best = {"method": None, "cluster": None, "cluster_size": 0, "true_positive": 0, "precision": 0.0, "recall": 0.0, "f1": 0.0}
    positive_count = int(truth.sum())
    for cluster in clusters:
        predicted = np.zeros(len(truth), dtype=bool)
        predicted[np.asarray(cluster["members"], dtype=int)] = True
        true_positive = int(np.sum(predicted & truth))
        if not true_positive:
            continue
        size = int(predicted.sum())
        precision = true_positive / size
        recall = true_positive / positive_count if positive_count else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        if f1 > best["f1"]:
            best = {
                "method": cluster["method"],
                "cluster": int(cluster["global_cluster"]),
                "cluster_size": size,
                "true_positive": true_positive,
                "precision": float(precision),
                "recall": float(recall),
                "f1": float(f1),
            }
    return best


def injection_p_value(clusters: list[dict[str, Any]], truth: np.ndarray, rng: np.random.Generator) -> float:
    observed = best_member_set(clusters, truth)["f1"]
    count = int(truth.sum())
    null_values = []
    for _ in range(99):
        indices = rng.choice(len(truth), size=count, replace=False)
        permuted = np.zeros(len(truth), dtype=bool)
        permuted[indices] = True
        null_values.append(best_member_set(clusters, permuted)["f1"])
    return float((1 + sum(value >= observed for value in null_values)) / 100)


def run_injections(config: UnifiedConfig) -> dict[str, Any]:
    backgrounds: dict[str, np.ndarray] = {}
    metadata: dict[str, Any] = {}
    for index, (name, (start, end)) in enumerate(INJECTION_BACKGROUNDS.items()):
        frame, download = load_window(name, start, end)
        prepared = base.prepare(frame, 2025, int(start[5:7]))
        data = prepared["data"]
        raw = prepared["raw"]
        sporadic = raw[data["label"].to_numpy(str) == "SPORADIC"]
        rng = np.random.default_rng(7000 + index)
        if len(sporadic) > MAX_BACKGROUND:
            sporadic = sporadic[rng.choice(len(sporadic), size=MAX_BACKGROUND, replace=False)]
        if len(sporadic) < 3000:
            raise RuntimeError(f"insufficient background for {name}")
        backgrounds[name] = sporadic
        metadata[name] = {
            **download,
            "quality_sporadics": int(len(data)),
            "source_rows": int(len(frame)),
            "sporadic_background_rows": int(len(sporadic)),
        }
    runs = []
    for background_index, (name, background) in enumerate(backgrounds.items()):
        for size in INJECTION_SIZES:
            for seed in INJECTION_SEEDS:
                rng = np.random.default_rng(100000 * background_index + 1000 * size + seed)
                combined, truth = inject(background, size, rng)
                clusters = cluster_hierarchy(combined, config)
                score = best_member_set(clusters, truth)
                p_value = injection_p_value(clusters, truth, rng)
                recovered = bool(
                    score["precision"] >= 0.50
                    and score["recall"] >= 0.50
                    and score["f1"] >= 0.50
                    and p_value <= 0.01
                )
                item = {
                    "background": name,
                    "injection_size": size,
                    "seed": seed,
                    "score": score,
                    "permutation_p": p_value,
                    "hierarchy_nodes": len(clusters),
                    "recovered": recovered,
                }
                runs.append(item)
                print(
                    f"{name} n={size} seed={seed}: precision={score['precision']:.3f} "
                    f"recall={score['recall']:.3f} F1={score['f1']:.3f} p={p_value:.3f} recovered={recovered}",
                    flush=True,
                )
    by_size = {}
    for size in INJECTION_SIZES:
        subset = [item for item in runs if item["injection_size"] == size]
        by_size[str(size)] = {
            "runs": len(subset),
            "recovered": sum(bool(item["recovered"]) for item in subset),
            "recovery_rate": sum(bool(item["recovered"]) for item in subset) / len(subset),
            "median_f1": float(np.median([item["score"]["f1"] for item in subset])),
        }
    verdict = "INJECTION_GATE_PASS" if by_size["40"]["recovery_rate"] >= 0.50 and by_size["80"]["recovery_rate"] >= 0.80 else "INJECTION_GATE_FAIL"
    return {
        "stage": "unified_hierarchy_weak_stream_injection",
        "labels_visible_to_clustering": False,
        "background_windows": INJECTION_BACKGROUNDS,
        "permutations_per_run": 99,
        "frozen_recovery_rule": {"precision": 0.50, "recall": 0.50, "f1": 0.50, "permutation_p_max": 0.01},
        "frozen_pass_rule": {"n40_minimum_rate": 0.50, "n80_minimum_rate": 0.80},
        "by_size": by_size,
        "verdict": verdict,
        "metadata": metadata,
        "runs": runs,
    }


def run_blind(
    discovery_year: int,
    months: tuple[int, ...],
    validation_years: tuple[int, ...],
    config: UnifiedConfig,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    catalog = base.parse_iau()
    all_candidates: list[dict[str, Any]] = []
    month_meta: dict[str, Any] = {}
    for month in months:
        key = f"{discovery_year}-{month:02d}"
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                candidates, meta = scan_month(discovery_year, month, catalog, config)
                all_candidates.extend(candidates)
                meta["download_attempts"] = attempt + 1
                month_meta[key] = meta
                last_error = None
                break
            except Exception as exc:
                last_error = exc
                print(f"{key}: attempt {attempt + 1}/3 ERROR {exc}", flush=True)
        if last_error is not None:
            month_meta[key] = {"error": f"{type(last_error).__name__}: {last_error}", "download_attempts": 3}
    all_candidates.sort(key=lambda item: item["score"], reverse=True)
    shortlisted = all_candidates[:30]
    cache: dict[tuple[int, int], dict[str, Any]] = {}
    final = []
    for index, candidate in enumerate(shortlisted, start=1):
        candidate["validation"] = {str(year): base.validate(candidate, year, cache) for year in validation_years}
        replicated = all(item["passed"] for item in candidate["validation"].values())
        candidate["clone_stability"] = base.clone_stability(candidate) if replicated else {"passed": False, "not_run": True}
        candidate["novel_discovery_gate_passed"] = bool(replicated and candidate["clone_stability"]["passed"])
        if candidate["novel_discovery_gate_passed"]:
            final.append(candidate)
        print(
            f"candidate {index}/{len(shortlisted)} month={candidate['month']:02d} "
            f"method={candidate['hierarchy_method']} n={candidate['members_discovery']} "
            f"replication={replicated} clone={candidate['clone_stability'].get('passed')} final={candidate['novel_discovery_gate_passed']}",
            flush=True,
        )
    result = {
        "stage": "unified_hierarchy_blind_discovery",
        "discovery_year": discovery_year,
        "validation_years": validation_years,
        "months": month_meta,
        "iau_solutions_parsed": len(catalog),
        "prevalidation_candidates": len(all_candidates),
        "validated_candidates": len(shortlisted),
        "survivors": len(final),
        "verdict": "NOVEL_CANDIDATE_SURVIVES_FULL_GATE" if final else "NO_NOVEL_CANDIDATE_SURVIVES_FULL_GATE",
        "candidates": [serializable_candidate(item) for item in shortlisted],
    }
    return result, all_candidates


def parser() -> argparse.ArgumentParser:
    output = argparse.ArgumentParser(description=__doc__)
    output.add_argument("mode", choices=("controls", "injections", "blind"))
    output.add_argument("--out", type=Path, required=True)
    output.add_argument("--target", type=Path, default=None)
    output.add_argument("--months", default="1,2,3,4,5,6,7")
    output.add_argument("--discovery-year", type=int, default=2026)
    output.add_argument("--validation-years", default="2025,2024,2023,2022")
    return output


def main() -> int:
    args = parser().parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    config = UnifiedConfig()
    (args.out / "CONFIG.json").write_text(json.dumps(jsonable(config.__dict__), indent=2, sort_keys=True) + "\n")
    if args.mode == "controls":
        result = run_controls(config)
        (args.out / "controls.json").write_text(json.dumps(jsonable(result), indent=2, sort_keys=True) + "\n")
    elif args.mode == "injections":
        result = run_injections(config)
        (args.out / "injections.json").write_text(json.dumps(jsonable(result), indent=2, sort_keys=True) + "\n")
    else:
        months = tuple(int(value) for value in args.months.split(",") if value)
        validation_years = tuple(int(value) for value in args.validation_years.split(",") if value)
        result, candidates = run_blind(args.discovery_year, months, validation_years, config)
        if args.target is not None:
            result["posthoc_target_reveal"] = reveal_target_overlap(candidates, args.target, args.discovery_year)
            result["posthoc_full_history_reveal"] = reveal_full_history_overlap(
                candidates, args.target, args.discovery_year
            )
        (args.out / "blind.json").write_text(json.dumps(jsonable(result), indent=2, sort_keys=True) + "\n")
    print(json.dumps({"mode": args.mode, "verdict": result["verdict"], "out": str(args.out)}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
