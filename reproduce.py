"""Verify the archived OrbitTrace results and regenerate the paper figures."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
ANALYSES = (
    "discovery",
    "earlier_year_confirmation",
    "activity_null",
    "orbital_null",
    "uncertainty_clones",
    "hierarchical_bootstrap",
    "geographic_replication",
    "validation_sensitivity",
    "external_archive_replication",
    "mdc_duplicate_screen",
    "nop004_population_comparison",
    "jpl_parent_body_screen",
    "core_hyperparameter_robustness",
)
EXPECTED_ANNUAL = {2022: 10, 2023: 8, 2024: 14, 2025: 34, 2026: 29}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require(condition: bool, name: str, checks: dict[str, bool]) -> None:
    checks[name] = bool(condition)


def validate_reference_outputs() -> dict[str, object]:
    """Check the invariants that define the archived paper result."""
    import pandas as pd

    canonical = pd.read_csv(ROOT / "data/derived/canonical_95.csv")
    discovery = pd.read_csv(ROOT / "data/derived/acrf_discovery_family_123.csv")
    annual = pd.read_csv(ROOT / "data/derived/annual_membership.csv")
    robustness = pd.read_csv(ROOT / "results/acrf_core_hyperparameter_robustness.csv")

    headline = json.loads((ROOT / "results/paper_headline_results.json").read_text())
    robustness_summary = json.loads(
        (ROOT / "results/acrf_core_hyperparameter_robustness.json").read_text()
    )
    external = json.loads((ROOT / "results/external_replication.json").read_text())
    mdc = json.loads((ROOT / "results/mdc_duplicate_screen.json").read_text())
    meta = json.loads((ROOT / "data/derived/acrf_baseline_metadata.json").read_text())

    checks: dict[str, bool] = {}
    _require(len(canonical) == 95, "canonical_rows", checks)
    _require(len(discovery) == 123, "discovery_rows", checks)
    _require(len(robustness) == 153, "robustness_rows", checks)

    canonical_id_column = "event_id" if "event_id" in canonical.columns else "CurNum"
    canonical_time_column = "Tobs" if "Tobs" in canonical.columns else None
    _require(
        canonical[canonical_id_column].astype(str).is_unique,
        "canonical_ids_unique",
        checks,
    )
    if canonical_time_column:
        _require(
            canonical[canonical_time_column].astype(str).is_unique,
            "canonical_times_unique",
            checks,
        )
    if "timestamp_key" in discovery.columns:
        _require(
            discovery["timestamp_key"].astype(str).is_unique,
            "discovery_timestamps_unique",
            checks,
        )
    if "canonical_target_member" in discovery.columns:
        target = discovery["canonical_target_member"].astype(str).str.lower().eq("true")
        _require(int(target.sum()) == 95, "discovery_contains_95_canonical_members", checks)

    annual_map = {
        int(row.year): int(row.members)
        for row in annual.itertuples(index=False)
    }
    _require(annual_map == EXPECTED_ANNUAL, "annual_counts", checks)
    _require(int(annual["members"].sum()) == 95, "annual_total", checks)

    _require(meta["rank"] == 7, "baseline_rank", checks)
    _require(meta["reported_members"] == 123, "baseline_members", checks)
    _require(meta["target_overlap"] == 95, "baseline_overlap", checks)
    _require(abs(float(meta["recall"]) - 1.0) < 1e-12, "baseline_recall", checks)

    _require(headline["discovery"]["rank"] == 7, "headline_rank", checks)
    _require(
        headline["annual_confirmation"]["members"]
        == {str(k): v for k, v in EXPECTED_ANNUAL.items()},
        "headline_annual_counts",
        checks,
    )
    _require(headline["validation_sensitivity"]["cells"] == 81, "validation_grid_cells", checks)
    _require(headline["validation_sensitivity"]["passing_cells"] == 81, "validation_grid_passes", checks)
    _require(headline["uncertainty_clones"]["passes"] == 1000, "uncertainty_clone_passes", checks)

    _require(robustness_summary["baseline_reproduced"] is True, "robustness_baseline", checks)
    _require(robustness_summary["unique_parameter_settings"] == 153, "robustness_unique_settings", checks)
    _require(robustness_summary["exact_95_recovery_cells"] == 37, "robustness_exact_95", checks)
    _require(robustness_summary["rank_le_100_cells"] == 83, "robustness_rank_le_100", checks)

    _require(external["sources"]["CAMS"]["members"] == 9, "cams_members", checks)
    _require(external["sources"]["SonotaCo"]["members"] == 11, "sonotaco_members", checks)
    _require(external["sources"]["EDMOND"]["members"] == 4, "edmond_members", checks)
    _require(external["independent_networks_passing"] == ["SonotaCo"], "external_formal_pass", checks)

    _require(mdc["hard_duplicate_matches"] == 0, "mdc_hard_duplicates", checks)
    _require(mdc["catalogue"]["submitted_rows_screened"] == 2179, "mdc_rows", checks)
    _require(mdc["nearest_complete_orbit"]["code"] == "NOP", "mdc_nearest_code", checks)
    _require(mdc["nearest_complete_orbit"]["solution"] == "004", "mdc_nearest_solution", checks)

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError(f"archived-result validation failed: {', '.join(failed)}")
    return {"checks": checks, "headline": meta}


def run_all(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    validation = validate_reference_outputs()

    for name in ANALYSES:
        subprocess.run(
            [sys.executable, f"analysis/{name}.py", "--out", str(out / f"{name}.json")],
            cwd=ROOT,
            check=True,
        )

    subprocess.run(
        [sys.executable, "benchmarks/run_benchmarks.py", "--out", str(out / "benchmarks.json")],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [sys.executable, "figures/generate_figures.py", "--out", str(out / "figures")],
        cwd=ROOT,
        check=True,
    )

    reference_paths = (
        (ROOT / "requirements.txt",)
        + tuple(sorted((ROOT / "configs").glob("*.json")))
        + tuple(sorted((ROOT / "data/derived").glob("*")))
        + tuple(sorted((ROOT / "results").glob("*")))
        + tuple(sorted((ROOT / "benchmarks").glob("*.json")))
    )
    manifest = {
        "package": "OrbitTrace",
        "verification_scope": "archived derived data, archived results, benchmark summaries, and figure regeneration",
        "validation": validation,
        "reference_inputs": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in reference_paths
            if path.is_file()
        },
        "generated_outputs": sorted(
            str(path.relative_to(out)) for path in out.rglob("*") if path.is_file()
        ),
    }
    (out / "reproduction_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(
        json.dumps(
            {"status": "PASS", "output": str(out), "checks": len(validation["checks"])},
            indent=2,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="verify archived results and regenerate all three figures")
    parser.add_argument("--out", type=Path, help="output directory; defaults to a temporary directory")
    args = parser.parse_args()
    if not args.all:
        parser.error("use --all to run the complete release check")
    out = args.out or Path(tempfile.mkdtemp(prefix="orbittrace-reproduction-"))
    run_all(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
