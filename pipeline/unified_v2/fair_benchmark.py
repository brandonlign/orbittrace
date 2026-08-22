"""Equal-information v2 benchmark against the archived literature panels."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from .common_evaluator import compare_to_literature, evaluate_candidate_catalogue
from .comparators import literature_comparator_registry
from .config import V2Config
from .crossfit_membership import expand_candidate
from .d_criterion import edmond_d_criterion_candidates
from .features import periodic_physical6_from_mapping
from .full_pipeline import build_full_catalogue
from .partitioned_hierarchy import fit_partitioned_recurrent_hierarchy
from .recurrent_tree import fit_recurrent_hierarchy

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


def _full_v2_candidates(
    rows: list[dict[str, Any]],
    config: V2Config,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Run the exact full-recovery v2 pipeline on one label-free row panel."""

    matrix = periodic_physical6_from_mapping(rows, config.feature_scales)
    years = np.asarray([int(row["year"]) for row in rows], dtype=np.int64)
    event_ids = np.asarray([str(row["id"]) for row in rows], dtype=str)
    solar = np.asarray([float(row["sol"]) for row in rows], dtype=float)
    orbit_matrix = np.asarray(
        [
            [
                float(row["e"]),
                float(row["q"]),
                float(row["inc"]),
                float(row["peri"]),
                float(row["node"]),
            ]
            for row in rows
        ],
        dtype=float,
    )
    parents, leaves, hierarchy_diagnostics = fit_partitioned_recurrent_hierarchy(
        matrix,
        years,
        event_ids,
        solar,
        config,
        include_leaves=True,
    )
    candidates, selection_diagnostics = build_full_catalogue(
        [*parents, *leaves],
        matrix,
        years,
        event_ids,
        orbit_matrix,
        config,
    )
    return candidates, {
        "hierarchy": hierarchy_diagnostics,
        "candidate_selection": selection_diagnostics,
        "pipeline": "unified_v2_full_partitioned_parent_leaf_halo_orbit_gate",
    }


def _legacy_parent_candidates(
    rows: list[dict[str, Any]],
    config: V2Config,
    *,
    halo: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Preserve the previously frozen parent-only benchmark route explicitly."""

    matrix = periodic_physical6_from_mapping(rows, config.feature_scales)
    years = np.asarray([int(row["year"]) for row in rows], dtype=np.int64)
    event_ids = np.asarray([str(row["id"]) for row in rows], dtype=str)
    parents, _leaves, diagnostics = fit_recurrent_hierarchy(
        matrix,
        years,
        event_ids,
        config,
        include_leaves=False,
    )
    candidates = (
        [expand_candidate(candidate, matrix, years, event_ids, config) for candidate in parents]
        if halo
        else parents
    )
    return candidates, {
        "hierarchy": diagnostics,
        "pipeline": "unified_v2_legacy_parent_plus_halo" if halo else "unified_v2_legacy_parent",
    }


def run(
    rows_root: Path,
    truth_root: Path,
    *,
    config: V2Config | None = None,
    pipeline: str = "legacy_parent",
) -> dict[str, Any]:
    config = config or V2Config()
    if pipeline not in {"legacy_parent", "legacy_parent_halo", "full"}:
        raise ValueError("pipeline must be legacy_parent, legacy_parent_halo, or full")
    panels: list[dict[str, Any]] = []
    d_criterion_panels: list[dict[str, Any]] = []
    wins = 0
    d_criterion_wins = 0
    pretruth: dict[str, Any] = {
        "method": (
            "unified v2 full partitioned parent/leaf catalogue plus cross-fitted halo and orbit gate"
            if pipeline == "full"
            else "v2 recurrent parent branch plus cross-fitted halo"
            if pipeline == "legacy_parent_halo"
            else "v2 recurrent parent branch"
        ),
        "pipeline": pipeline,
        "truth_accessed": False,
        "routes": {},
        "comparator_registry": [item.__dict__ for item in literature_comparator_registry()],
    }
    for route in ROUTES:
        rows = _load_rows(rows_root, route)
        if pipeline == "full":
            candidates, diagnostics = _full_v2_candidates(rows, config)
        else:
            candidates, diagnostics = _legacy_parent_candidates(
                rows, config, halo=pipeline == "legacy_parent_halo"
            )
        d_criterion_candidates, d_criterion_diagnostics = edmond_d_criterion_candidates(rows)
        pretruth["routes"][route] = {
            "rows": int(len(rows)),
            "diagnostics": diagnostics,
            "candidate_count": int(len(candidates)),
            "candidate_order_membership_sha256": hashlib.sha256(
                "\n".join("|".join(candidate["event_ids"]) for candidate in candidates).encode()
            ).hexdigest(),
            "d_criterion": d_criterion_diagnostics,
            "d_criterion_candidate_order_membership_sha256": hashlib.sha256(
                "\n".join(
                    "|".join(candidate["event_ids"]) for candidate in d_criterion_candidates
                ).encode()
            ).hexdigest(),
        }
        for year in YEARS:
            literature = LITERATURE[(route, year)]
            truth = json.loads((truth_root / f"truth_{route}_{year}.json").read_text())
            # The archived panels evaluate the pooled ranking against each
            # year's truth projection. Keep that exact information budget.
            method = evaluate_candidate_catalogue(candidates, truth, literature["budget"])
            comparison = compare_to_literature(method, literature)
            wins += int(comparison["passed"])
            panels.append({"route": route, "year": year, "budget": literature["budget"], **comparison})
            d_criterion = evaluate_candidate_catalogue(
                d_criterion_candidates, truth, literature["budget"]
            )
            d_comparison = compare_to_literature(method, {
                "macro_f1": d_criterion["macro_f1"],
                "recovered": d_criterion["recovered_f1_gt_0_5"],
            })
            d_criterion_wins += int(d_comparison["passed"])
            d_criterion_panels.append(
                {
                    "route": route,
                    "year": year,
                    "budget": literature["budget"],
                    "comparator_method": d_criterion,
                    **d_comparison,
                }
            )

    pretruth["truth_loaded_only_after_method_candidates"] = True
    return {
        "verdict": f"{'PASS' if wins == 4 else 'FAIL'}_V2_LITERATURE_{wins}_OF_4",
        "expanded_verdict": (
            f"{'PASS' if wins == 4 and d_criterion_wins == 4 else 'FAIL'}_"
            f"V2_LITERATURE_AND_DCRITERION_{wins + d_criterion_wins}_OF_8"
        ),
        "panel_wins": int(wins),
        "d_criterion_panel_wins": int(d_criterion_wins),
        "pretruth": pretruth,
        "panels": panels,
        "d_criterion_panels": d_criterion_panels,
        "temporal_information": "all methods receive pooled 2013+2014 label-free rows before truth",
        "scope": (
            "Binding archived Sugar/HDBSCAN panels plus a clean-room EDMOND D-criterion "
            "adapter on the exact same rows, truth, candidate budgets, and evaluator."
            if pipeline == "full"
            else "Historical parent-branch characterization retained for provenance; it is not the full v2 recovery pipeline."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows-root", type=Path, required=True)
    parser.add_argument("--truth-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--pipeline",
        choices=("legacy_parent", "legacy_parent_halo", "full"),
        default="legacy_parent",
    )
    args = parser.parse_args()
    result = run(args.rows_root, args.truth_root, pipeline=args.pipeline)
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.out / "fair_benchmark_v2.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(path), "verdict": result["verdict"]}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
