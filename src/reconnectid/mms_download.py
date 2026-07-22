"""Cached public MMS burst-mode acquisition through PySPEDAS."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
import json
import logging
import os
import time
import numpy as np
import pandas as pd

from .config import PilotConfig
from .variable_resolver import PRODUCT_REQUESTS, resolve_variable

LOGGER = logging.getLogger(__name__)


@dataclass
class ProductRecord:
    product: str
    success: bool
    variable: str = ""
    native_cadence_seconds: float = float("nan")
    valid_fraction: float = 0.0
    cache_path: str = ""
    failure_reason: str = ""


def _event_paths(root: Path, event_id: str) -> tuple[Path, Path]:
    return root / "data/cache/events" / f"{event_id}.npz", root / "data/cache/events" / f"{event_id}.json"


def _extract_tplot(name: str) -> tuple[np.ndarray, np.ndarray]:
    # PySPEDAS 2.x owns its tplot registry; 1.x used the external pytplot one.
    try:
        from pyspedas import get_data
    except ImportError:  # pragma: no cover - compatibility with older supported releases
        from pytplot import get_data
    data = get_data(name)
    if data is None:
        raise RuntimeError(f"pytplot variable {name!r} has no data")
    if hasattr(data, "times"):
        times, values = np.asarray(data.times, float), np.asarray(data.y, float)
    else:
        times, values = np.asarray(data[0], float), np.asarray(data[1], float)
    if len(times) != values.shape[0] or len(times) < 2:
        raise ValueError(f"Invalid shape for {name}: time={times.shape}, data={values.shape}")
    return times, values


def _load_instruments(trange: list[str], probe: str) -> None:
    """Load required public L2 burst products, allowing PySPEDAS to cache CDFs."""
    import pyspedas
    kwargs = dict(trange=trange, probe=probe, data_rate="brst", level="l2", time_clip=True)
    pyspedas.projects.mms.fgm(**kwargs)
    pyspedas.projects.mms.edp(datatype="dce", **kwargs)
    pyspedas.projects.mms.fpi(datatype="des-moms", **kwargs)
    pyspedas.projects.mms.fpi(datatype="dis-moms", **kwargs)


def download_event(event: pd.Series, cfg: PilotConfig, root: Path, force: bool = False) -> dict[str, Any]:
    """Download/resolve one event and checkpoint its arrays and explicit manifest."""
    npz_path, json_path = _event_paths(root, str(event.event_id))
    npz_path.parent.mkdir(parents=True, exist_ok=True)
    if npz_path.exists() and json_path.exists() and not force:
        cached_manifest = json.loads(json_path.read_text())
        if cached_manifest.get("success") is True:
            return cached_manifest
        LOGGER.info("Retrying previously failed checkpoint for %s", event.event_id)
    os.environ.setdefault("SPEDAS_DATA_DIR", str(root / "data/raw"))
    timestamp = pd.Timestamp(event.timestamp)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize("UTC")
    start = timestamp - pd.Timedelta(seconds=cfg.event_window_seconds)
    end = timestamp + pd.Timedelta(seconds=cfg.event_window_seconds)
    trange = [start.strftime("%Y-%m-%d/%H:%M:%S.%f"), end.strftime("%Y-%m-%d/%H:%M:%S.%f")]
    records: list[ProductRecord] = []
    arrays: dict[str, np.ndarray] = {}
    try:
        try:
            from pyspedas import del_data, tplot_names
        except ImportError:  # pragma: no cover
            from pytplot import del_data, tplot_names
        del_data("*")
        _load_instruments(trange, str(event.spacecraft)[-1])
        try:
            names = list(tplot_names(quiet=True))
        except TypeError:  # pragma: no cover - older external pytplot API
            names = list(tplot_names())
        for product, factory in PRODUCT_REQUESTS.items():
            try:
                variable = resolve_variable(names, factory(str(event.spacecraft).lower()))
                times, values = _extract_tplot(variable)
                finite = np.isfinite(times) & np.all(np.isfinite(values.reshape(len(times), -1)), axis=1)
                cadence = float(np.nanmedian(np.diff(times)))
                arrays[f"{product}_time"] = times
                arrays[f"{product}_values"] = values
                records.append(ProductRecord(product, True, variable, cadence, float(finite.mean()), str(npz_path)))
            except Exception as exc:
                LOGGER.exception("Failed resolving %s for %s", product, event.event_id)
                records.append(ProductRecord(product, False, failure_reason=f"{type(exc).__name__}: {exc}"))
    except Exception as exc:
        LOGGER.exception("MMS acquisition failed for %s", event.event_id)
        records = [ProductRecord(p, False, failure_reason=f"{type(exc).__name__}: {exc}") for p in PRODUCT_REQUESTS]
    success = len(records) == len(PRODUCT_REQUESTS) and all(r.success for r in records)
    if arrays:
        temp = npz_path.with_suffix(".npz.part")
        with temp.open("wb") as handle:
            np.savez_compressed(handle, **arrays)
        temp.replace(npz_path)
    manifest = {
        "event_id": str(event.event_id), "timestamp": timestamp.isoformat(),
        "spacecraft": str(event.spacecraft), "success": success,
        "products": [asdict(r) for r in records],
        "failure_reason": "" if success else "; ".join(r.failure_reason for r in records if not r.success),
        "cache_path": str(npz_path) if arrays else "", "attempted_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
    }
    tmp_json = json_path.with_suffix(".json.part")
    tmp_json.write_text(json.dumps(manifest, indent=2, allow_nan=True))
    tmp_json.replace(json_path)
    return manifest


def download_events(events: pd.DataFrame, cfg: PilotConfig, root: Path, force: bool = False) -> pd.DataFrame:
    rows = []
    for _, event in events.iterrows():
        manifest = download_event(event, cfg, root, force=force)
        flat = {k: v for k, v in manifest.items() if k != "products"}
        flat["resolved_variables"] = json.dumps({p["product"]: p["variable"] for p in manifest["products"]})
        flat["native_cadences"] = json.dumps({p["product"]: p["native_cadence_seconds"] for p in manifest["products"]})
        flat["valid_fractions"] = json.dumps({p["product"]: p["valid_fraction"] for p in manifest["products"]})
        rows.append(flat)
        time.sleep(0.1)
    result = pd.DataFrame(rows)
    destination = root / "data/event_metadata/download_manifest.csv"
    result.to_csv(destination, index=False)
    return result
