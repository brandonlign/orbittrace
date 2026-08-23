"""Generate Figures 1--3 from the versioned plotted data tables."""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for number in (1, 2, 3):
        subprocess.run([sys.executable, f"figures/figure_{number}.py", "--out", str(args.out / f"figure_{number}.png")], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
