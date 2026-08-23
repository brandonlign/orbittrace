"""Report the complete 153-setting ACRF robustness grid."""
from __future__ import annotations
import argparse
from pathlib import Path
import json
from common import read_json, write_stage


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    summary = read_json("results/acrf_core_hyperparameter_robustness.json")
    provenance = read_json("data/derived/acrf_baseline_metadata.json")
    write_stage(args.out, "153_setting_acrf_core_hyperparameter_robustness", ["results/acrf_core_hyperparameter_robustness.json", "results/acrf_core_hyperparameter_robustness.csv", "configs/robustness_grid.json"], {"raw_design_cells": summary["raw_design_cells"], "unique_parameter_settings": summary["unique_parameter_settings"], "baseline_reproduced": summary["baseline_reproduced"], "exact_95_recovery_fraction": summary["exact_95_recovery_fraction"], "at_least_90_recovery_fraction": summary["at_least_90_recovery_fraction"], "at_least_80_recovery_fraction": summary["at_least_80_recovery_fraction"], "rank_le_100_fraction": summary["rank_le_100_fraction"], "baseline": {"rank": provenance["rank"], "reported_members": provenance["reported_members"], "target_overlap": provenance["target_overlap"]}})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
