"""Truth-free ranking and equal-capacity projection helpers."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Sequence

import pandas as pd

from .core import (
    CCFConfig,
    CCFScanner,
    CandidateResult,
    ScanResult,
    candidate_sort_key,
    cell_membership_family,
    normalize_frame,
)
from .nulls import PhasePermutationNull
from .stage0 import global_p_from_maxima


@dataclass(frozen=True)
class AnnualProjection:
    year: int
    capacity: int
    candidate_cells: tuple[tuple[int, ...], ...]
    member_ids: tuple[tuple[str, ...], ...]

    @property
    def returned_count(self) -> int:
        return len(self.candidate_cells)

    @property
    def capacity_satisfied(self) -> bool:
        return self.returned_count == self.capacity

    @property
    def fingerprint(self) -> str:
        payload = json.dumps(
            {
                "year": self.year,
                "capacity": self.capacity,
                "candidate_cells": self.candidate_cells,
                "member_ids": self.member_ids,
            },
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class FrozenTemporalHoldout:
    """One frozen discovery ranking projected into untouched years."""

    discovery_years: tuple[int, ...]
    holdout_years: tuple[int, ...]
    capacity: int
    ranked_cells: tuple[tuple[int, ...], ...]
    projections: tuple[AnnualProjection, ...]
    discovery_frame_sha256: str

    @property
    def capacity_satisfied(self) -> bool:
        return all(projection.capacity_satisfied for projection in self.projections)

    @property
    def underfilled_years(self) -> tuple[int, ...]:
        return tuple(
            projection.year for projection in self.projections if not projection.capacity_satisfied
        )

    @property
    def ranking_fingerprint(self) -> str:
        payload = json.dumps(
            {
                "discovery_years": self.discovery_years,
                "ranked_cells": self.ranked_cells,
            },
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


def assign_global_scores(
    candidates: Sequence[CandidateResult], calibration_maxima: Sequence[float],
) -> tuple[CandidateResult, ...]:
    """Attach complete-null catalogue scores before the final sort."""

    scored = [
        CandidateResult(
            cell=candidate.cell,
            heldout_p_values=candidate.heldout_p_values,
            heldout_statistics=candidate.heldout_statistics,
            recurrence_p=candidate.recurrence_p,
            represented_years=candidate.represented_years,
            p_global=global_p_from_maxima(candidate.score, calibration_maxima),
            alias_cells=candidate.alias_cells,
        )
        for candidate in candidates
    ]
    return tuple(sorted(scored, key=candidate_sort_key))


def ranked_catalogue(
    result: ScanResult,
    calibration_maxima: Sequence[float] | None = None,
) -> tuple[CandidateResult, ...]:
    """Return the selected local-max catalogue in its frozen global order."""

    selected = result.selected
    if calibration_maxima is None:
        return tuple(sorted(selected, key=candidate_sort_key))
    return assign_global_scores(selected, calibration_maxima)


def project_annual_catalogue(
    frame: pd.DataFrame,
    ranked_candidates: Sequence[CandidateResult],
    year: int,
    capacity: int,
    config: CCFConfig | None = None,
    *,
    strict_capacity: bool = True,
) -> AnnualProjection:
    """Project one global ranking into one annual capacity without reranking.

    ``strict_capacity=False`` records an underfilled projection instead of
    raising.  This is useful for fair holdout accounting: a method that cannot
    supply the predeclared capacity is measured as underfilled, not repaired by
    an annual rerank or an adaptive threshold.
    """

    if capacity < 1:
        raise ValueError("capacity must be positive")
    config = config or CCFConfig()
    normalized = normalize_frame(frame)
    annual = normalized.loc[normalized["year"] == int(year)].copy()
    if annual.empty:
        raise ValueError(f"no rows for projection year {year}")
    cells: list[tuple[int, ...]] = []
    members: list[tuple[str, ...]] = []
    for candidate in ranked_candidates:
        mask = cell_membership_family(annual, candidate.membership_cells, config)
        if not bool(mask.any()):
            continue
        cells.append(candidate.cell.as_tuple())
        members.append(tuple(sorted(annual.loc[mask, "event_id"].astype(str).tolist())))
        if len(cells) == capacity:
            break
    if strict_capacity and len(cells) < capacity:
        raise ValueError(f"capacity failure for year {year}: {len(cells)} eligible cells < {capacity}")
    return AnnualProjection(int(year), int(capacity), tuple(cells), tuple(members))


def run_frozen_temporal_holdout(
    frame: pd.DataFrame,
    discovery_years: Sequence[int],
    holdout_years: Sequence[int],
    capacity: int,
    *,
    scanner: CCFScanner | None = None,
    randomizations: int | None = None,
    calibration_maxima: Sequence[float] | None = None,
    config: CCFConfig | None = None,
) -> FrozenTemporalHoldout:
    """Fit and rank on discovery years, then project unchanged into holdouts.

    The holdout rows are not passed to candidate generation, null fitting, or
    ranking.  The returned projections preserve the single discovery ranking;
    under-capacity years are retained as explicit benchmark outcomes.
    """

    normalized = normalize_frame(frame)
    discovery = tuple(int(year) for year in discovery_years)
    holdout = tuple(int(year) for year in holdout_years)
    if not discovery or not holdout:
        raise ValueError("discovery_years and holdout_years must both be non-empty")
    if len(set(discovery)) != len(discovery) or len(set(holdout)) != len(holdout):
        raise ValueError("discovery_years and holdout_years must not contain duplicates")
    if set(discovery) & set(holdout):
        raise ValueError("discovery and holdout years must be disjoint")
    present_years = set(int(year) for year in normalized["year"].unique())
    missing = sorted((set(discovery) | set(holdout)) - present_years)
    if missing:
        raise ValueError(f"requested years are absent from the frame: {missing}")
    if len(discovery) < 3:
        raise ValueError("frozen temporal holdout requires at least three discovery years")
    if scanner is None:
        scanner = CCFScanner(config)
    if config is None:
        config = scanner.config
    elif scanner.config != config:
        raise ValueError("scanner and config must use the same frozen parameters")
    discovery_frame = normalized.loc[normalized["year"].isin(discovery)].reset_index(drop=True)
    discovery_null = PhasePermutationNull(
        discovery_frame,
        config,
        namespace="cc-cfrs-v1-frozen-temporal-holdout",
    )
    result = scanner.scan(discovery_frame, discovery_null, randomizations=randomizations)
    ranked = ranked_catalogue(result, calibration_maxima)
    projections = tuple(
        project_annual_catalogue(
            normalized,
            ranked,
            year,
            capacity,
            config,
            strict_capacity=False,
        )
        for year in holdout
    )
    payload = discovery_frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return FrozenTemporalHoldout(
        discovery_years=discovery,
        holdout_years=holdout,
        capacity=int(capacity),
        ranked_cells=tuple(candidate.cell.as_tuple() for candidate in ranked),
        projections=projections,
        discovery_frame_sha256=hashlib.sha256(payload).hexdigest(),
    )


def assert_same_information(left: pd.DataFrame, right: pd.DataFrame) -> None:
    """Fail closed unless two method inputs contain identical normalized rows."""

    left_normalized = normalize_frame(left)
    right_normalized = normalize_frame(right)
    if list(left_normalized.columns) != list(right_normalized.columns):
        raise ValueError("method inputs have different normalized columns")
    if left_normalized.shape != right_normalized.shape:
        raise ValueError("method inputs have different shapes")
    if not left_normalized.equals(right_normalized):
        raise ValueError("method inputs are not byte-equivalent after normalization")


__all__ = [
    "AnnualProjection",
    "FrozenTemporalHoldout",
    "assert_same_information",
    "assign_global_scores",
    "project_annual_catalogue",
    "ranked_catalogue",
    "run_frozen_temporal_holdout",
]
