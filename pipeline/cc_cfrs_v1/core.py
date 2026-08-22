"""Core implementation of the Canonical-Cell Cross-Fitted Recurrent Scan.

The implementation deliberately keeps the scientific primitives explicit:

* a fixed physical representation and three coupled scales;
* one stabilized cell-family identity shared by every leave-one-year-out fold;
* deterministic anchor fitting and membership;
* held-out empirical p-values and a two-of-three partial conjunction; and
* fixed physical adjacency for duplicate suppression.

The module does not know OrbitTrace target IDs, coordinates, membership, or
truth labels.  Adapters are responsible for converting an unlabeled source
catalogue into the required columns documented in ``README.md``.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import itertools
import json
import math
from typing import Callable, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = (
    "event_id",
    "year",
    "sol_lon_deg",
    "radiant_lon_deg",
    "radiant_lat_deg",
    "speed_km_s",
)
MEMBERSHIP_BATCH_SIZE = 64


def wrap_deg(value: np.ndarray | float) -> np.ndarray | float:
    """Wrap degrees into [0, 360), using one deterministic convention."""

    wrapped = np.mod(np.asarray(value, dtype=float), 360.0)
    if np.ndim(value) == 0:
        return float(wrapped)
    return wrapped


def circ_diff(value: np.ndarray | float, center: np.ndarray | float) -> np.ndarray | float:
    """Return the signed circular difference in [-180, 180)."""

    diff = (np.asarray(value, dtype=float) - np.asarray(center, dtype=float) + 180.0) % 360.0 - 180.0
    if np.ndim(diff) == 0:
        return float(diff)
    return diff


def radiant_z(latitude_deg: np.ndarray | float) -> np.ndarray | float:
    z = np.sin(np.deg2rad(np.asarray(latitude_deg, dtype=float)))
    if np.ndim(z) == 0:
        return float(z)
    return z


@dataclass(frozen=True)
class CCFConfig:
    """Pre-truth scientific parameters for CC-CFRS v1.

    The default values are the frozen exploratory contract for this lane. Tests
    may use a smaller scale tuple or randomization count, but such
    configurations are explicitly non-production and cannot be used for a
    benchmark claim.
    """

    base_sol_half_width_deg: float = 5.0
    base_radiant_half_width_deg: float = 4.0
    base_speed_fraction: float = 0.10
    scales: tuple[float, ...] = (0.5, 1.0, 2.0)
    minimum_training_members: int = 4
    minimum_represented_years: int = 2
    minimum_anchor_bin_members: int = 16
    candidate_anchor_quota: int = 4
    candidate_peak_quota: int = 2
    proposal_alias_block: int = 2
    maximum_fit_members: int = 64
    robust_iterations: int = 5
    huber_delta: float = 1.5
    max_drift_lon_deg_per_deg: float = 2.0
    max_drift_z_per_deg: float = 0.20
    max_drift_log_speed_per_deg: float = 0.02
    minimum_speed_km_s: float = 5.0
    maximum_speed_km_s: float = 100.0
    heldout_randomizations: int = 999
    exclude_sol_low_deg: float = 20.0
    exclude_sol_high_deg: float = 55.0
    null_radiant_lon_bin_deg: float = 120.0
    null_z_bin_width: float = 1.0
    null_speed_edges_km_s: tuple[float, ...] = (5.0, 25.0, 45.0, 65.0, 101.0)

    def __post_init__(self) -> None:
        if not self.scales:
            raise ValueError("at least one scale is required")
        if any(scale <= 0 for scale in self.scales):
            raise ValueError("scales must be positive")
        if self.minimum_training_members < 2:
            raise ValueError("minimum_training_members must be at least 2")
        if self.minimum_represented_years < 2:
            raise ValueError("minimum_represented_years must be at least 2")
        if self.minimum_anchor_bin_members < self.minimum_training_members:
            raise ValueError("minimum_anchor_bin_members must cover minimum_training_members")
        if self.candidate_anchor_quota < 1:
            raise ValueError("candidate_anchor_quota must be positive")
        if self.candidate_peak_quota < 1:
            raise ValueError("candidate_peak_quota must be positive")
        if self.proposal_alias_block < 1:
            raise ValueError("proposal_alias_block must be positive")
        if self.maximum_fit_members < self.minimum_training_members:
            raise ValueError("maximum_fit_members must cover minimum_training_members")
        if self.minimum_speed_km_s <= 0 or self.maximum_speed_km_s <= self.minimum_speed_km_s:
            raise ValueError("speed bounds are invalid")
        if self.heldout_randomizations < 1:
            raise ValueError("heldout_randomizations must be positive")
        if self.null_radiant_lon_bin_deg <= 0 or self.null_z_bin_width <= 0:
            raise ValueError("null source bins must be positive")
        if len(self.null_speed_edges_km_s) < 2 or any(
            right <= left for left, right in zip(self.null_speed_edges_km_s, self.null_speed_edges_km_s[1:])
        ):
            raise ValueError("null speed edges must be strictly increasing")
        if self.null_speed_edges_km_s[0] > self.minimum_speed_km_s:
            raise ValueError("null speed edges must start at or below the minimum speed")
        if self.null_speed_edges_km_s[-1] <= self.maximum_speed_km_s:
            raise ValueError("null speed edges must extend above the maximum speed")


@dataclass(frozen=True, order=True)
class CanonicalCell:
    """The exact global identity used across every fold."""

    scale_index: int
    q_sol: int
    q_lon: int
    q_z: int
    q_speed: int
    q_dlon: int
    q_dz: int
    q_dlog_speed: int

    def as_tuple(self) -> tuple[int, ...]:
        return (
            self.scale_index,
            self.q_sol,
            self.q_lon,
            self.q_z,
            self.q_speed,
            self.q_dlon,
            self.q_dz,
            self.q_dlog_speed,
        )

    def hash_hex(self) -> str:
        payload = json.dumps(self.as_tuple(), separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class CandidateResult:
    cell: CanonicalCell
    heldout_p_values: tuple[float, ...]
    heldout_statistics: tuple[float, ...]
    recurrence_p: float
    represented_years: int
    p_global: float | None = None
    alias_cells: tuple[CanonicalCell, ...] = ()

    @property
    def membership_cells(self) -> tuple[CanonicalCell, ...]:
        return self.alias_cells or (self.cell,)

    @property
    def score(self) -> float:
        return -math.log10(max(self.recurrence_p, np.finfo(float).tiny))

    @property
    def second_strongest_log_evidence(self) -> float:
        values = sorted((-math.log10(max(p, np.finfo(float).tiny)) for p in self.heldout_p_values), reverse=True)
        return float(values[1] if len(values) > 1 else 0.0)


@dataclass(frozen=True)
class ScanResult:
    candidates: tuple[CandidateResult, ...]
    selected: tuple[CandidateResult, ...]

    @property
    def max_statistic(self) -> float:
        return max((candidate.score for candidate in self.selected), default=0.0)

    @property
    def selected_statistics(self) -> tuple[float, ...]:
        return tuple(candidate.score for candidate in self.selected)


def normalize_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate and deterministically order an unlabeled event table.

    Invalid physical rows fail closed by being removed.  The adapter or
    caller should record the number removed in its provenance manifest.
    """

    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    out = frame.loc[:, list(REQUIRED_COLUMNS)].copy()
    out["event_id"] = out["event_id"].astype(str)
    if out["event_id"].duplicated().any():
        raise ValueError("event_id values must be unique")
    for column in REQUIRED_COLUMNS[1:]:
        out[column] = pd.to_numeric(out[column], errors="coerce")
    valid = out[list(REQUIRED_COLUMNS[1:])].notna().all(axis=1)
    valid &= out["speed_km_s"] > 0
    valid &= out["radiant_lat_deg"].between(-90.0, 90.0)
    if not valid.all():
        out = out.loc[valid].copy()
    if out.empty:
        raise ValueError("no valid physical rows remain")
    out["year"] = out["year"].astype(int)
    return out.sort_values(["year", "event_id"], kind="mergesort").reset_index(drop=True)


