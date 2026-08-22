"""Canonical-Cell Cross-Fitted Recurrent Scan, version 1.

This package is the new methodology study.  The historical OrbitTrace
pipeline remains unchanged; CC-CFRS is intentionally isolated under its own
versioned namespace.
"""

from .core import (
    CCFConfig,
    CCFScanner,
    CandidateResult,
    CanonicalCell,
    ScanResult,
    combine_recurrence_p,
    normalize_frame,
)
from .adapters import (
    AdapterResult,
    SourceSpec,
    adapt_frame,
    adapt_raw_frame,
    combine_years,
    load_csv,
    select_physical_columns,
)
from .nulls import PhasePermutationNull, derive_seed
from .evaluator import (
    AnnualProjection,
    FrozenTemporalHoldout,
    assert_same_information,
    assign_global_scores,
    project_annual_catalogue,
    ranked_catalogue,
    run_frozen_temporal_holdout,
)
from .stage0 import (
    Stage0Config,
    Stage0GateResult,
    Stage0PipelineSummary,
    Stage0RunResult,
    clopper_pearson_upper,
    evaluate_stage0_gate,
    global_p_from_maxima,
    run_stage0,
)

__all__ = [
    "CCFConfig",
    "CCFScanner",
    "AdapterResult",
    "AnnualProjection",
    "FrozenTemporalHoldout",
    "CandidateResult",
    "CanonicalCell",
    "ScanResult",
    "Stage0Config",
    "Stage0GateResult",
    "Stage0PipelineSummary",
    "Stage0RunResult",
    "SourceSpec",
    "PhasePermutationNull",
    "clopper_pearson_upper",
    "combine_recurrence_p",
    "adapt_frame",
    "adapt_raw_frame",
    "assert_same_information",
    "assign_global_scores",
    "combine_years",
    "derive_seed",
    "evaluate_stage0_gate",
    "global_p_from_maxima",
    "run_stage0",
    "normalize_frame",
    "load_csv",
    "project_annual_catalogue",
    "ranked_catalogue",
    "run_frozen_temporal_holdout",
    "select_physical_columns",
]
