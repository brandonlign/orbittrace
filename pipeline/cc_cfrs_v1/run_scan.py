"""Command-line entry point for one label-free CC-CFRS scan.

This runs the frozen scanner once on the supplied yearly source tables.  It
does not run the larger Stage 0 calibration/validation bank; use
``run_stage0`` for that separately guarded experiment.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from .adapters import SourceSpec, combine_years, load_csv
from .core import CCFConfig, CCFScanner
from .nulls import PhasePermutationNull


def _parse_inputs(values: list[str]) -> list[tuple[int, Path]]:
    parsed: list[tuple[int, Path]] = []
    for value in values:
        if "=" not in value:
            raise argparse.ArgumentTypeError(f"input must be YEAR=PATH: {value}")
        year_text, path_text = value.split("=", 1)
        try:
            year = int(year_text)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(f"invalid input year: {year_text}") from exc
        parsed.append((year, Path(path_text)))
    if len(parsed) < 3:
        raise argparse.ArgumentTypeError("at least three yearly inputs are required")
    years = [year for year, _ in parsed]
    if len(set(years)) != len(years):
        raise argparse.ArgumentTypeError("input years must be unique")
    return sorted(parsed)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one label-free CC-CFRS v1 scan")
    parser.add_argument("--source", required=True)
    parser.add_argument("--input", action="append", required=True, metavar="YEAR=CSV")
    parser.add_argument("--delimiter", default=",", help="CSV delimiter; use ';' for SonotaCo exports")
    parser.add_argument(
        "--randomizations",
        type=int,
        default=None,
        help="held-out null randomizations; default is the frozen production count of 999",
    )
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    return parser


def _candidate_report(candidate: object) -> dict[str, object]:
    return {
        "cell": candidate.cell.as_tuple(),
        "cell_sha256": candidate.cell.hash_hex(),
        "alias_cells": [cell.as_tuple() for cell in candidate.membership_cells],
        "heldout_p_values": candidate.heldout_p_values,
        "heldout_statistics": candidate.heldout_statistics,
        "recurrence_p": candidate.recurrence_p,
        "represented_years": candidate.represented_years,
        "score": candidate.score,
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    inputs = _parse_inputs(args.input)
    adapted = [
        load_csv(path, SourceSpec(args.source, year=year), sep=args.delimiter, low_memory=False)
        for year, path in inputs
    ]
    combined = combine_years(adapted)
    config = CCFConfig()
    scanner = CCFScanner(config)
    endpoint_hash = str(combined.manifest["frame_sha256"])
    null = PhasePermutationNull(
        combined.frame,
        config,
        namespace=f"{args.source}-scan",
        endpoint_hash=endpoint_hash,
    )
    result = scanner.scan(combined.frame, null, randomizations=args.randomizations)
    randomizations = config.heldout_randomizations if args.randomizations is None else int(args.randomizations)
    report = {
        "method": "cc-cfrs-v1",
        "source": args.source,
        "input_manifest": combined.manifest,
        "configuration": asdict(config),
        "randomizations": randomizations,
        "scan": {
            "candidate_count": len(result.candidates),
            "selected_count": len(result.selected),
            "max_statistic": result.max_statistic,
            "selected": [_candidate_report(candidate) for candidate in result.selected],
        },
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    if args.output is not None:
        args.output.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
