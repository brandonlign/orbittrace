"""One fixed recurrent hierarchy method for controls and blind discovery.

The method uses one physical feature representation and one HDBSCAN hierarchy
per input panel.  EOM parent clusters preserve the full-catalogue behaviour of
the existing recurrent-EOM method; leaf descendants preserve compact weak
structures that an EOM-only extraction can absorb into a broad parent.  Both
levels go through the same source, stability, orbital, and untouched-year
checks.  No target labels or target coordinates are read by this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd

from pipeline.pr57_novel import run_novel_search as base


@dataclass(frozen=True)
class UnifiedConfig:
    """Frozen configuration for the exploratory unified method."""

    feature_scales: tuple[float, float, float, float] = (3.5, 3.0, 2.5, 2.5)
    min_cluster_size: int = 12
    min_samples: int = 4
    hierarchy_methods: tuple[str, str] = ("eom", "leaf")
    max_novel_members: int = 300
    max_scaled_rms: float = 1.35
    max_solar_sigma_deg: float = 2.5
    min_membership_probability: float = 0.35
    min_nights: int = 4
    min_stations: int = 6
    max_one_night_fraction: float = 0.50
    max_one_station_set_fraction: float = 0.50
    min_orbit_fraction: float = 0.80
    max_orbit_median_d: float = 0.10
    max_orbit_q90_d: float = 0.20
    min_split_observed: int = 4
    max_split_p: float = 0.01
    max_orbit_null_p: float = 0.01
    max_catalog_solar_delta_deg: float = 7.0
    max_catalog_radiant_distance: float = 2.5
    max_catalog_radiant_without_orbit: float = 2.0
    max_catalog_orbit_d: float = 0.20
    dedup_distance: float = 1.0

    def __post_init__(self) -> None:
        if len(self.feature_scales) != 4 or any(value <= 0 for value in self.feature_scales):
            raise ValueError("feature_scales must contain four positive values")
        if self.min_cluster_size < 2 or self.min_samples < 1:
            raise ValueError("cluster sizes must be positive")
        if not self.hierarchy_methods or any(value not in {"eom", "leaf"} for value in self.hierarchy_methods):
            raise ValueError("hierarchy_methods must contain only eom or leaf")


def _scaled_features(features: np.ndarray, config: UnifiedConfig) -> np.ndarray:
    return features / np.asarray(config.feature_scales, dtype=float)[None, :]


def cluster_hierarchy(features: np.ndarray, config: UnifiedConfig | None = None) -> list[dict[str, Any]]:
    """Return EOM and leaf candidates from one fixed feature panel.

    The returned members are integer row positions into ``features``.  The
    clustering stage never receives truth labels.
    """

    config = config or UnifiedConfig()
    scaled = _scaled_features(np.asarray(features, dtype=float), config)
    output: list[dict[str, Any]] = []
    for method_index, selection_method in enumerate(config.hierarchy_methods):
        model = base.HDBSCAN(
            min_cluster_size=config.min_cluster_size,
            min_samples=config.min_samples,
            cluster_selection_method=selection_method,
            leaf_size=60,
            n_jobs=-1,
        )
        assignments = model.fit_predict(scaled)
        probabilities = np.asarray(model.probabilities_, dtype=float)
        for cluster in [int(value) for value in np.unique(assignments) if int(value) >= 0]:
            members = np.flatnonzero(assignments == cluster)
            if members.size < config.min_cluster_size:
                continue
            output.append(
                {
                    "method": selection_method,
                    "cluster": cluster,
                    "global_cluster": method_index * 1_000_000 + cluster,
                    "members": members,
                    "size": int(members.size),
                    "mean_probability": float(np.mean(probabilities[members])),
                    "assignments": assignments,
                }
            )
    return output


def best_known_cluster(
    labels: pd.Series | np.ndarray,
    clusters: Iterable[dict[str, Any]],
    target: str,
) -> dict[str, Any]:
    """Score the best hierarchy member set against a held-out known label."""

    truth = np.asarray(labels, dtype=str)
    actual = truth == str(target)
    total = int(actual.sum())
    best: dict[str, Any] | None = None
    for candidate in clusters:
        predicted = np.zeros(len(truth), dtype=bool)
        predicted[np.asarray(candidate["members"], dtype=int)] = True
        true_positive = int(np.sum(predicted & actual))
        if not true_positive:
            continue
        size = int(predicted.sum())
        precision = true_positive / size
        recall = true_positive / total if total else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        score = {
            "target": str(target),
            "true_count": total,
            "method": candidate["method"],
            "cluster": int(candidate["global_cluster"]),
            "cluster_size": size,
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "recovered": bool(precision >= 0.35 and recall >= 0.35 and f1 >= 0.35),
        }
        if best is None or score["f1"] > best["f1"]:
            best = score
    return best or {
        "target": str(target),
        "true_count": total,
        "method": None,
        "cluster": None,
        "cluster_size": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
        "recovered": False,
    }


def largest_non_target_fraction(
    labels: pd.Series | np.ndarray,
    clusters: Iterable[dict[str, Any]],
    target: str,
) -> float:
    """Return the largest cluster containing no member of the named target."""

    truth = np.asarray(labels, dtype=str)
    fractions = []
    for candidate in clusters:
        members = np.asarray(candidate["members"], dtype=int)
        if members.size and not bool(np.any(truth[members] == str(target))):
            fractions.append(float(members.size / len(truth)))
    return max(fractions, default=0.0)


def _global_night_split(nights: np.ndarray) -> np.ndarray:
    order = {value: index for index, value in enumerate(sorted(np.unique(nights).tolist()))}
    return np.asarray([order[value] % 2 == 0 for value in nights], dtype=bool)


def _candidate_distance(left: np.ndarray, right: np.ndarray) -> float:
    return float(
        np.sqrt(
            (float(base.circ_diff(left[0], right[0])) / 3.5) ** 2
            + ((left[1] - right[1]) / 3.0) ** 2
            + ((left[2] - right[2]) / 2.5) ** 2
            + (float(base.circ_diff(left[3], right[3])) / 2.5) ** 2
        )
    )


def strict_iau_match(
    center: np.ndarray,
    medoid: np.ndarray,
    catalog: list[dict[str, Any]],
    config: UnifiedConfig,
) -> dict[str, Any]:
    """Use the repaired label-free geometry veto from the blind rediscovery."""

    best: dict[str, Any] | None = None
    for item in catalog:
        solar_delta = abs(float(base.circ_diff(center[3], item["sol"])))
        radiant = float(
            np.sqrt(
                (float(base.circ_diff(center[0], item["slon"])) / 4.0) ** 2
                + ((center[1] - item["beta"]) / 4.0) ** 2
                + ((center[2] - item["vg"]) / 3.0) ** 2
            )
        )
        orbit_distance = (
            None
            if item.get("orbit") is None
            else float(base.orbit_distance_matrix(medoid[None, :], item["orbit"][None, :])[0, 0])
        )
        matched = bool(
            solar_delta <= config.max_catalog_solar_delta_deg
            and (
                (
                    orbit_distance is not None
                    and radiant <= config.max_catalog_radiant_distance
                    and orbit_distance <= config.max_catalog_orbit_d
                )
                or (orbit_distance is None and radiant <= config.max_catalog_radiant_without_orbit)
            )
        )
        score = (solar_delta / 7.0) ** 2 + radiant**2 + (
            (orbit_distance / 0.15) ** 2 if orbit_distance is not None else 1.0
        )
        candidate = {
            "matched": matched,
            "code": item["code"],
            "name": item["name"],
            "status": item["status"],
            "solar_delta": solar_delta,
            "radiant_scaled_distance": radiant,
            "orbit_d": orbit_distance,
            "score": float(score),
        }
        if best is None or candidate["score"] < best["score"]:
            best = candidate
    return best or {"matched": False}


def _novel_candidate(
    prepared: dict[str, Any],
    cluster: dict[str, Any],
    month: int,
    catalog: list[dict[str, Any]],
    config: UnifiedConfig,
) -> dict[str, Any] | None:
    """Apply the frozen target-free candidate gates to one hierarchy node."""

    data = prepared["data"]
    raw = prepared["raw"]
    scaled = prepared["scaled"]
    nights = prepared["nights"]
    members = np.asarray(cluster["members"], dtype=int)
    if not config.min_cluster_size <= len(members) <= config.max_novel_members:
        return None
    points = scaled[members]
    center_scaled = np.median(points, axis=0)
    scaled_rms = float(np.sqrt(np.mean(np.sum((points - center_scaled[None, :]) ** 2, axis=1))))
    sigma_raw = base.robust_sigma(raw[members], np.asarray([0.3, 0.3, 0.3, 0.3]))
    solar_sigma = float(sigma_raw[3])
    if scaled_rms > config.max_scaled_rms or solar_sigma > config.max_solar_sigma_deg:
        return None
    mean_probability = float(cluster["mean_probability"])
    if mean_probability < config.min_membership_probability:
        return None

    member_nights = nights[members]
    unique_nights, night_counts = np.unique(member_nights, return_counts=True)
    if len(unique_nights) < config.min_nights or night_counts.max() / len(members) > config.max_one_night_fraction:
        return None
    station_sets = data.iloc[members]["participating_stations"].fillna("").astype(str)
    all_stations = set().union(*(base.station_tokens(value) for value in station_sets))
    top_station_fraction = float(station_sets.value_counts(normalize=True).iloc[0]) if len(station_sets) else 1.0
    if len(all_stations) < config.min_stations or top_station_fraction > config.max_one_station_set_fraction:
        return None

    member_frame = data.iloc[members].reset_index(drop=True)
    orbit_mask = base.valid_orbits(member_frame)
    if orbit_mask.sum() < config.min_cluster_size or orbit_mask.mean() < config.min_orbit_fraction:
        return None
    member_orbits = member_frame.loc[orbit_mask, base.ORBIT_COLUMNS].to_numpy(float)
    orbit = base.orbit_summary(member_orbits)
    if orbit["median_d"] > config.max_orbit_median_d or orbit["q90_d"] > config.max_orbit_q90_d:
        return None

    split_a_all = _global_night_split(nights)
    split_a_members = split_a_all[members]
    if split_a_members.sum() < 5 or (~split_a_members).sum() < 5:
        return None
    rng = np.random.default_rng(base.SEED + month * 10000 + int(cluster["global_cluster"]))
    a_to_b = base.density_test(scaled[members][split_a_members], scaled[~split_a_all], rng)
    b_to_a = base.density_test(scaled[members][~split_a_members], scaled[split_a_all], rng)
    if min(a_to_b["observed"], b_to_a["observed"]) < config.min_split_observed:
        return None
    if max(a_to_b["p"], b_to_a["p"]) > config.max_split_p:
        return None

    center_raw = center_scaled * np.asarray(config.feature_scales, dtype=float)
    absolute_center = np.asarray(
        [center_raw[0], center_raw[1], center_raw[2], (prepared["center_sol"] + center_raw[3]) % 360.0]
    )
    source = base.source_region(float(absolute_center[0]), float(absolute_center[1]), float(absolute_center[2]))
    if source is not None:
        return None
    orbit_null = base.orbit_null(
        data,
        member_orbits,
        float(absolute_center[3]),
        max(3 * solar_sigma, 1.5),
        rng,
    )
    if orbit_null["p"] > config.max_orbit_null_p:
        return None
    nearest_iau = strict_iau_match(absolute_center, orbit["medoid"], catalog, config)
    if nearest_iau.get("matched"):
        return None

    score = (
        math_log1p(len(members))
        + mean_probability
        - scaled_rms
        - solar_sigma / 4.0
        - orbit["median_d"] * 5.0
        - max(a_to_b["p"], b_to_a["p"]) * 10.0
    )
    return {
        "month": int(month),
        "discovery_year": int(prepared.get("year", 2025)),
        "cluster": int(cluster["global_cluster"]),
        "hierarchy_method": cluster["method"],
        "members_discovery": int(len(members)),
        "members_2025": int(len(members)),
        "center": absolute_center.tolist(),
        "sigma_raw": sigma_raw.tolist(),
        "scaled_center": center_scaled.tolist(),
        "scaled_rms": scaled_rms,
        "solar_sigma_deg": solar_sigma,
        "mean_probability": mean_probability,
        "nights_2025": int(len(unique_nights)),
        "stations_2025": int(len(all_stations)),
        "orbit_medoid": orbit["medoid"].tolist(),
        "orbit_median_d": orbit["median_d"],
        "orbit_q90_d": orbit["q90_d"],
        "orbit_null": orbit_null,
        "split_a_to_b": a_to_b,
        "split_b_to_a": b_to_a,
        "nearest_iau": nearest_iau,
        "score": float(score),
        "member_ids_2025": member_frame["unique_trajectory_identifier"].astype(str).tolist(),
        "member_rows_2025": member_frame,
    }


def math_log1p(value: int) -> float:
    """Named wrapper keeps the score formula easy to audit."""

    return float(np.log1p(value))


def scan_month(
    year: int,
    month: int,
    catalog: list[dict[str, Any]],
    config: UnifiedConfig | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Run one target-free month scan and return deduplicated survivors."""

    config = config or UnifiedConfig()
    prepared = base.prepare(base.load_month(year, month), year, month)
    prepared["year"] = int(year)
    print(f"{year}-{month:02d}: scanning {len(prepared['data']):,} quality sporadics", flush=True)
    clusters = cluster_hierarchy(prepared["raw"], config)
    candidates = [
        candidate
        for cluster in clusters
        if (candidate := _novel_candidate(prepared, cluster, month, catalog, config)) is not None
    ]
    candidates.sort(key=lambda item: item["score"], reverse=True)
    deduped: list[dict[str, Any]] = []
    for candidate in candidates:
        center = np.asarray(candidate["center"], dtype=float)
        if any(_candidate_distance(center, np.asarray(kept["center"], dtype=float)) < config.dedup_distance for kept in deduped):
            continue
        deduped.append(candidate)
    print(f"{year}-{month:02d}: hierarchy_nodes={len(clusters)}; uncatalogued_candidates={len(deduped)}", flush=True)
    return deduped, {
        "quality_sporadics": int(len(prepared["data"])),
        "hierarchy_nodes": int(len(clusters)),
        "uncatalogued_candidates": int(len(deduped)),
    }


