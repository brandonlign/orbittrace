"""Shared helpers for the paper-only frozen-result analyses."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def read_json(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_stage(out: Path, stage: str, inputs: list[str], headline: dict[str, Any]) -> dict[str, Any]:
    record = {
        "stage": stage,
        "inputs": {relative: sha256(ROOT / relative) for relative in inputs},
        "headline": headline,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    return record
