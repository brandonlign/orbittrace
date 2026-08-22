"""Strict label-free source adapters for CC-CFRS v1.

The historical scripts use source-specific downloaders.  This adapter layer
does not import those scripts or their truth-bearing fields; it accepts a
local decoded table and normalizes only the physical columns needed by
CC-CFRS.  That keeps source acquisition/provenance separate from the method
and makes the target firewall testable before any scan is run.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd

from .core import CCFConfig, normalize_frame, wrap_deg


RadiantLonMode = Literal["ecliptic", "sun_centered"]

TRUTH_COLUMN_TOKENS = (
    "shower",
    "target",
    "truth",
    "membership",
    "background",
    "orbittrace",
    "known",
)
TRUTH_EXACT_KEYS = {"sh", "shower", "showerlabel", "showercode", "stream", "streamcode", "iau", "iaucode", "label"}


@dataclass(frozen=True)
class SourceSpec:
    source: str
    year: int | None = None
    radiant_lon_mode: RadiantLonMode = "ecliptic"
    # Discovery must retain the full solar-longitude domain.  An interval
    # exclusion is available only for an explicitly separate control panel.
    exclude_target_interval: bool = False


@dataclass(frozen=True)
class AdapterResult:
    frame: pd.DataFrame
    manifest: dict[str, object]


def _column_key(value: object) -> str:
    return re.sub(r"[^a-z0-9]", "", str(value).casefold())


def _resolve(frame: pd.DataFrame, aliases: tuple[str, ...], required: bool = True) -> str | None:
    lookup: dict[str, list[str]] = {}
    for column in frame.columns:
        lookup.setdefault(_column_key(column), []).append(str(column))
    matches: list[str] = []
    for alias in aliases:
        matches.extend(lookup.get(_column_key(alias), []))
    unique = sorted(set(matches))
    if len(unique) > 1:
        raise ValueError(f"ambiguous aliases {aliases}: matched {unique}")
    if not unique and required:
        raise ValueError(f"none of the required aliases are present: {aliases}")
    return unique[0] if unique else None


def _assert_label_free_columns(frame: pd.DataFrame) -> None:
    suspicious = []
    for column in frame.columns:
        key = _column_key(column)
        if key in TRUTH_EXACT_KEYS or any(token in key for token in TRUTH_COLUMN_TOKENS):
            suspicious.append(str(column))
    if suspicious:
        raise ValueError(f"truth-bearing columns are not accepted by the label-free adapter: {suspicious}")


def _ecliptic_from_equatorial(ra_deg: np.ndarray, dec_deg: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ra = np.deg2rad(ra_deg)
    dec = np.deg2rad(dec_deg)
    obliquity = math_radians(23.43928)
    x = np.cos(dec) * np.cos(ra)
    y = np.cos(dec) * np.sin(ra)
    z = np.sin(dec)
    ecliptic_y = y * np.cos(obliquity) + z * np.sin(obliquity)
    ecliptic_z = -y * np.sin(obliquity) + z * np.cos(obliquity)
    return (
        np.rad2deg(np.arctan2(ecliptic_y, x)) % 360.0,
        np.rad2deg(np.arcsin(np.clip(ecliptic_z, -1.0, 1.0))),
    )


def math_radians(value: float) -> float:
    """Small named wrapper keeps the conversion visible in provenance code."""

    return float(np.deg2rad(value))


def _stable_table_hash(frame: pd.DataFrame) -> str:
    payload = frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def adapt_frame(frame: pd.DataFrame, spec: SourceSpec) -> AdapterResult:
    """Normalize one decoded source table into the CC-CFRS input schema."""

    if not isinstance(frame, pd.DataFrame):
        raise TypeError("adapt_frame expects a pandas DataFrame")
    _assert_label_free_columns(frame)

    event_column = _resolve(
        frame,
        ("event_id", "unique_trajectory_identifier", "identifier", "IID", "CurNum", "id", "_#"),
    )
    year_column = _resolve(frame, ("year", "Yr", "yr"), required=False)
    sol_column = _resolve(
        frame,
        ("sol_lon_deg", "solar_longitude_deg", "sol", "soldeg", "LS", "solar_longitude"),
    )
    speed_column = _resolve(frame, ("speed_km_s", "vgeo_km_s", "vgeo", "Vg", "vg"))
    radiant_lon_column = _resolve(
        frame,
        ("radiant_lon_deg", "ecl_lon_deg", "ecliptic_longitude_deg", "ecl_lon", "lamgeo_deg", "lam"),
        required=False,
    )
    radiant_lat_column = _resolve(
        frame,
        ("radiant_lat_deg", "ecl_lat_deg", "ecliptic_latitude_deg", "ecl_lat", "betgeo_deg", "bet", "beta"),
        required=False,
    )
    if (radiant_lon_column is None) != (radiant_lat_column is None):
        raise ValueError("radiant longitude and latitude must be supplied together")
    ra_column = _resolve(frame, ("ra_deg", "RA", "right_ascension"), required=False)
    dec_column = _resolve(frame, ("dec_deg", "DECL", "dec", "declination"), required=False)
    if radiant_lon_column is None and (ra_column is None or dec_column is None):
        raise ValueError("provide ecliptic radiant columns or both equatorial RA/Dec columns")

    values = pd.DataFrame(index=frame.index)
    values["event_id"] = frame[event_column].astype(str)
    if year_column is not None:
        years = pd.to_numeric(frame[year_column], errors="coerce")
        if spec.year is not None and (years.dropna().astype(int) != int(spec.year)).any():
            raise ValueError(f"source table contains years other than requested {spec.year}")
        values["year"] = years
    elif spec.year is not None:
        values["year"] = int(spec.year)
    else:
        raise ValueError("year must be supplied by the table or SourceSpec")
    values["sol_lon_deg"] = pd.to_numeric(frame[sol_column], errors="coerce")
    if radiant_lon_column is not None:
        raw_lon = pd.to_numeric(frame[radiant_lon_column], errors="coerce").to_numpy(float)
        raw_lat = pd.to_numeric(frame[radiant_lat_column], errors="coerce").to_numpy(float)
    else:
        raw_ra = pd.to_numeric(frame[ra_column], errors="coerce").to_numpy(float)
        raw_dec = pd.to_numeric(frame[dec_column], errors="coerce").to_numpy(float)
        raw_lon, raw_lat = _ecliptic_from_equatorial(raw_ra, raw_dec)
        spec = SourceSpec(spec.source, spec.year, "ecliptic", spec.exclude_target_interval)
    if spec.radiant_lon_mode == "ecliptic":
        values["radiant_lon_deg"] = wrap_deg(raw_lon - values["sol_lon_deg"].to_numpy(float))
    else:
        values["radiant_lon_deg"] = wrap_deg(raw_lon)
    values["radiant_lat_deg"] = raw_lat
    values["speed_km_s"] = pd.to_numeric(frame[speed_column], errors="coerce")
    values = normalize_frame(values)

    before_exclusion = len(values)
    if spec.exclude_target_interval:
        sol = values["sol_lon_deg"].to_numpy(float)
        keep = ~((sol >= 20.0) & (sol <= 55.0))
        values = values.loc[keep].reset_index(drop=True)
    if values.empty:
        raise ValueError("no rows remain after the label-free source firewall")
    values["event_id"] = (
        spec.source
        + ":"
        + values["year"].astype(int).astype(str)
        + ":"
        + values["event_id"].astype(str)
    )
    values = normalize_frame(values)
    return AdapterResult(
        frame=values,
        manifest={
            "source": spec.source,
            "year": spec.year,
            "radiant_lon_mode": spec.radiant_lon_mode,
            "target_interval_excluded": spec.exclude_target_interval,
            "rows_before_target_exclusion": before_exclusion,
            "rows_after_target_exclusion": int(len(values)),
            "frame_sha256": _stable_table_hash(values),
            "columns_used": {
                "event_id": event_column,
                "year": year_column or "SourceSpec.year",
                "solar_longitude": sol_column,
                "radiant_longitude": radiant_lon_column or "derived_from_RA_Dec",
                "radiant_latitude": radiant_lat_column or "derived_from_RA_Dec",
                "speed": speed_column,
            },
        },
    )


def select_physical_columns(frame: pd.DataFrame) -> tuple[pd.DataFrame, tuple[str, ...]]:
    """Apply the raw-table firewall before any truth-bearing field is read.

    Only columns needed to identify and normalize the physical event geometry
    are retained.  All other raw fields are returned as an audit list and are
    never passed to ``adapt_frame``.
    """

    event_column = _resolve(
        frame,
        ("event_id", "unique_trajectory_identifier", "identifier", "IID", "CurNum", "id", "_#"),
    )
    year_column = _resolve(frame, ("year", "Yr", "yr"), required=False)
    sol_column = _resolve(
        frame,
        ("sol_lon_deg", "solar_longitude_deg", "sol", "soldeg", "LS", "solar_longitude"),
    )
    speed_column = _resolve(frame, ("speed_km_s", "vgeo_km_s", "vgeo", "Vg", "vg"))
    radiant_lon_column = _resolve(
        frame,
        ("radiant_lon_deg", "ecl_lon_deg", "ecliptic_longitude_deg", "ecl_lon", "lamgeo_deg", "lam"),
        required=False,
    )
    radiant_lat_column = _resolve(
        frame,
        ("radiant_lat_deg", "ecl_lat_deg", "ecliptic_latitude_deg", "ecl_lat", "betgeo_deg", "bet", "beta"),
        required=False,
    )
    if (radiant_lon_column is None) != (radiant_lat_column is None):
        raise ValueError("radiant longitude and latitude must be supplied together")
    ra_column = _resolve(frame, ("ra_deg", "RA", "right_ascension"), required=False)
    dec_column = _resolve(frame, ("dec_deg", "DECL", "dec", "declination"), required=False)
    if radiant_lon_column is None and (ra_column is None or dec_column is None):
        raise ValueError("provide ecliptic radiant columns or both equatorial RA/Dec columns")
    selected_names = {
        event_column,
        year_column,
        sol_column,
        speed_column,
        radiant_lon_column,
        radiant_lat_column,
        ra_column,
        dec_column,
    }
    selected = [str(column) for column in frame.columns if str(column) in selected_names]
    dropped = tuple(str(column) for column in frame.columns if str(column) not in selected_names)
    return frame.loc[:, selected].copy(), dropped


def adapt_raw_frame(frame: pd.DataFrame, spec: SourceSpec) -> AdapterResult:
    """Select physical columns, then run the strict normalized-table adapter."""

    selected, dropped = select_physical_columns(frame)
    result = adapt_frame(selected, spec)
    manifest = dict(result.manifest)
    manifest["raw_columns"] = [str(column) for column in frame.columns]
    manifest["pre_firewall_dropped_columns"] = list(dropped)
    manifest["pre_firewall_rule"] = (
        "only event identity, year, solar longitude, radiant geometry, and speed are retained"
    )
    return AdapterResult(result.frame, manifest)


def load_csv(path: str | Path, spec: SourceSpec, **read_csv_kwargs: object) -> AdapterResult:
    """Read one local decoded CSV and apply the strict label-free adapter."""

    source_path = Path(path)
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    frame = pd.read_csv(source_path, **read_csv_kwargs)
    result = adapt_raw_frame(frame, spec)
    manifest = dict(result.manifest)
    manifest["path"] = str(source_path)
    manifest["file_sha256"] = hashlib.sha256(source_path.read_bytes()).hexdigest()
    return AdapterResult(result.frame, manifest)


def combine_years(results: list[AdapterResult]) -> AdapterResult:
    """Combine already-adapted years while preserving provenance."""

    if not results:
        raise ValueError("at least one adapted year is required")
    combined = pd.concat([result.frame for result in results], ignore_index=True)
    combined = normalize_frame(combined)
    if combined["event_id"].duplicated().any():
        raise ValueError("adapted source event IDs are not globally unique")
    return AdapterResult(
        combined,
        {
            "sources": [result.manifest for result in results],
            "years": sorted(int(year) for year in combined["year"].unique()),
            "rows": int(len(combined)),
            "frame_sha256": _stable_table_hash(combined),
        },
    )


__all__ = [
    "AdapterResult",
    "SourceSpec",
    "adapt_frame",
    "adapt_raw_frame",
    "combine_years",
    "load_csv",
    "select_physical_columns",
]
