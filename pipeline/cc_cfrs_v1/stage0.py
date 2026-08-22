"""Stage 0 calibration and finite-sample validation helpers."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable, Sequence

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Stage0Config:
    """The production Stage 0 bank contract."""

    calibration_replicates: int = 999
    validation_panels: int = 2000
    stratum_count: int = 4
    panels_per_stratum: int = 500
    alpha: float = 0.05
    overall_upper_bound: float = 0.060
    stratum_upper_bound: float = 0.075
    confidence: float = 0.95

    def __post_init__(self) -> None:
        if self.validation_panels != self.stratum_count * self.panels_per_stratum:
            raise ValueError("validation_panels must equal stratum_count * panels_per_stratum")
        if self.calibration_replicates != 999:
            raise ValueError("production calibration bank must contain exactly 999 replicates")
        if self.validation_panels != 2000:
            raise ValueError("production validation bank must contain exactly 2,000 panels")


@dataclass(frozen=True)
class Stage0GateResult:
    passed: bool
    overall_rejections: int
    overall_panels: int
    overall_upper_bound: float
    stratum_rejections: tuple[int, ...]
    stratum_panels: tuple[int, ...]
    stratum_upper_bounds: tuple[float, ...]


@dataclass(frozen=True)
class Stage0PipelineSummary:
    """The only statistic interface Stage 0 exposes to the bank runner."""

    max_statistic: float
    selected_statistics: tuple[float, ...]


@dataclass(frozen=True)
class Stage0RunResult:
    calibration_maxima: tuple[float, ...]
    validation_statistics: tuple[tuple[float, ...], ...]
    validation_rejections: tuple[bool, ...]
    validation_strata: tuple[int, ...]
    gate: Stage0GateResult


def _binomial_cdf(k: int, n: int, probability: float) -> float:
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    if probability <= 0.0:
        return 1.0
    if probability >= 1.0:
        return 0.0
    log_terms = []
    log_p = math.log(probability)
    log_q = math.log1p(-probability)
    for i in range(k + 1):
        log_terms.append(
            math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * log_p + (n - i) * log_q
        )
    maximum = max(log_terms)
    return float(math.exp(maximum) * sum(math.exp(term - maximum) for term in log_terms))


def clopper_pearson_upper(successes: int, trials: int, confidence: float = 0.95) -> float:
    """One-sided exact Clopper–Pearson upper confidence bound."""

    if trials <= 0 or successes < 0 or successes > trials:
        raise ValueError("invalid binomial counts")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between zero and one")
    if successes == trials:
        return 1.0
    target = 1.0 - confidence
    low, high = successes / trials, 1.0
    for _ in range(80):
        midpoint = (low + high) / 2.0
        if _binomial_cdf(successes, trials, midpoint) > target:
            low = midpoint
        else:
            high = midpoint
    return float(high)


def evaluate_stage0_gate(
    rejections: Sequence[bool | int],
    strata: Sequence[int],
    config: Stage0Config | None = None,
) -> Stage0GateResult:
    """Evaluate the predeclared panel-level Stage 0 rejection gate."""

    contract = config or Stage0Config()
    if len(rejections) != contract.validation_panels or len(strata) != contract.validation_panels:
        raise ValueError("Stage 0 requires exactly 2,000 validation panels")
    strata_array = np.asarray(strata, dtype=int)
    rejection_array = np.asarray(rejections, dtype=bool)
    if set(strata_array.tolist()) != set(range(contract.stratum_count)):
        raise ValueError("strata must be exactly the preregistered integer IDs")
    stratum_rejections: list[int] = []
    stratum_panels: list[int] = []
    stratum_bounds: list[float] = []
    for stratum in range(contract.stratum_count):
        mask = strata_array == stratum
        panels = int(mask.sum())
        if panels != contract.panels_per_stratum:
            raise ValueError("each Stage 0 stratum must contain exactly 500 panels")
        count = int(rejection_array[mask].sum())
        stratum_rejections.append(count)
        stratum_panels.append(panels)
        stratum_bounds.append(clopper_pearson_upper(count, panels, contract.confidence))
    overall_rejections = int(rejection_array.sum())
    overall_bound = clopper_pearson_upper(overall_rejections, contract.validation_panels, contract.confidence)
    passed = (
        overall_bound <= contract.overall_upper_bound
        and all(bound <= contract.stratum_upper_bound for bound in stratum_bounds)
    )
    return Stage0GateResult(
        passed=passed,
        overall_rejections=overall_rejections,
        overall_panels=contract.validation_panels,
        overall_upper_bound=overall_bound,
        stratum_rejections=tuple(stratum_rejections),
        stratum_panels=tuple(stratum_panels),
        stratum_upper_bounds=tuple(stratum_bounds),
    )


def global_p_from_maxima(statistic: float, calibration_maxima: Sequence[float]) -> float:
    """Convert a selected statistic to the complete-null catalogue score."""

    maxima = np.asarray(calibration_maxima, dtype=float)
    if maxima.size != 999 or not np.isfinite(maxima).all():
        raise ValueError("p_global requires exactly 999 finite calibration maxima")
    if not np.isfinite(statistic):
        raise ValueError("statistic must be finite")
    exceedances = int(np.sum(maxima >= statistic - 1e-15))
    return float((1 + exceedances) / (len(maxima) + 1))


def run_stage0(
    panel_factory: Callable[[str, int], tuple[pd.DataFrame, int]],
    pipeline: Callable[[pd.DataFrame, int], Stage0PipelineSummary],
    config: Stage0Config | None = None,
    progress: Callable[[str, int], None] | None = None,
) -> Stage0RunResult:
    """Run the exact Stage 0 calibration and validation bank.

    ``panel_factory(bank, index)`` must return an unlabeled panel and its
    predeclared integer stratum.  ``bank`` is either ``"calibration"`` or
    ``"validation"``.  The supplied pipeline must rerun the complete
    candidate-generation, held-out-scoring, recurrence, and local-maximum
    selection path from that panel.  This function intentionally does not
    provide a way to append panels or extend a bank after seeing results.
    """

    contract = config or Stage0Config()
    calibration_maxima: list[float] = []
    for index in range(contract.calibration_replicates):
        panel, stratum = panel_factory("calibration", index)
        if stratum not in range(contract.stratum_count):
            raise ValueError("calibration panel returned an invalid stratum")
        summary = pipeline(panel, index)
        if not np.isfinite(summary.max_statistic):
            raise ValueError("calibration pipeline returned a non-finite maximum")
        calibration_maxima.append(float(summary.max_statistic))
        if progress is not None and (
            index == 0 or (index + 1) % 25 == 0 or index + 1 == contract.calibration_replicates
        ):
            progress("calibration", index + 1)

    validation_statistics: list[tuple[float, ...]] = []
    validation_rejections: list[bool] = []
    validation_strata: list[int] = []
    for index in range(contract.validation_panels):
        panel, stratum = panel_factory("validation", index)
        if stratum not in range(contract.stratum_count):
            raise ValueError("validation panel returned an invalid stratum")
        summary = pipeline(panel, contract.calibration_replicates + index)
        statistics = tuple(float(statistic) for statistic in summary.selected_statistics)
        if any(not np.isfinite(statistic) for statistic in statistics):
            raise ValueError("validation pipeline returned a non-finite selected statistic")
        p_values = tuple(global_p_from_maxima(statistic, calibration_maxima) for statistic in statistics)
        rejected = any(p_value <= contract.alpha for p_value in p_values)
        validation_statistics.append(statistics)
        validation_rejections.append(rejected)
        validation_strata.append(int(stratum))
        if progress is not None and (index == 0 or (index + 1) % 25 == 0 or index + 1 == contract.validation_panels):
            progress("validation", index + 1)
    gate = evaluate_stage0_gate(validation_rejections, validation_strata, contract)
    return Stage0RunResult(
        calibration_maxima=tuple(calibration_maxima),
        validation_statistics=tuple(validation_statistics),
        validation_rejections=tuple(validation_rejections),
        validation_strata=tuple(validation_strata),
        gate=gate,
    )


__all__ = [
    "Stage0Config",
    "Stage0GateResult",
    "Stage0PipelineSummary",
    "Stage0RunResult",
    "clopper_pearson_upper",
    "evaluate_stage0_gate",
    "global_p_from_maxima",
    "run_stage0",
]