def combine_recurrence_p(p_values: Mapping[int, float] | Sequence[float]) -> float:
    """Bonferroni partial-conjunction p for activity in at least two years."""

    values = np.asarray(list(p_values.values()) if isinstance(p_values, Mapping) else list(p_values), dtype=float)
    if values.size < 3:
        raise ValueError("CC-CFRS recurrence requires at least three years")
    if not np.isfinite(values).all() or (values < 0).any() or (values > 1).any():
        raise ValueError("p-values must lie in [0, 1]")
    second_smallest = float(np.sort(values)[1])
    return min(1.0, float((values.size - 1) * second_smallest))


def _huber_fit(x: np.ndarray, y: np.ndarray, config: CCFConfig) -> tuple[float, float]:
    if x.size < 2 or np.ptp(x) <= np.finfo(float).eps:
        return float(np.mean(y)), 0.0
    design = np.column_stack((np.ones(x.size), x))
    weights = np.ones(x.size, dtype=float)
    coefficients = np.zeros(2, dtype=float)
    for _ in range(config.robust_iterations):
        weighted_design = design * weights[:, None]
        weighted_y = y * weights
        coefficients, *_ = np.linalg.lstsq(weighted_design, weighted_y, rcond=None)
        residual = y - design @ coefficients
        scale = float(np.median(np.abs(residual - np.median(residual)))) * 1.4826
        scale = max(scale, 1e-9)
        standardized = np.abs(residual) / (config.huber_delta * scale)
        weights = np.ones_like(standardized)
        outlier = standardized > 1.0
        weights[outlier] = 1.0 / standardized[outlier]
    return float(coefficients[0]), float(coefficients[1])


def _scale_widths(scale: float, config: CCFConfig) -> dict[str, float]:
    sol_full = 2.0 * config.base_sol_half_width_deg * scale
    radiant_full = 2.0 * config.base_radiant_half_width_deg * scale
    sol_cell = sol_full / 4.0
    lon_cell = radiant_full / 4.0
    z_cell = 2.0 * math.sin(math.radians(radiant_full / 2.0)) / 4.0
    speed_log_full = math.log((1.0 + config.base_speed_fraction * scale) / (1.0 - config.base_speed_fraction * scale))
    speed_log_cell = speed_log_full / 4.0
    return {
        "sol_half": config.base_sol_half_width_deg * scale,
        "radiant_half": config.base_radiant_half_width_deg * scale,
        "speed_log_half": speed_log_full / 2.0,
        "sol_cell": sol_cell,
        "lon_cell": lon_cell,
        "z_cell": z_cell,
        "speed_log_cell": speed_log_cell,
        "drift_lon_cell": lon_cell / config.base_sol_half_width_deg,
        "drift_z_cell": z_cell / config.base_sol_half_width_deg,
        "drift_log_speed_cell": speed_log_cell / config.base_sol_half_width_deg,
    }


def _quantize(value: float, origin: float, width: float) -> int:
    return int(math.floor((value - origin) / width))


