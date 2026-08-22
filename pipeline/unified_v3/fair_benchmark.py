"""Equal-information MSCR-v3 benchmark against archived literature panels."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from pipeline.unified_v2.common_evaluator import compare_to_literature, evaluate_candidate_catalogue
from pipeline.unified_v2.comparators import literature_comparator_registry
from pipeline.unified_v2.d_criterion import edmond_d_criterion_candidates
from pipeline.unified_v2.fair_benchmark import LITERATURE, ROUTES, ROW_SHA, YEARS
from pipeline.unified_v2.features import periodic_physical6_from_mapping

from .config import V3Config
from .method import build_multiscale_catalogue


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_rows(rows_root: Path, route: str) -> list[dict[str, Any]]:
    pooled: list[dict[str, Any]] = []
    for year in YEARS:
        path = rows_root / f"{route}_{year}.json"
        if _sha256(path) != ROW_SHA[(route, year)]:
            raise RuntimeError(f"{route} {year} row bytes changed")
        pooled.extend(json.loads(path.read_text()))
    return pooled


def _method_inputs(rows: list[dict[str, Any]], config: V3Config) -> tuple[np.ndarray, ...]:
    matrix = periodic_physical6_from_mapping(rows, config.feature_scales)
    years = np.asarray([int(row["year"]) for row in rows], dtype=np.int64)
    event_ids = np.asarray([str(row["id"]) for row in rows], dtype=str)
    solar = np.asarray([float(row["sol"]) for row in rows], dtype=float)
    orbit = np.asarray(
        [[float(row[key]) for key in ("e", "q", "inc", "peri", "node")] for row in rows],
        dtype=float,
    )
    return matrix, years, event_ids, solar, orbit


def _catalogue_hash(candidates: list[dict[str, Any]], key: str) -> str:
    return hashlib.sha256(
        "\n".join("|".join(map(str, candidate.get(key, ()))) for candidate in candidates).encode()
    ).hexdigest()


def run(rows_root: Path, truth_root: Path, config: V3Config | None = None) -> dict[str, Any]:
    config = config or V3Config()
    prepared: dict[str, dict[str, Any]] = {}
    pretruth: dict[str, Any] = {
        "method": "ACRF-v3.5 anchored cross-window recurrent fusion",
        "truth_accessed": False,
        "config": asdict(config),
        "routes": {},
        "comparator_registry": [item.__dict__ for item in literature_comparator_registry()],
    }
    for route in ROUTES:
        rows = _load_rows(rows_root, route)
        matrix, years, event_ids, solar, orbit = _method_inputs(rows, config)
        budget = max(int(LITERATURE[(route, year)]["budget"]) for year in YEARS)
        candidates, diagnostics = build_multiscale_catalogue(
            matrix,
            years,
            event_ids,
            solar,
            orbit,
            config,
            expansion_limit=budget,
        )
        d_candidates, d_diagnostics = edmond_d_criterion_candidates(rows)
        prepared[route] = {
            "candidates": candidates,
            "d_candidates": d_candidates,
            "rows": rows,
        }
        pretruth["routes"][route] = {
            "rows": int(len(rows)),
            "candidate_count": int(len(candidates)),
            "materialized_budget": int(budget),
            "diagnostics": diagnostics,
            "seed_order_membership_sha256": _catalogue_hash(candidates, "event_ids"),
            "final_order_membership_sha256": _catalogue_hash(candidates[:budget], "final_event_ids"),
            "d_criterion": d_diagnostics,
            "d_criterion_order_membership_sha256": _catalogue_hash(d_candidates, "event_ids"),
        }

    panels: list[dict[str, Any]] = []
    d_panels: list[dict[str, Any]] = []
    literature_wins = 0
    d_wins = 0
    for route in ROUTES:
        candidates = prepared[route]["candidates"]
        d_candidates = prepared[route]["d_candidates"]
        for year in YEARS:
            literature = LITERATURE[(route, year)]
            truth = json.loads((truth_root / f"truth_{route}_{year}.json").read_text())
            method = evaluate_candidate_catalogue(candidates, truth, int(literature["budget"]))
            comparison = compare_to_literature(method, literature)
            literature_wins += int(comparison["passed"])
            panels.append({"route": route, "year": year, **comparison})
            d_method = evaluate_candidate_catalogue(d_candidates, truth, int(literature["budget"]))
            d_comparison = compare_to_literature(
                method,
                {
                    "macro_f1": d_method["macro_f1"],
                    "recovered": d_method["recovered_f1_gt_0_5"],
                },
            )
            d_wins += int(d_comparison["passed"])
            d_panels.append(
                {
                    "route": route,
                    "year": year,
                    "comparator_method": d_method,
                    **d_comparison,
                }
            )
    pretruth["truth_loaded_only_after_all_ranked_final_memberships"] = True
    pretruth["truth_accessed"] = True
    return {
        "verdict": f"{'PASS' if literature_wins == 4 else 'FAIL'}_ACRF_V3_5_LITERATURE_{literature_wins}_OF_4",
        "expanded_verdict": (
            f"{'PASS' if literature_wins == 4 and d_wins == 4 else 'FAIL'}_"
            f"ACRF_V3_5_LITERATURE_AND_DCRITERION_{literature_wins + d_wins}_OF_8"
        ),
        "literature_panel_wins": int(literature_wins),
        "d_criterion_panel_wins": int(d_wins),
        "pretruth": pretruth,
        "panels": panels,
        "d_criterion_panels": d_panels,
        "temporal_information": "all methods receive pooled 2013+2014 label-free rows before truth",
        "scope": "same rows, truth projections, candidate budgets, Hungarian macro-F1 evaluator, and final-membership semantics",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows-root", type=Path, required=True)
    parser.add_argument("--truth-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.rows_root, args.truth_root)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "fair_benchmark_v3.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(path), "verdict": result["verdict"]}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
