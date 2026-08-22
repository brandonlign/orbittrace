"""Nuisance-preserving recurrence-destroying null panels for CC-CFRS."""
from __future__ import annotations

from collections import defaultdict
import hashlib
from typing import Iterable

import numpy as np
import pandas as pd

from .core import CCFConfig, normalize_frame, radiant_z


def derive_seed(*parts: object) -> int:
    """Derive a reproducible uint64 seed from an explicit namespace."""

    encoded = "||".join(str(part) for part in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(encoded).digest()[:8], "big", signed=False)


def _normalized_frame_hash(frame: pd.DataFrame) -> str:
    """Hash the exact normalized physical table used by a null generator."""

    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _source_stratum(frame: pd.DataFrame, config: CCFConfig) -> np.ndarray:
    """Create fixed, label-free broad-source strata.

    The bins are deliberately coarse.  They preserve broad radiant and speed
    structure while the independent within-stratum phase permutation breaks
    the exact solar-longitude/radiant association used by a recurring cell.
    """

    lon_bin = np.floor(
        np.mod(frame["radiant_lon_deg"].to_numpy(float), 360.0) / config.null_radiant_lon_bin_deg
    ).astype(int)
    z_bin = np.floor(
        (np.asarray(radiant_z(frame["radiant_lat_deg"].to_numpy(float))) + 1.0) / config.null_z_bin_width
    ).astype(int)
    speed = frame["speed_km_s"].to_numpy(float)
    speed_edges = np.asarray(config.null_speed_edges_km_s, dtype=float)
    speed_bin = np.clip(np.searchsorted(speed_edges, speed, side="right") - 1, 0, len(speed_edges) - 2)
    return np.asarray([f"{a}:{b}:{c}" for a, b, c in zip(lon_bin, z_bin, speed_bin)], dtype=object)


class PhasePermutationNull:
    """Callable generator that preserves rows and broad source structure."""

    def __init__(
        self,
        frame: pd.DataFrame,
        config: CCFConfig | None = None,
        namespace: str = "cc-cfrs-v1",
        endpoint_hash: str | None = None,
        require_target_interval_excluded: bool = False,
    ) -> None:
        self.frame = normalize_frame(frame)
        self.config = config or CCFConfig()
        self.namespace = namespace
        self.endpoint_hash = str(endpoint_hash or _normalized_frame_hash(self.frame)).casefold()
        if len(self.endpoint_hash) != 64 or any(
            character not in "0123456789abcdef" for character in self.endpoint_hash.casefold()
        ):
            raise ValueError("endpoint_hash must be a 64-character hexadecimal SHA-256 digest")
        sol = self.frame["sol_lon_deg"].to_numpy(float)
        excluded = (sol >= self.config.exclude_sol_low_deg) & (sol <= self.config.exclude_sol_high_deg)
        if require_target_interval_excluded and excluded.any():
            raise ValueError(
                "PhasePermutationNull was configured to require the inclusive target-excluded interval to be removed"
            )
        strata = _source_stratum(self.frame, self.config)
        self._groups: dict[tuple[int, str], np.ndarray] = {}
        for (year, source), indices in self._group_indices(self.frame["year"].to_numpy(int), strata):
            self._groups[(year, source)] = indices

    @staticmethod
    def _group_indices(years: np.ndarray, strata: np.ndarray) -> Iterable[tuple[tuple[int, str], np.ndarray]]:
        groups: dict[tuple[int, str], list[int]] = defaultdict(list)
        for index, key in enumerate(zip(years, strata)):
            groups[(int(key[0]), str(key[1]))].append(index)
        for key in sorted(groups):
            yield key, np.asarray(groups[key], dtype=int)

    def __call__(self, randomization_index: int) -> pd.DataFrame:
        rng = np.random.default_rng(
            derive_seed("cc-cfrs-v1", self.endpoint_hash, self.namespace, "phase-permutation", randomization_index)
        )
        out = self.frame.copy()
        values = out["sol_lon_deg"].to_numpy(float).copy()
        for key in sorted(self._groups):
            indices = self._groups[key]
            if indices.size > 1:
                values[indices] = values[rng.permutation(indices)]
        out["sol_lon_deg"] = values
        return out


__all__ = ["PhasePermutationNull", "derive_seed"]