def _canonicalize(
    scale_index: int,
    sol: float,
    lon: float,
    z: float,
    log_speed: float,
    dlon: float,
    dz: float,
    dlog_speed: float,
    config: CCFConfig,
) -> CanonicalCell | None:
    scale = config.scales[scale_index]
    widths = _scale_widths(scale, config)
    if not (-config.max_drift_lon_deg_per_deg <= dlon <= config.max_drift_lon_deg_per_deg):
        return None
    if not (-config.max_drift_z_per_deg <= dz <= config.max_drift_z_per_deg):
        return None
    if not (-config.max_drift_log_speed_per_deg <= dlog_speed <= config.max_drift_log_speed_per_deg):
        return None
    q_sol = _quantize(float(wrap_deg(sol)), 0.0, widths["sol_cell"])
    q_lon = _quantize(float(wrap_deg(lon)), 0.0, widths["lon_cell"])
    q_z = _quantize(float(np.clip(z, -1.0, 1.0)), -1.0, widths["z_cell"])
    log_min = math.log(config.minimum_speed_km_s)
    q_speed = _quantize(log_speed, log_min, widths["speed_log_cell"])
    q_dlon = _quantize(dlon, -config.max_drift_lon_deg_per_deg, widths["drift_lon_cell"])
    q_dz = _quantize(dz, -config.max_drift_z_per_deg, widths["drift_z_cell"])
    q_dlog = _quantize(dlog_speed, -config.max_drift_log_speed_per_deg, widths["drift_log_speed_cell"])
    return CanonicalCell(scale_index, q_sol, q_lon, q_z, q_speed, q_dlon, q_dz, q_dlog)


def cell_geometry(cell: CanonicalCell, config: CCFConfig) -> dict[str, float]:
    """Decode a canonical cell using fixed half-open lattice conventions."""

    scale = config.scales[cell.scale_index]
    widths = _scale_widths(scale, config)
    sol = (cell.q_sol + 0.5) * widths["sol_cell"] % 360.0
    lon = (cell.q_lon + 0.5) * widths["lon_cell"] % 360.0
    z = np.clip(-1.0 + (cell.q_z + 0.5) * widths["z_cell"], -1.0, 1.0)
    log_speed = math.log(config.minimum_speed_km_s) + (cell.q_speed + 0.5) * widths["speed_log_cell"]
    dlon = -config.max_drift_lon_deg_per_deg + (cell.q_dlon + 0.5) * widths["drift_lon_cell"]
    dz = -config.max_drift_z_per_deg + (cell.q_dz + 0.5) * widths["drift_z_cell"]
    dlog = -config.max_drift_log_speed_per_deg + (cell.q_dlog_speed + 0.5) * widths["drift_log_speed_cell"]
    return {
        "sol": sol,
        "lon": lon,
        "lat": math.degrees(math.asin(float(z))),
        "z": float(z),
        "log_speed": log_speed,
        "speed": math.exp(log_speed),
        "dlon": dlon,
        "dz": dz,
        "dlog_speed": dlog,
        "sol_half": widths["sol_half"],
        "radiant_half": widths["radiant_half"],
        "speed_log_half": widths["speed_log_half"],
    }


def _radiant_distance_deg(
    lon_a: np.ndarray,
    lat_a: np.ndarray,
    lon_b: np.ndarray | float,
    lat_b: np.ndarray | float,
) -> np.ndarray:
    a_lon = np.deg2rad(lon_a)
    a_lat = np.deg2rad(lat_a)
    b_lon = np.deg2rad(np.asarray(lon_b, dtype=float))
    b_lat = np.deg2rad(np.asarray(lat_b, dtype=float))
    cosine = np.sin(a_lat) * np.sin(b_lat) + np.cos(a_lat) * np.cos(b_lat) * np.cos(a_lon - b_lon)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))


