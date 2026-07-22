#!/usr/bin/env python3
"""Validate runtime, import dependencies, and record reproducibility metadata."""
from pathlib import Path
import importlib.metadata as md
import json, platform, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from reconnectid.config import ensure_directories

ensure_directories(ROOT)
required = ["numpy","scipy","pandas","scikit-learn","matplotlib","pyspedas","pytplot","cdflib","requests","pyyaml","joblib","pyarrow","pytest"]
versions, missing = {}, []
for package in required:
    try: versions[package] = md.version(package)
    except md.PackageNotFoundError: missing.append(package)
try: commit = subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True,check=False).stdout.strip() or "not-a-git-checkout"
except OSError: commit = "git-unavailable"
info = {"python":sys.version,"platform":platform.platform(),"packages":versions,"git_commit":commit,"missing":missing}
(ROOT/"results/logs/environment.json").write_text(json.dumps(info,indent=2))
print(json.dumps(info,indent=2))
if sys.version_info[:2] != (3,11): print("WARNING: the reproducibility target is Python 3.11",file=sys.stderr)
if missing: raise SystemExit(f"Missing required packages: {', '.join(missing)}")

