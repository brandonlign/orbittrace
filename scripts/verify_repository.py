#!/usr/bin/env python3
"""Verify the final GhostStream repository structure, hygiene, and frozen result metadata."""

from __future__ import annotations

import compileall
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    ROOT / "RESULTS.md",
    ROOT / "requirements.txt",
    ROOT / "pipeline" / "SOURCE_MANIFEST.json",
    ROOT / "pipeline" / "pr57_novel" / "run_novel_search.py",
    ROOT / "pipeline" / "pr57_novel" / "validate_april_candidate.py",
    ROOT / "candidate" / "candidate_solution.json",
    ROOT / "candidate" / "mdc" / "GhostStream_April_95_GMN_lookup.csv",
    ROOT / "validation" / "exact_recovered" / "exact_reproduction.json",
    ROOT / "validation" / "exact_blind_rediscovery" / "blind_rediscovery.json",
    ROOT / "results" / "ghoststream_final_summary.json",
]

FORBIDDEN_TOP_LEVEL = {"pilots", "recovery"}
FORBIDDEN_PARTS = {"__pycache__", ".pytest_cache", ".venv", "venv", ".idea", ".vscode"}
FORBIDDEN_NAMES = {".DS_Store", ".coverage"}
FORBIDDEN_SUFFIXES = (".log", ".tmp", ".bak", ".orig", ".rej", ".swp", "~")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"Expected a JSON object: {path}")
    return value


def check_hygiene() -> None:
    present_top_level = {path.name for path in ROOT.iterdir()}
    forbidden = sorted(FORBIDDEN_TOP_LEVEL & present_top_level)
    if forbidden:
        raise SystemExit(f"Obsolete top-level directories remain: {forbidden}")

    junk: list[str] = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in FORBIDDEN_PARTS for part in relative.parts):
            junk.append(str(relative))
            continue
        if path.is_file() and (
            path.name in FORBIDDEN_NAMES or path.name.endswith(FORBIDDEN_SUFFIXES)
        ):
            junk.append(str(relative))
    if junk:
        raise SystemExit("Generated or temporary artifacts are tracked:\n- " + "\n- ".join(sorted(junk)))


def main() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.is_file()]
    if missing:
        raise SystemExit("Missing required files:\n- " + "\n- ".join(missing))

    candidate = load_json(ROOT / "candidate" / "candidate_solution.json")
    summary = load_json(ROOT / "results" / "ghoststream_final_summary.json")
    reproduction = load_json(
        ROOT / "validation" / "exact_recovered" / "exact_reproduction.json"
    )
    blind = load_json(
        ROOT / "validation" / "exact_blind_rediscovery" / "blind_rediscovery.json"
    )
    manifest = load_json(ROOT / "pipeline" / "SOURCE_MANIFEST.json")

    assert candidate["internal_id"] == "GhostStream-April-36.9"
    assert candidate["official_iau_designation"] is None
    assert summary["primary_result"]["confirmed_gmn_members"] == 95
    assert summary["primary_result"]["hard_iau_matches"] == 0
    assert reproduction["status"] == "EXACT_REPRODUCTION"
    assert blind["status"] == "EXACT_2026_BLIND_REDISCOVERY"
    assert blind["full_gate_survivors_across_matrix"] == 1
    assert manifest["sources"]["pr56_runner"]["file_count"] == 13
    assert manifest["sources"]["pr57_novel"]["file_count"] == 35

    check_hygiene()

    if not compileall.compile_dir(ROOT / "pipeline", quiet=1):
        raise SystemExit("Python compilation failed under pipeline/")

    print("GhostStream repository verification passed.")
    print("Repository hygiene: no generated or temporary artifacts tracked.")
    print("Scientific status: high-confidence candidate; independent review pending.")


if __name__ == "__main__":
    main()
