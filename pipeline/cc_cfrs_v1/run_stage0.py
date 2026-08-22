"""Command-line entry point for the exact CC-CFRS Stage 0 bank.

Example, after obtaining three local decoded source CSVs:

    python -m pipeline.cc_cfrs_v1.run_stage0 \
      --source SonotaCo \
      --input 2012=/data/S12.csv \
      --input 2013=/data/S13.csv \
      --input 2014=/data/S14.csv \
      --delimiter ';' \
      --confirm-expensive

The command prints a JSON report.  It never reads truth labels or target
identifiers because the source adapter drops those fields before normalization.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .adapters import SourceSpec, combine_years, load_csv
from .core import CCFConfig, CCFScanner
from .nulls import PhasePermutationNull
from .stage0 import Stage0PipelineSummary, run_stage0


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
    parser = argparse.ArgumentParser(description="Run the exact CC-CFRS v1 Stage 0 bank")
    parser.add_argument("--source", required=True)
    parser.add_argument("--input", action="append", required=True, metavar="YEAR=CSV")
    parser.add_argument("--delimiter", default=",", help="CSV delimiter; use ';' for SonotaCo exports")
    parser.add_argument("--confirm-expensive", action="store_true", help="authorize the exact 999 x 2,000 run")
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.confirm_expensive:
        raise SystemExit("refusing to start the exact Stage 0 bank without --confirm-expensive")
    inputs = _parse_inputs(args.input)
    adapted = [
        load_csv(path, SourceSpec(args.source, year=year), sep=args.delimiter, low_memory=False)
        for year, path in inputs
    ]
    combined = combine_years(adapted)
    config = CCFConfig()
    scanner = CCFScanner(config)
    endpoint_hash = str(combined.manifest["frame_sha256"])
    calibration_null = PhasePermutationNull(
        combined.frame,
        config,
        namespace=f"{args.source}-stage0-calibration",
        endpoint_hash=endpoint_hash,
    )
    validation_null = PhasePermutationNull(
        combined.frame,
        config,
        namespace=f"{args.source}-stage0-validation",
        endpoint_hash=endpoint_hash,
    )

    def panel_factory(bank: str, index: int) -> tuple[pd.DataFrame, int]:
        if bank == "calibration":
            return calibration_null(index), index % 4
        return validation_null(index), index // 500

    def pipeline(panel: pd.DataFrame, seed: int) -> Stage0PipelineSummary:
        heldout_null = PhasePermutationNull(panel, config, namespace=f"{args.source}-heldout-{seed}")
        result = scanner.scan(panel, heldout_null, randomizations=config.heldout_randomizations)
        return Stage0PipelineSummary(result.max_statistic, result.selected_statistics)

    def progress(bank: str, count: int) -> None:
        print(f"{bank}: {count}", flush=True)

    stage0 = run_stage0(panel_factory, pipeline, progress=progress)
    report = {
        "method": "cc-cfrs-v1",
        "source": args.source,
        "input_manifest": combined.manifest,
        "null_endpoint_hash": endpoint_hash,
        "stage0": {
            "calibration_replicates": len(stage0.calibration_maxima),
            "validation_panels": len(stage0.validation_rejections),
            "gate": {
                "passed": stage0.gate.passed,
                "overall_rejections": stage0.gate.overall_rejections,
                "overall_upper_bound": stage0.gate.overall_upper_bound,
                "stratum_rejections": stage0.gate.stratum_rejections,
                "stratum_upper_bounds": stage0.gate.stratum_upper_bounds,
            },
        },
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    if args.output is not None:
        args.output.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
