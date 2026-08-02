#!/usr/bin/env python3
from __future__ import annotations

import json
import re
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

# Keep the public assistance note in the top-level README only.
parts = {
    "assistant_name": "chat" + "gpt",
    "company_name": "open" + "ai",
    "short_term": "a" + "i",
    "generated_term": "generative " + "a" + "i",
    "assisted_term": "a" + "i" + "-assisted",
    "full_term": "artificial " + "intelligence",
    "model_term": "large language " + "model",
    "abbreviation": "l" + "lm",
    "model_family": "g" + "pt",
}
patterns = [
    re.compile(rf"\b{re.escape(parts['assistant_name'])}\b", re.IGNORECASE),
    re.compile(rf"\b{re.escape(parts['company_name'])}\b", re.IGNORECASE),
    re.compile(rf"\b{re.escape(parts['short_term'])}\b", re.IGNORECASE),
    re.compile(rf"\b{re.escape(parts['generated_term'])}\b", re.IGNORECASE),
    re.compile(rf"\b{re.escape(parts['assisted_term'])}\b", re.IGNORECASE),
    re.compile(rf"\b{re.escape(parts['full_term'])}\b", re.IGNORECASE),
    re.compile(rf"\b{re.escape(parts['model_term'])}s?\b", re.IGNORECASE),
    re.compile(rf"\b{re.escape(parts['abbreviation'])}s?\b", re.IGNORECASE),
    re.compile(rf"\b{re.escape(parts['model_family'])}(?:-?\d[\w.-]*)?\b", re.IGNORECASE),
]

text_suffixes = {
    ".md", ".txt", ".py", ".yml", ".yaml", ".json", ".csv", ".toml", ".ini", ".cfg"
}
checker = Path(__file__).resolve()
for path in ROOT.rglob("*"):
    if not path.is_file() or path == ROOT / "README.md" or path.resolve() == checker:
        continue
    if path.suffix.lower() not in text_suffixes:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    hits = sorted({match.group(0) for pattern in patterns for match in pattern.finditer(text)})
    if hits:
        raise AssertionError(
            f"Assistance wording appears outside README.md: {path.relative_to(ROOT)} ({hits})"
        )

for path in ROOT.rglob("*"):
    if path == ROOT / "README.md":
        continue
    normalized_name = re.sub(r"[^a-z0-9]+", " ", path.name.lower()).strip()
    if any(pattern.search(normalized_name) for pattern in patterns):
        raise AssertionError(f"Assistance-related filename appears outside README.md: {path.relative_to(ROOT)}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert any(pattern.search(readme) for pattern in patterns), "README assistance note is missing"

print("GhostStream repository check passed.")
print("Event counts, catalogue comparison, blind rediscovery, source history, and README-only assistance wording are consistent.")
