"""Posthoc-only target reveal for a frozen v2 application artifact."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .application import _target_reveal


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frozen", type=Path, required=True)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    frozen_bytes = args.frozen.read_bytes()
    payload = json.loads(frozen_bytes.decode("utf-8"))
    years = tuple(int(value) for value in payload["years"])
    reveal = _target_reveal(payload["candidates"], args.target, years)
    result = {
        "stage": "unified_v2_posthoc_target_reveal",
        "frozen_artifact": str(args.frozen),
        "frozen_artifact_sha256": hashlib.sha256(frozen_bytes).hexdigest(),
        "target_accessed_after_frozen_ranking": True,
        "target_free_generation_artifact_unchanged": True,
        "reveal": reveal,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(args.out), "best": reveal["best"]}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
