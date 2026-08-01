#!/usr/bin/env python3
"""Audit the recovered known-shower and weak-injection control outputs.

This verifier intentionally preserves the original v2 aggregate no-go. The
three untouched named showers were recovered and the injection gate passed,
but the v2 gate's largest-cluster rule was infeasible for Eta Aquariids because
the labelled target itself occupied more than the frozen 30% maximum. A
separate prospective holdout is therefore required; this audit does not convert
the historical no-go into a pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path
from typing import Any

SOURCE_COMMIT = "4175e5187fcc6faf3d1befb099a9e35be96850f2"
EXPECTED_ORIGINAL_VERDICT = "NO_GO_DEGENERATE_PARENT_CLUSTER"


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def close(name: str, actual: float, expected: float, tolerance: float) -> float:
    actual = float(actual)
    if not math.isclose(actual, expected, abs_tol=tolerance, rel_tol=0.0):
        raise AssertionError(f"{name}: expected {expected} ± {tolerance}, found {actual}")
    return actual


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("ghoststream_method_control_evidence"))
    parser.add_argument("--environment", type=Path, default=Path("ghoststream_method_environment.txt"))
    parser.add_argument("--source-hashes", type=Path, default=Path("ghoststream_method_source_sha256.txt"))
    args = parser.parse_args()

    recovery = load("ghoststream_results_v2/ghoststream_recovery_gate_v2.json")
    if recovery.get("verdict") != EXPECTED_ORIGINAL_VERDICT:
        raise AssertionError(
            f"Expected preserved historical verdict {EXPECTED_ORIGINAL_VERDICT}, "
            f"found {recovery.get('verdict')}"
        )
    if recovery.get("untouched_eligible") != 3 or recovery.get("untouched_recovered") != 3:
        raise AssertionError("Expected all three untouched named showers to be recovered")

    frozen_maximum = float(recovery["frozen_pass_rule"]["maximum_largest_cluster_fraction"])
    expected_showers = {
        "Lyrids": ("LYR", 0.810, 1.000, 0.895),
        "Eta_Aquariids": ("ETA", 0.904, 1.000, 0.950),
        "Southern_Delta_Aquariids": ("SDA", 0.856, 1.000, 0.922),
    }
    shower_checks: dict[str, Any] = {}
    infeasible_controls: list[str] = []
    for name, (code, precision, recall, f1) in expected_showers.items():
        result = recovery["untouched"][name]
        item = result["score"]
        if item["shower"] != code or item["recovered"] is not True:
            raise AssertionError(f"Unexpected {name} recovery: {item}")
        sampled_rows = int(recovery["metadata"]["untouched"][name]["sampled_rows"])
        true_count = int(item["true_count"])
        observed_recall = float(item["recall"])
        target_prevalence = true_count / sampled_rows
        unavoidable_cluster_fraction = (true_count * observed_recall) / sampled_rows
        rule_infeasible = unavoidable_cluster_fraction > frozen_maximum
        if rule_infeasible:
            infeasible_controls.append(name)
        shower_checks[name] = {
            "code": code,
            "sampled_rows": sampled_rows,
            "true_count": true_count,
            "target_prevalence": target_prevalence,
            "precision": close(f"{name} precision", item["precision"], precision, 0.002),
            "recall": close(f"{name} recall", item["recall"], recall, 0.002),
            "f1": close(f"{name} F1", item["f1"], f1, 0.002),
            "target_cluster_fraction": float(item["cluster_size"]) / sampled_rows,
            "largest_cluster_fraction": float(result["largest_cluster_fraction"]),
            "unavoidable_cluster_fraction_at_observed_recall": unavoidable_cluster_fraction,
            "frozen_maximum_largest_cluster_fraction": frozen_maximum,
            "original_rule_infeasible_for_this_control": rule_infeasible,
        }

    if "Eta_Aquariids" not in infeasible_controls:
        raise AssertionError(
            "Expected Eta Aquariids to demonstrate the mathematical conflict "
            "between target prevalence and the 30% largest-cluster ceiling"
        )

    injection = load("ghoststream_injection_results/ghoststream_injection_gate.json")
    if injection.get("verdict") != "INJECTION_GATE_PASS":
        raise AssertionError(f"Injection gate failed: {injection.get('verdict')}")
    expected_injection = {
        "20": (9, 4, 0.526),
        "40": (9, 7, 0.800),
        "80": (9, 8, 0.870),
    }
    injection_checks: dict[str, Any] = {}
    for size, (runs, recovered, median_f1) in expected_injection.items():
        item = injection["by_size"][size]
        if item["runs"] != runs or item["recovered"] != recovered:
            raise AssertionError(f"Injection n={size}: expected {recovered}/{runs}, found {item}")
        injection_checks[size] = {
            "runs": runs,
            "recovered": recovered,
            "recovery_rate": item["recovery_rate"],
            "median_f1": close(f"injection n={size} median F1", item["median_f1"], median_f1, 0.002),
        }

    output = args.output_dir
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree("ghoststream_results_v2", output / "known_shower_recovery")
    shutil.copytree("ghoststream_injection_results", output / "weak_stream_injection")
    shutil.copy2(args.environment, output / "environment.txt")
    shutil.copy2(args.source_hashes, output / "source_sha256.txt")

    evidence: dict[str, Any] = {
        "status": "RECOVERED_METHOD_CONTROL_AUDIT_NEGATIVE_GATE_INFEASIBLE",
        "source_repository": "brandonlign/remotion-worker",
        "source_commit": SOURCE_COMMIT,
        "scientific_gate_passed": False,
        "corrected_prospective_holdout_required": True,
        "known_shower_recovery": {
            "original_verdict": recovery["verdict"],
            "untouched_recovered": 3,
            "untouched_eligible": 3,
            "frozen_maximum_largest_cluster_fraction": frozen_maximum,
            "infeasible_controls": infeasible_controls,
            "showers": shower_checks,
            "interpretation": (
                "The aggregate no-go is preserved. Eta Aquariids occupied more than "
                "30% of its holdout sample, so a full-recall target cluster could not "
                "satisfy the frozen global largest-cluster ceiling. This is a gate-design "
                "contradiction, not permission to relabel the historical verdict as a pass."
            ),
        },
        "weak_stream_injection": {
            "verdict": injection["verdict"],
            "permutations_per_run": injection["permutations_per_run"],
            "by_size": injection_checks,
        },
    }
    files = []
    for path in sorted(item for item in output.rglob("*") if item.is_file()):
        files.append({
            "path": path.relative_to(output).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    evidence["files"] = files
    (output / "method_controls.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    eta = shower_checks["Eta_Aquariids"]
    lines = [
        "# GhostStream recovered method-control audit",
        "",
        "**Verdict:** `RECOVERED_METHOD_CONTROL_AUDIT_NEGATIVE_GATE_INFEASIBLE`",
        "",
        "The recovered control code was run unchanged from its immutable source commit.",
        "The historical aggregate gate remains a no-go and is not retroactively converted to a pass.",
        "",
        "## Preserved results",
        "",
        "- Original aggregate known-shower verdict: **`NO_GO_DEGENERATE_PARENT_CLUSTER`**",
        "- Untouched named showers individually recovered: **3/3**",
        "- Lyrids: precision 0.810, recall 1.000, F1 0.895",
        "- Eta Aquariids: precision 0.904, recall 1.000, F1 0.950",
        "- Southern Delta Aquariids: precision 0.856, recall 1.000, F1 0.922",
        "- Injection gate: **`INJECTION_GATE_PASS`**",
        "- 20-member injections: **4/9**, median F1 0.526",
        "- 40-member injections: **7/9**, median F1 0.800",
        "- 80-member injections: **8/9**, median F1 0.870",
        "",
        "## Why the aggregate rule was infeasible",
        "",
        f"Eta Aquariids supplied {eta['true_count']} of {eta['sampled_rows']} sampled rows "
        f"({eta['target_prevalence']:.3%}). The frozen rule prohibited any cluster larger "
        f"than {frozen_maximum:.0%}. At the observed recall, any ETA-containing target "
        f"cluster had an unavoidable minimum fraction of "
        f"{eta['unavoidable_cluster_fraction_at_observed_recall']:.3%}.",
        "",
        "A prospective independent-year holdout with the same 30% threshold applied only "
        "to non-target clusters is required. That correction tests the intended failure "
        "mode without making a strong real shower mathematically incapable of passing.",
        "",
    ]
    (output / "METHOD_CONTROLS.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