def jsonable(value: Any) -> Any:
    if isinstance(value, (np.integer, np.floating, np.bool_)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def serializable_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return jsonable({key: value for key, value in candidate.items() if key != "member_rows_2025"})


def reveal_target_overlap(
    candidates: Iterable[dict[str, Any]], target_path: Path, discovery_year: int = 2025
) -> list[dict[str, Any]]:
    """Posthoc-only target reveal; never called before ranking or validation."""

    target = pd.read_csv(target_path)
    target_times = set(pd.to_datetime(target["Tobs"], utc=True).dt.floor("s").astype("int64").tolist())
    output = []
    for rank, candidate in enumerate(candidates, start=1):
        values = pd.to_datetime(
            candidate["member_rows_2025"]["beginning_utc_time"], utc=True, errors="coerce"
        ).dt.floor("s")
        candidate_times = set(values.dropna().astype("int64").tolist())
        overlap = len(target_times & candidate_times)
        members = int(candidate.get("members_discovery", candidate["members_2025"]))
        target_count = int(pd.to_datetime(target["Tobs"], utc=True).dt.year.eq(int(discovery_year)).sum())
        output.append(
            {
                "pre_reveal_rank": rank,
                "month": candidate["month"],
                "hierarchy_method": candidate["hierarchy_method"],
                "discovery_year": int(discovery_year),
                "members_discovery": members,
                "target_overlap": int(overlap),
                "target_precision": float(overlap / members) if members else 0.0,
                "target_recall_discovery_year": float(overlap / max(1, target_count)),
            }
        )
    return output


def reveal_full_history_overlap(
    candidates: Iterable[dict[str, Any]], target_path: Path, discovery_year: int
) -> list[dict[str, Any]]:
    """Posthoc exact overlap across discovery and every validated year."""

    target = pd.read_csv(target_path)
    target_times = pd.to_datetime(target["Tobs"], utc=True, errors="coerce")
    target_by_year: dict[int, set[str]] = {}
    for value in target_times.dropna():
        target_by_year.setdefault(int(value.year), set()).add(value.strftime("%Y%m%d%H%M%S"))

    def event_key(value: Any) -> str:
        digits = "".join(character for character in str(value) if character.isdigit())
        return digits[:14]

    output = []
    for rank, candidate in enumerate(candidates, start=1):
        ids_by_year: dict[int, list[str]] = {
            int(discovery_year): list(candidate.get("member_ids_2025", []))
        }
        for year, validation in candidate.get("validation", {}).items():
            ids_by_year[int(year)] = list(validation.get("member_ids", []))

        annual = {}
        total_overlap = 0
        total_members = 0
        total_target = 0
        for year in sorted(target_by_year):
            member_keys = {event_key(value) for value in ids_by_year.get(year, [])}
            overlap = len(member_keys & target_by_year[year])
            target_count = len(target_by_year[year])
            annual[str(year)] = {
                "members": len(member_keys),
                "target_count": target_count,
                "overlap": overlap,
                "precision": float(overlap / len(member_keys)) if member_keys else 0.0,
                "recall": float(overlap / target_count) if target_count else 0.0,
            }
            total_overlap += overlap
            total_members += len(member_keys)
            total_target += target_count
        precision = total_overlap / total_members if total_members else 0.0
        recall = total_overlap / total_target if total_target else 0.0
        output.append(
            {
                "pre_reveal_rank": rank,
                "month": candidate["month"],
                "hierarchy_method": candidate["hierarchy_method"],
                "members": total_members,
                "target_count": total_target,
                "target_overlap": total_overlap,
                "target_precision": float(precision),
                "target_recall": float(recall),
                "target_f1": float(2 * precision * recall / (precision + recall)) if precision + recall else 0.0,
                "annual": annual,
            }
        )
    return output


__all__ = [
    "UnifiedConfig",
    "best_known_cluster",
    "cluster_hierarchy",
    "largest_non_target_fraction",
    "jsonable",
    "reveal_target_overlap",
    "reveal_full_history_overlap",
    "scan_month",
    "serializable_candidate",
]