def _frame_feature_arrays(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return (
        frame["sol_lon_deg"].to_numpy(float),
        frame["radiant_lon_deg"].to_numpy(float),
        frame["radiant_lat_deg"].to_numpy(float),
        np.log(frame["speed_km_s"].to_numpy(float)),
    )


def _year_feature_arrays(
    frame: pd.DataFrame,
) -> dict[int, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    years = frame["year"].to_numpy(int)
    output: dict[int, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = {}
    for year in sorted(set(int(value) for value in years)):
        mask = years == year
        output[year] = _frame_feature_arrays(frame.loc[mask])
    return output


def _membership_arrays(
    features: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    cell: CanonicalCell,
    config: CCFConfig,
) -> np.ndarray:
    geometry = cell_geometry(cell, config)
    sol, lon, lat, log_speed = features
    z = radiant_z(lat)
    x = circ_diff(sol, geometry["sol"])
    predicted_lon = wrap_deg(geometry["lon"] + geometry["dlon"] * x)
    predicted_z = np.clip(geometry["z"] + geometry["dz"] * x, -1.0, 1.0)
    predicted_lat = np.degrees(np.arcsin(predicted_z))
    predicted_log_speed = geometry["log_speed"] + geometry["dlog_speed"] * x
    radiant_distance = _radiant_distance_deg(lon, lat, predicted_lon, predicted_lat)
    return (
        (np.abs(x) <= geometry["sol_half"])
        & (radiant_distance <= geometry["radiant_half"])
        & (np.abs(log_speed - predicted_log_speed) <= geometry["speed_log_half"])
    )


def cell_membership(frame: pd.DataFrame, cell: CanonicalCell, config: CCFConfig) -> np.ndarray:
    """Return a deterministic boolean membership mask for one cell."""

    return _membership_arrays(_frame_feature_arrays(frame), cell, config)


def cell_membership_family(
    frame: pd.DataFrame,
    cells: Sequence[CanonicalCell],
    config: CCFConfig,
) -> np.ndarray:
    """Return the union membership of a predeclared fold-stable cell family."""

    if not cells:
        return np.zeros(len(frame), dtype=bool)
    features = _frame_feature_arrays(frame)
    membership = np.zeros(len(frame), dtype=bool)
    for cell in cells:
        membership |= _membership_arrays(features, cell, config)
    return membership


def _fit_anchor(frame: pd.DataFrame, anchor_index: int, scale_index: int, config: CCFConfig) -> CanonicalCell | None:
    return _fit_anchor_subset(frame, anchor_index, scale_index, config, None)


def _fit_anchor_subset(
    frame: pd.DataFrame,
    anchor_index: int,
    scale_index: int,
    config: CCFConfig,
    candidate_indices: np.ndarray | None,
) -> CanonicalCell | None:
    scale = config.scales[scale_index]
    widths = _scale_widths(scale, config)
    all_sol = frame["sol_lon_deg"].to_numpy(float)
    all_lon = frame["radiant_lon_deg"].to_numpy(float)
    all_lat = frame["radiant_lat_deg"].to_numpy(float)
    all_z = np.asarray(radiant_z(all_lat), dtype=float)
    all_log_speed = np.log(frame["speed_km_s"].to_numpy(float))
    indices = (
        np.arange(len(frame), dtype=int)
        if candidate_indices is None
        else np.asarray(candidate_indices, dtype=int)
    )
    if not np.isin(anchor_index, indices):
        indices = np.unique(np.concatenate((indices, np.asarray([anchor_index], dtype=int))))
    if indices.size > config.maximum_fit_members:
        anchor_sol = float(all_sol[anchor_index])
        anchor_lon = float(all_lon[anchor_index])
        anchor_lat = float(all_lat[anchor_index])
        anchor_log_speed = float(all_log_speed[anchor_index])
        distance = (
            (np.asarray(circ_diff(all_sol[indices], anchor_sol), dtype=float) / widths["sol_half"]) ** 2
            + (
                _radiant_distance_deg(
                    all_lon[indices],
                    all_lat[indices],
                    anchor_lon,
                    anchor_lat,
                )
                / widths["radiant_half"]
            ) ** 2
            + ((all_log_speed[indices] - anchor_log_speed) / widths["speed_log_half"]) ** 2
        )
        order = np.lexsort((frame["event_id"].to_numpy()[indices], distance))
        selected = indices[order[: config.maximum_fit_members]]
        if not np.isin(anchor_index, selected):
            selected[-1] = anchor_index
        indices = selected
    sol = all_sol[indices]
    lon = all_lon[indices]
    lat = all_lat[indices]
    z = all_z[indices]
    log_speed = all_log_speed[indices]
    anchor_local = int(np.flatnonzero(indices == anchor_index)[0])
    anchor_sol = float(sol[anchor_local])
    anchor_lon = float(lon[anchor_local])
    anchor_lat = float(lat[anchor_local])
    anchor_log_speed = float(log_speed[anchor_local])
    x = np.asarray(circ_diff(sol, anchor_sol), dtype=float)
    initial_radiant = _radiant_distance_deg(lon, lat, anchor_lon, anchor_lat)
    initial_mask = (
        (np.abs(x) <= widths["sol_half"])
        & (initial_radiant <= widths["radiant_half"])
        & (np.abs(log_speed - anchor_log_speed) <= widths["speed_log_half"])
    )
    if int(initial_mask.sum()) < config.minimum_training_members:
        return None
    intercept_lon, drift_lon = _huber_fit(x[initial_mask], np.asarray(circ_diff(lon[initial_mask], anchor_lon)), config)
    intercept_z, drift_z = _huber_fit(x[initial_mask], z[initial_mask], config)
    intercept_log_speed, drift_log_speed = _huber_fit(x[initial_mask], log_speed[initial_mask], config)
    return _canonicalize(
        scale_index,
        anchor_sol,
        float(wrap_deg(anchor_lon + intercept_lon)),
        intercept_z,
        intercept_log_speed,
        drift_lon,
        drift_z,
        drift_log_speed,
        config,
    )


def _coarse_key(
    sol: float,
    lon: float,
    z: float,
    log_speed: float,
    scale_index: int,
    config: CCFConfig,
) -> tuple[int, int, int, int]:
    """Return a deterministic coarse zero-drift bin for anchor grouping."""

    scale = config.scales[scale_index]
    widths = _scale_widths(scale, config)
    sol_width = 2.0 * widths["sol_half"]
    lon_width = 2.0 * widths["radiant_half"]
    z_width = 2.0 * math.sin(math.radians(widths["radiant_half"]))
    speed_width = 2.0 * widths["speed_log_half"]
    sol_bins = max(1, int(round(360.0 / sol_width)))
    lon_bins = max(1, int(round(360.0 / lon_width)))
    q_sol = int(math.floor(float(wrap_deg(sol)) / sol_width)) % sol_bins
    q_lon = int(math.floor(float(wrap_deg(lon)) / lon_width)) % lon_bins
    q_z = int(math.floor((float(np.clip(z, -1.0, 1.0)) + 1.0) / z_width))
    q_speed = int(math.floor((log_speed - math.log(config.minimum_speed_km_s)) / speed_width))
    return q_sol, q_lon, q_z, q_speed


def _density_key(
    sol: float,
    lon: float,
    z: float,
    log_speed: float,
    scale_index: int,
    config: CCFConfig,
) -> tuple[int, int, int, int]:
    """Return the quarter-window bin used to identify compact anchor cores."""

    widths = _scale_widths(config.scales[scale_index], config)
    sol_width = widths["sol_half"] / 2.0
    lon_width = widths["radiant_half"] / 2.0
    z_width = math.sin(math.radians(widths["radiant_half"])) / 2.0
    speed_width = widths["speed_log_half"] / 2.0
    sol_bins = max(1, int(round(360.0 / sol_width)))
    lon_bins = max(1, int(round(360.0 / lon_width)))
    return (
        int(math.floor(float(wrap_deg(sol)) / sol_width)) % sol_bins,
        int(math.floor(float(wrap_deg(lon)) / lon_width)) % lon_bins,
        int(math.floor((float(np.clip(z, -1.0, 1.0)) + 1.0) / z_width)),
        int(math.floor((log_speed - math.log(config.minimum_speed_km_s)) / speed_width)),
    )


def _anchor_groups(frame: pd.DataFrame, scale_index: int, config: CCFConfig) -> list[tuple[int, np.ndarray]]:
    """Build occupied groups and retain the densest local anchors."""

    event_ids = frame["event_id"].astype(str).to_numpy()
    sol = frame["sol_lon_deg"].to_numpy(float)
    lon = frame["radiant_lon_deg"].to_numpy(float)
    z = np.asarray(radiant_z(frame["radiant_lat_deg"].to_numpy(float)), dtype=float)
    log_speed = np.log(frame["speed_km_s"].to_numpy(float))
    years = frame["year"].to_numpy(int)
    groups: dict[tuple[int, int, int, int], list[int]] = {}
    group_year_counts: dict[tuple[int, int, int, int], dict[int, int]] = {}
    density_groups: dict[tuple[int, int, int, int], list[int]] = {}
    density_year_counts: dict[tuple[int, int, int, int], dict[int, int]] = {}
    coarse_to_density: dict[tuple[int, int, int, int], set[tuple[int, int, int, int]]] = {}
    coarse_keys: list[tuple[int, int, int, int]] = []
    density_keys: list[tuple[int, int, int, int]] = []
    for index in range(len(frame)):
        key = _coarse_key(sol[index], lon[index], z[index], log_speed[index], scale_index, config)
        density_key = _density_key(sol[index], lon[index], z[index], log_speed[index], scale_index, config)
        coarse_keys.append(key)
        density_keys.append(density_key)
        groups.setdefault(key, []).append(index)
        year_counts = group_year_counts.setdefault(key, {})
        year_counts[int(years[index])] = year_counts.get(int(years[index]), 0) + 1
        density_groups.setdefault(density_key, []).append(index)
        density_counts_for_key = density_year_counts.setdefault(density_key, {})
        density_counts_for_key[int(years[index])] = density_counts_for_key.get(int(years[index]), 0) + 1
        coarse_to_density.setdefault(key, set()).add(density_key)
    if not groups:
        return []
    scale = config.scales[scale_index]
    widths = _scale_widths(scale, config)
    sol_bins = max(1, int(round(360.0 / (2.0 * widths["sol_half"]))))
    lon_bins = max(1, int(round(360.0 / (2.0 * widths["radiant_half"]))))
    offsets = tuple(itertools.product((-1, 0, 1), repeat=4))
    density_counts = np.asarray([len(density_groups[key]) for key in density_keys], dtype=int)
    density_scores = {
        key: (
            len(year_counts),
            sum(min(count, config.minimum_anchor_bin_members) for count in year_counts.values()),
            sum(math.log1p(count) for count in year_counts.values()),
        )
        for key, year_counts in density_year_counts.items()
    }
    dominant_density = {
        key: max(
            density_keys_for_group,
            key=lambda value: (
                density_scores[value][0],
                density_scores[value][1],
                density_scores[value][2],
                tuple(-component for component in value),
            ),
        )
        for key, density_keys_for_group in coarse_to_density.items()
    }
    group_scores = {
        key: density_scores[dominant_density[key]]
        for key in group_year_counts
    }
    seen_anchors: set[int] = set()
    output: list[tuple[int, np.ndarray]] = []
    for key in sorted(groups):
        neighboring_indices: list[int] = []
        neighboring_keys: list[tuple[int, int, int, int]] = []
        for d_sol, d_lon, d_z, d_speed in offsets:
            neighbor = (
                (key[0] + d_sol) % sol_bins,
                (key[1] + d_lon) % lon_bins,
                key[2] + d_z,
                key[3] + d_speed,
            )
            if neighbor in groups:
                neighboring_keys.append(neighbor)
                neighboring_indices.extend(groups[neighbor])
        indices = np.asarray(sorted(set(neighboring_indices)), dtype=int)
        if indices.size < config.minimum_training_members:
            continue
        ranked_keys = sorted(
            set(neighboring_keys),
            key=lambda value: (-group_scores[value][0], -group_scores[value][1], -group_scores[value][2], value),
        )
        if key not in ranked_keys[: config.candidate_peak_quota]:
            continue
        anchor_pool = np.asarray(density_groups[dominant_density[key]], dtype=int)
        if anchor_pool.size < config.minimum_training_members:
            anchor_pool = np.asarray(groups[key], dtype=int)
        if anchor_pool.size < config.minimum_anchor_bin_members:
            anchor_pool = indices
        ordered = sorted(anchor_pool.tolist(), key=lambda index: (-density_counts[index], event_ids[index]))
        retained = 0
        for anchor in ordered:
            if anchor in seen_anchors:
                continue
            seen_anchors.add(anchor)
            output.append((anchor, indices))
            retained += 1
            if retained >= config.candidate_anchor_quota:
                break
    return output


def propose_cells(frame: pd.DataFrame, config: CCFConfig) -> tuple[CanonicalCell, ...]:
    """Generate cells from occupied coarse anchor groups.

    Each scale retains a fixed quota of anchors from compact recurrence-aware
    density modes. The fit sees the mode's coarse bin and one-bin physical
    neighborhood, bounded to the nearest physical members around the anchor.
    This keeps the candidate opportunity deterministic while avoiding an O(n^2)
    all-event pass.
    """

    frame = normalize_frame(frame)
    cells: set[CanonicalCell] = set()
    for scale_index in range(len(config.scales)):
        for anchor_index, candidate_indices in _anchor_groups(frame, scale_index, config):
            cell = _fit_anchor_subset(frame, anchor_index, scale_index, config, candidate_indices)
            if cell is not None:
                cells.add(cell)
    return tuple(sorted(cells))


def _proposal_alias_key(cell: CanonicalCell, config: CCFConfig) -> tuple[int, ...]:
    block = config.proposal_alias_block
    return tuple(
        [cell.scale_index]
        + [int(value // block) for value in cell.as_tuple()[1:]]
    )


def _proposal_alias_distance(a: CanonicalCell, b: CanonicalCell, config: CCFConfig) -> float:
    if a.scale_index != b.scale_index:
        return math.inf
    ga = cell_geometry(a, config)
    gb = cell_geometry(b, config)
    widths = _scale_widths(config.scales[a.scale_index], config)
    return float(
        (float(circ_diff(ga["sol"], gb["sol"])) / widths["sol_cell"]) ** 2
        + (float(circ_diff(ga["lon"], gb["lon"])) / widths["lon_cell"]) ** 2
        + ((ga["z"] - gb["z"]) / widths["z_cell"]) ** 2
        + ((ga["log_speed"] - gb["log_speed"]) / widths["speed_log_cell"]) ** 2
        + ((ga["dlon"] - gb["dlon"]) / widths["drift_lon_cell"]) ** 2
        + ((ga["dz"] - gb["dz"]) / widths["drift_z_cell"]) ** 2
        + ((ga["dlog_speed"] - gb["dlog_speed"]) / widths["drift_log_speed_cell"]) ** 2
    )


def _stabilize_proposals(
    proposals: Mapping[int, tuple[CanonicalCell, ...]], config: CCFConfig,
) -> dict[int, tuple[CanonicalCell, ...]]:
    """Coalesce fold-jittered proposals into deterministic lattice-block medoids."""

    stabilized, _ = _stabilized_proposal_data(proposals, config)
    return stabilized


def _stabilized_proposal_data(
    proposals: Mapping[int, tuple[CanonicalCell, ...]], config: CCFConfig,
) -> tuple[dict[int, tuple[CanonicalCell, ...]], dict[CanonicalCell, tuple[CanonicalCell, ...]]]:
    grouped: dict[tuple[int, ...], list[CanonicalCell]] = {}
    for cells in proposals.values():
        for cell in cells:
            grouped.setdefault(_proposal_alias_key(cell, config), []).append(cell)
    representatives: dict[tuple[int, ...], CanonicalCell] = {}
    for alias_key, cells in grouped.items():
        unique = tuple(sorted(set(cells)))
        representatives[alias_key] = min(
            unique,
            key=lambda cell: (
                sum(_proposal_alias_distance(cell, other, config) for other in unique),
                cell.as_tuple(),
            ),
        )
    aliases_by_representative: dict[CanonicalCell, tuple[CanonicalCell, ...]] = {}
    for alias_key, cells in grouped.items():
        representative = representatives[alias_key]
        aliases_by_representative[representative] = tuple(sorted(set(cells)))
    stabilized = {
        year: tuple(sorted({representatives[_proposal_alias_key(cell, config)] for cell in cells}))
        for year, cells in proposals.items()
    }
    return stabilized, aliases_by_representative


def _year_fraction(frame: pd.DataFrame, year: int, cell: CanonicalCell, config: CCFConfig) -> float:
    year_frame = frame.loc[frame["year"] == year]
    if year_frame.empty:
        return 0.0
    return float(cell_membership(year_frame, cell, config).sum() / len(year_frame))


def _year_fraction_arrays(
    features: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    cell: CanonicalCell,
    config: CCFConfig,
) -> float:
    membership = _membership_arrays(features, cell, config)
    return float(membership.sum() / membership.size) if membership.size else 0.0


def _year_fraction_batch(
    features: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    cells: Sequence[CanonicalCell],
    config: CCFConfig,
) -> np.ndarray:
    """Evaluate many cells against one year with bounded temporary arrays."""

    if not cells:
        return np.asarray([], dtype=float)
    sol, lon, lat, log_speed = features
    fractions: list[np.ndarray] = []
    for start in range(0, len(cells), MEMBERSHIP_BATCH_SIZE):
        batch = cells[start : start + MEMBERSHIP_BATCH_SIZE]
        geometries = [cell_geometry(cell, config) for cell in batch]
        centers_sol = np.asarray([geometry["sol"] for geometry in geometries], dtype=float)[:, None]
        centers_lon = np.asarray([geometry["lon"] for geometry in geometries], dtype=float)[:, None]
        centers_z = np.asarray([geometry["z"] for geometry in geometries], dtype=float)[:, None]
        centers_log_speed = np.asarray([geometry["log_speed"] for geometry in geometries], dtype=float)[:, None]
        drifts_lon = np.asarray([geometry["dlon"] for geometry in geometries], dtype=float)[:, None]
        drifts_z = np.asarray([geometry["dz"] for geometry in geometries], dtype=float)[:, None]
        drifts_log_speed = np.asarray([geometry["dlog_speed"] for geometry in geometries], dtype=float)[:, None]
        sol_half = np.asarray([geometry["sol_half"] for geometry in geometries], dtype=float)[:, None]
        radiant_half = np.asarray([geometry["radiant_half"] for geometry in geometries], dtype=float)[:, None]
        speed_log_half = np.asarray([geometry["speed_log_half"] for geometry in geometries], dtype=float)[:, None]
        x = circ_diff(sol[None, :], centers_sol)
        predicted_lon = wrap_deg(centers_lon + drifts_lon * x)
        predicted_z = np.clip(centers_z + drifts_z * x, -1.0, 1.0)
        predicted_lat = np.degrees(np.arcsin(predicted_z))
        predicted_log_speed = centers_log_speed + drifts_log_speed * x
        radiant_distance = _radiant_distance_deg(
            lon[None, :],
            lat[None, :],
            predicted_lon,
            predicted_lat,
        )
        membership = (
            (np.abs(x) <= sol_half)
            & (radiant_distance <= radiant_half)
            & (np.abs(log_speed[None, :] - predicted_log_speed) <= speed_log_half)
        )
        fractions.append(membership.mean(axis=1))
    return np.concatenate(fractions)


def _year_fraction_family_batch(
    features: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    families: Sequence[Sequence[CanonicalCell]],
    config: CCFConfig,
) -> np.ndarray:
    """Evaluate fold-stable cell families using union membership."""

    return np.asarray(
        [
            float(cell_membership_family_from_features(features, family, config).mean())
            if features[0].size
            else 0.0
            for family in families
        ],
        dtype=float,
    )


def cell_membership_family_from_features(
    features: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    cells: Sequence[CanonicalCell],
    config: CCFConfig,
) -> np.ndarray:
    """Evaluate a cell family without rebuilding a temporary DataFrame."""

    membership = np.zeros(features[0].size, dtype=bool)
    for cell in cells:
        membership |= _membership_arrays(features, cell, config)
    return membership


def _candidate_adjacent(a: CanonicalCell, b: CanonicalCell, config: CCFConfig) -> bool:
    if abs(a.scale_index - b.scale_index) > 1:
        return False
    ga = cell_geometry(a, config)
    gb = cell_geometry(b, config)
    if abs(float(circ_diff(ga["sol"], gb["sol"]))) > ga["sol_half"] + gb["sol_half"]:
        return False
    sample_solar = (
        ga["sol"],
        gb["sol"],
        float(wrap_deg(ga["sol"] - ga["sol_half"])),
        float(wrap_deg(ga["sol"] + ga["sol_half"])),
        float(wrap_deg(gb["sol"] - gb["sol_half"])),
        float(wrap_deg(gb["sol"] + gb["sol_half"])),
    )
    for solar in sample_solar:
        xa = float(circ_diff(solar, ga["sol"]))
        xb = float(circ_diff(solar, gb["sol"]))
        la = float(wrap_deg(ga["lon"] + ga["dlon"] * xa))
        lb = float(wrap_deg(gb["lon"] + gb["dlon"] * xb))
        za = float(np.clip(ga["z"] + ga["dz"] * xa, -1.0, 1.0))
        zb = float(np.clip(gb["z"] + gb["dz"] * xb, -1.0, 1.0))
        da = math.degrees(math.asin(za))
        db = math.degrees(math.asin(zb))
        radiant_gap = float(_radiant_distance_deg(np.asarray([la]), np.asarray([da]), lb, db)[0])
        speed_gap = abs((ga["log_speed"] + ga["dlog_speed"] * xa) - (gb["log_speed"] + gb["dlog_speed"] * xb))
        if radiant_gap > ga["radiant_half"] + gb["radiant_half"]:
            return False
        if speed_gap > ga["speed_log_half"] + gb["speed_log_half"]:
            return False
    return True


def select_local_maxima(results: Sequence[CandidateResult], config: CCFConfig) -> tuple[CandidateResult, ...]:
    """Apply the fixed physical adjacency and lexicographic plateau rule."""

    buckets: dict[tuple[int, int, int, int, int], list[CandidateResult]] = {}
    for result in results:
        buckets.setdefault(_selection_bucket(result.cell, config), []).append(result)
    selected: list[CandidateResult] = []
    for candidate in results:
        suppressed = False
        bucket = _selection_bucket(candidate.cell, config)
        for neighbor_bucket in _neighbor_selection_buckets(bucket, config):
            for other in buckets.get(neighbor_bucket, ()):
                if other.cell == candidate.cell or not _candidate_adjacent(candidate.cell, other.cell, config):
                    continue
                if other.score > candidate.score + 1e-12:
                    suppressed = True
                    break
                if abs(other.score - candidate.score) <= 1e-12 and other.cell < candidate.cell:
                    suppressed = True
                    break
            if suppressed:
                break
        if not suppressed:
            selected.append(candidate)
    return tuple(sorted(selected, key=candidate_sort_key))


def _selection_bucket(cell: CanonicalCell, config: CCFConfig) -> tuple[int, int, int, int, int]:
    geometry = cell_geometry(cell, config)
    sol_width = 2.0 * config.base_sol_half_width_deg
    lon_width = 2.0 * config.base_radiant_half_width_deg
    z_width = 2.0 * math.sin(math.radians(config.base_radiant_half_width_deg))
    speed_width = _scale_widths(1.0, config)["speed_log_half"] * 2.0
    sol_bins = max(1, int(round(360.0 / sol_width)))
    lon_bins = max(1, int(round(360.0 / lon_width)))
    return (
        cell.scale_index,
        int(math.floor(geometry["sol"] / sol_width)) % sol_bins,
        int(math.floor(geometry["lon"] / lon_width)) % lon_bins,
        int(math.floor((geometry["z"] + 1.0) / z_width)),
        int(math.floor((geometry["log_speed"] - math.log(config.minimum_speed_km_s)) / speed_width)),
    )


def _neighbor_selection_buckets(
    bucket: tuple[int, int, int, int, int], config: CCFConfig,
) -> Iterable[tuple[int, int, int, int, int]]:
    scale_index, q_sol, q_lon, q_z, q_speed = bucket
    sol_bins = max(1, int(round(360.0 / (2.0 * config.base_sol_half_width_deg))))
    lon_bins = max(1, int(round(360.0 / (2.0 * config.base_radiant_half_width_deg))))
    for scale in range(max(0, scale_index - 1), min(len(config.scales), scale_index + 2)):
        for d_sol, d_lon, d_z, d_speed in itertools.product((-2, -1, 0, 1, 2), repeat=4):
            yield (
                scale,
                (q_sol + d_sol) % sol_bins,
                (q_lon + d_lon) % lon_bins,
                q_z + d_z,
                q_speed + d_speed,
            )


def candidate_sort_key(candidate: CandidateResult) -> tuple[float, float, float, int, str]:
    return (
        1.0 if candidate.p_global is None else candidate.p_global,
        candidate.recurrence_p,
        -candidate.second_strongest_log_evidence,
        -candidate.represented_years,
        candidate.cell.hash_hex(),
    )


class CCFScanner:
    """Cross-fitted scanner with no access to target labels or IDs."""

    def __init__(self, config: CCFConfig | None = None) -> None:
        self.config = config or CCFConfig()
        self._proposal_aliases: dict[CanonicalCell, tuple[CanonicalCell, ...]] = {}

    def propose_by_fold(self, frame: pd.DataFrame) -> dict[int, tuple[CanonicalCell, ...]]:
        frame = normalize_frame(frame)
        years = tuple(sorted(int(year) for year in frame["year"].unique()))
        if len(years) < 3:
            raise ValueError("CC-CFRS requires at least three observing years")
        proposals: dict[int, tuple[CanonicalCell, ...]] = {}
        for heldout in years:
            training = frame.loc[frame["year"] != heldout]
            proposals[heldout] = propose_cells(training, self.config)
        stabilized, aliases = _stabilized_proposal_data(proposals, self.config)
        self._proposal_aliases = aliases
        return stabilized

    def scan(
        self,
        frame: pd.DataFrame,
        null_factory: Callable[[int], pd.DataFrame],
        randomizations: int | None = None,
    ) -> ScanResult:
        """Run candidate generation, held-out p-values, recurrence, and selection.

        ``null_factory(i)`` must return the i-th complete held-out null panel
        with identical row IDs, years, and nuisance-preserving schema.  The
        factory is called exactly ``randomizations`` times.
        """

        frame = normalize_frame(frame)
        proposals = self.propose_by_fold(frame)
        years = tuple(sorted(proposals))
        randomization_count = self.config.heldout_randomizations if randomizations is None else int(randomizations)
        if randomization_count < 1:
            raise ValueError("randomizations must be positive")
        proposal_sets = {year: set(proposals[year]) for year in years}
        universe = sorted(
            cell
            for cell in {cell for fold in proposals.values() for cell in fold}
            if sum(cell in proposal_sets[year] for year in years) >= self.config.minimum_represented_years
        )
        families = {
            cell: self._proposal_aliases.get(cell, (cell,))
            for cell in universe
        }
        year_frames = _year_feature_arrays(frame)
        expected_identity = frame.loc[:, ["event_id", "year"]].reset_index(drop=True)
        observed_by_cell = {cell: [0.0] * len(years) for cell in universe}
        for year_index, year in enumerate(years):
            active_cells = [cell for cell in universe if cell in proposal_sets[year]]
            active_fractions = _year_fraction_family_batch(
                year_frames[year], [families[cell] for cell in active_cells], self.config,
            )
            for cell, fraction in zip(active_cells, active_fractions):
                observed_by_cell[cell][year_index] = float(fraction)
        results: list[CandidateResult] = []
        eligible: list[
            tuple[CanonicalCell, tuple[CanonicalCell, ...], tuple[float, ...], tuple[bool, ...]]
        ] = []
        for cell in universe:
            present = tuple(cell in proposal_sets[year] for year in years)
            observed = tuple(observed_by_cell[cell])
            if sum(statistic > 0.0 for statistic in observed) < self.config.minimum_represented_years:
                continue
            eligible.append((cell, families[cell], observed, present))
        exceedances = np.zeros((len(eligible), len(years)), dtype=np.int32)
        eligible_by_year: dict[int, list[tuple[int, CanonicalCell, tuple[CanonicalCell, ...], float]]] = {}
        for year_index, year in enumerate(years):
            eligible_by_year[year] = [
                (candidate_index, cell, aliases, observed[year_index])
                for candidate_index, (cell, aliases, observed, present) in enumerate(eligible)
                if present[year_index]
            ]
        for randomization_index in range(randomization_count):
            null_frame = normalize_frame(null_factory(randomization_index))
            null_identity = null_frame.loc[:, ["event_id", "year"]].reset_index(drop=True)
            if not null_identity.equals(expected_identity):
                raise ValueError("null panel changed event IDs or years")
            null_year_arrays = _year_feature_arrays(null_frame)
            for year_index, year in enumerate(years):
                active = eligible_by_year[year]
                active_fractions = _year_fraction_family_batch(
                    null_year_arrays[year],
                    [aliases for _, _, aliases, _ in active], self.config,
                )
                for (candidate_index, _, _, observed_stat), null_stat in zip(active, active_fractions):
                    exceedances[candidate_index, year_index] += int(null_stat >= observed_stat - 1e-15)
        for candidate_index, (cell, aliases, observed, present) in enumerate(eligible):
            p_values = tuple(
                float((1 + exceedances[candidate_index, year_index]) / (randomization_count + 1.0))
                if is_present
                else 1.0
                for year_index, is_present in enumerate(present)
            )
            recurrence_p = combine_recurrence_p(p_values)
            results.append(
                CandidateResult(
                    cell=cell,
                    heldout_p_values=p_values,
                    heldout_statistics=observed,
                    recurrence_p=recurrence_p,
                    represented_years=sum(stat > 0.0 for stat in observed),
                    alias_cells=aliases,
                )
            )
        selected = select_local_maxima(results, self.config)
        return ScanResult(tuple(sorted(results, key=candidate_sort_key)), selected)


__all__ = [
    "CCFConfig",
    "CCFScanner",
    "CandidateResult",
    "CanonicalCell",
    "ScanResult",
    "cell_geometry",
    "cell_membership",
    "circ_diff",
    "combine_recurrence_p",
    "normalize_frame",
    "propose_cells",
    "select_local_maxima",
    "wrap_deg",
]
