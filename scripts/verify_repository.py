#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required = [
    ROOT / "README.md",
    ROOT / "RESULTS.md",
    ROOT / "candidate/CANDIDATE_DOSSIER.md",
    ROOT / "candidate/EXPERT_REVIEW_PACKET.md",
    ROOT / "candidate/mdc/MANUSCRIPT_DRAFT.md",
    ROOT / "candidate/mdc/GhostStream_April_95_GMN_lookup.csv",
    ROOT / "candidate/candidate_solution.json",
    ROOT / "results/ghoststream_final_summary.json",
    ROOT / "validation/exact_recovered/exact_reproduction.json",
    ROOT / "validation/exact_blind_rediscovery/blind_rediscovery.json",
    ROOT / "pipeline/pr57_novel/run_novel_search.py",
    ROOT / "pipeline/SOURCE_MANIFEST.json",
]

missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
if missing:
    raise SystemExit("Missing required files:\n- " + "\n- ".join(missing))

summary = json.loads((ROOT / "results/ghoststream_final_summary.json").read_text())
assert summary["pilot"] == "GhostStream"
assert summary["primary_result"]["confirmed_gmn_members"] == 95
assert summary["primary_result"]["hard_iau_matches"] == 0
assert summary["reproducibility_status"]["exact_primary_clean_rerun_completed"] is True

blind = json.loads((ROOT / "validation/exact_blind_rediscovery/blind_rediscovery.json").read_text())
assert blind["status"] == "EXACT_2026_BLIND_REDISCOVERY"
assert blind["full_gate_survivors_across_matrix"] == 1
assert blind["additional_non_april_survivors"] == []

manifest = json.loads((ROOT / "pipeline/SOURCE_MANIFEST.json").read_text())
assert manifest["sources"]["pr56_runner"]["file_count"] == 13
assert manifest["sources"]["pr57_novel"]["file_count"] == 35

for path in sorted((ROOT / "pipeline").rglob("*.py")) + sorted((ROOT / "scripts").rglob("*.py")):
    compile(path.read_text(encoding="utf-8"), str(path), "exec")

for obsolete in [ROOT / "pilots", ROOT / "recovery"]:
    assert not obsolete.exists(), f"Obsolete directory remains: {obsolete.name}"

junk_suffixes = (".tmp", ".bak", ".orig", ".rej", ".swp", "~")
for path in ROOT.rglob("*"):
    if path.is_dir() and path.name in {"__pycache__", ".pytest_cache", ".venv", "venv"}:
        raise AssertionError(f"Generated directory is tracked: {path.relative_to(ROOT)}")
    if path.is_file() and path.name.lower().endswith(junk_suffixes):
        raise AssertionError(f"Temporary file is tracked: {path.relative_to(ROOT)}")

# The public disclosure belongs in the top-level README and nowhere else in the repository prose.
terms = ("chat" + "gpt", "open" + "ai", "generative " + "ai", "ai" + "-assisted", "use of " + "ai")
for path in ROOT.rglob("*"):
    if not path.is_file() or path == ROOT / "README.md" or path.suffix.lower() not in {".md", ".txt", ".py", ".yml", ".yaml"}:
        continue
    lower = path.read_text(encoding="utf-8", errors="ignore").lower()
    hits = [term for term in terms if term in lower]
    if hits:
        raise AssertionError(f"Assistance disclosure appears outside README.md: {path.relative_to(ROOT)} ({hits})")

print("GhostStream repository check passed.")
print("The event counts, catalogue comparison, blind rediscovery, and source history are present and consistent.")
