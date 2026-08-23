"""Run the major analysis reporters and regenerate the three figures."""
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_reference_outputs() -> dict[str, object]:
    import pandas as pd

    canonical = pd.read_csv(ROOT / "data/derived/canonical_95.csv")
    discovery = pd.read_csv(ROOT / "data/derived/acrf_discovery_family_123.csv")
    annual = pd.read_csv(ROOT / "data/derived/annual_membership.csv")
    robustness = pd.read_csv(ROOT / "results/acrf_core_hyperparameter_robustness.csv")
    summary = json.loads((ROOT / "results/acrf_core_hyperparameter_robustness.json").read_text())
    mdc = json.loads((ROOT / "results/mdc_duplicate_screen.json").read_text())
    meta = json.loads((ROOT / "data/derived/acrf_baseline_metadata.json").read_text())
    checks = {
        "canonical_rows": len(canonical) == 95,
        "discovery_rows": len(discovery) == 123,
        "annual_total": int(annual["members"].sum()) == 95,
        "robustness_rows": len(robustness) == 153,
        "baseline_rank": meta["rank"] == 7,
        "baseline_members": meta["reported_members"] == 123,
        "baseline_overlap": meta["target_overlap"] == 95,
        "mdc_hard_duplicates": mdc["hard_duplicate_matches"] == 0,
        "mdc_nearest": mdc["nearest_complete_orbit"]["code"] == "NOP",
        "robustness_baseline": summary["baseline_reproduced"] is True,
    }
    if not all(checks.values()):
        raise RuntimeError(f"reference-output validation failed: {checks}")
    return {"checks": checks, "headline": meta}


def run_all(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    validation = validate_reference_outputs()
    for name in ANALYSES:
        subprocess.run([sys.executable, f"analysis/{name}.py", "--out", str(out / f"{name}.json")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "benchmarks/run_benchmarks.py", "--out", str(out / "benchmarks.json")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "figures/generate_figures.py", "--out", str(out / "figures")], cwd=ROOT, check=True)
    reference_paths = (
        (ROOT / "requirements.txt",)
        + tuple(sorted((ROOT / "configs").glob("*.json")))
        + tuple(sorted((ROOT / "data/derived").glob("*")))
        + tuple(sorted((ROOT / "results").glob("*")))
        + tuple(sorted((ROOT / "benchmarks").glob("*.json")))
    )
    manifest = {
        "package": "OrbitTrace reproducibility package",
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
    (out / "reproduction_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "output": str(out), "headline": validation["headline"]}, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="run all analysis reporters and figures")
    parser.add_argument("--out", type=Path, help="output directory; defaults to a temporary directory")
    args = parser.parse_args()
    if not args.all:
        parser.error("use --all to run the complete reproducibility check")
    out = args.out or Path(tempfile.mkdtemp(prefix="orbittrace-reproduction-"))
    run_all(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
