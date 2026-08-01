#!/usr/bin/env python3
"""Verify the recovered known-shower and weak-injection control gates."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path
from typing import Any

SOURCE_COMMIT = "4175e5187fcc6faf3d1befb099a9e35be96850f2"


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
    if recovery.get("verdict") != "RECOVERY_GATE_PASS":
        raise AssertionError(f"Known-shower recovery gate failed: {recovery.get('verdict')}")
    if recovery.get("untouched_eligible") != 3 or recovery.get("untouched_recovered") != 3:
        raise AssertionError("Expected all three untouched known showers to recover")
    expected_showers = {
        "Lyrids": ("LYR", 0.810, 1.000, 0.895),
        "Eta_Aquariids": ("ETA", 0.904, 1.000, 0.950),
        "Southern_Delta_Aquariids": ("SDA", 0.856, 1.000, 0.922),
    }
    shower_checks: dict[str, Any] = {}
    for name, (code, precision, recall, f1) in expected_showers.items():
        item = recovery["untouched"][name]["score"]
        if item["shower"] != code or item["recovered"] is not True:
            raise AssertionError(f"Unexpected {name} recovery: {item}")
        shower_checks[name] = {
            "code": code,
            "true_count": item["true_count"],
            "precision": close(f"{name} precision", item["precision"], precision, 0.002),
            "recall": close(f"{name} recall", item["recall"], recall, 0.002),
            "f1": close(f"{name} F1", item["f1"], f1, 0.002),
        }

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

    evidence = {
        "status": "EXACT_RECOVERED_METHOD_CONTROLS",
        "source_repository": "brandonlign/remotion-worker",
        "source_commit": SOURCE_COMMIT,
        "known_shower_recovery": {
            "verdict": recovery["verdict"],
            "untouched_recovered": 3,
            "untouched_eligible": 3,
            "showers": shower_checks,
        },
        "weak_stream_injection": {
            "verdict": injection["verdict"],
            "permutations_per_run": injection["permutations_per_run"],
            "by_size": injection_checks,
        },
    }
    files = []
    for path in sorted(item for item in output.rglob("*") if item.is_file()):
        files.append({"path": path.relative_to(output).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    evidence["files"] = files
    (output / "method_controls.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# GhostStream recovered method controls",
        "",
        "**Verdict:** `EXACT_RECOVERED_METHOD_CONTROLS`",
        "",
        "The recovered control code was run from its immutable source commit before interpreting the blind-search result.",
        "",
        "- Untouched known showers recovered: **3/3**",
        "- Lyrids: precision 0.810, recall 1.000, F1 0.895",
        "- Eta Aquariids: precision 0.904, recall 1.000, F1 0.950",
        "- Southern Delta Aquariids: precision 0.856, recall 1.000, F1 0.922",
        "- 20-member injections: **4/9**, median F1 0.526",
        "- 40-member injections: **7/9**, median F1 0.800",
        "- 80-member injections: **8/9**, median F1 0.870",
        "",
    ]
    (output / "METHOD_CONTROLS.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
