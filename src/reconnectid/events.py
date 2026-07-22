"""Published EDR event-list acquisition, parsing, annotation, and selection."""
from __future__ import annotations

from io import StringIO
from pathlib import Path
import hashlib
import logging
import re
import requests
import pandas as pd

LOGGER = logging.getLogger(__name__)
ZENODO_API = "https://zenodo.org/api/records/{record}"
CATALOG_FILE = "EDR_list_MMS.txt"
ANCHORS = {
    ("2015-09-08", "11:01:20.370", "MMS3"): "large-guide-field anchor",
    ("2015-12-14", "01:17:39.650", "MMS1"): "intermediate-guide-field anchor",
}
CANONICAL = ("2015-10-16", "13:07:02.200", "MMS2")


def download_event_list(record: int, destination: Path, timeout: float = 30) -> Path:
    """Download the immutable Zenodo event catalog, using a local cache on reruns."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size > 0:
        LOGGER.info("Using cached event catalog %s", destination)
        return destination
    meta = requests.get(ZENODO_API.format(record=record), timeout=timeout)
    meta.raise_for_status()
    matches = [x for x in meta.json().get("files", []) if x.get("key") == CATALOG_FILE]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one {CATALOG_FILE}; found {len(matches)}")
    url = matches[0]["links"].get("content") or matches[0]["links"].get("self")
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    expected = matches[0].get("checksum", "")
    if expected.startswith("md5:"):
        actual = hashlib.md5(response.content).hexdigest()  # nosec: integrity check required by Zenodo metadata
        if actual != expected.removeprefix("md5:"):
            raise IOError("Zenodo event-list checksum mismatch")
    tmp = destination.with_suffix(destination.suffix + ".part")
    tmp.write_bytes(response.content)
    tmp.replace(destination)
    return destination


def parse_event_list(path: Path) -> pd.DataFrame:
    """Parse Zenodo's tab-separated catalog without changing reference strings."""
    text = path.read_text(encoding="utf-8-sig")
    rows: list[dict[str, object]] = []
    for line in StringIO(text):
        line = line.strip()
        if not line or line.lower().startswith("date"):
            continue
        parts = re.split(r"\s+", line, maxsplit=3)
        if len(parts) != 4 or not re.fullmatch(r"MMS[1-4]", parts[2], re.I):
            raise ValueError(f"Unparseable event-list line: {line!r}")
        date, time, sc, reference = parts
        timestamp = pd.Timestamp(f"{date}T{time}Z")
        key = (date, time, sc.upper())
        rows.append({
            "date": date, "time": time, "spacecraft": sc.upper(),
            "reference_paper": reference, "timestamp": timestamp,
            "literature_label": ANCHORS.get(key, ""),
            "is_guide_field_study": key in ANCHORS,
            "is_canonical": key == CANONICAL,
        })
    frame = pd.DataFrame(rows).sort_values("timestamp", kind="stable").reset_index(drop=True)
    if frame.empty or frame["timestamp"].duplicated().any():
        raise ValueError("Catalog is empty or contains duplicate timestamps")
    frame.insert(0, "event_id", [f"EDR{i:03d}" for i in range(1, len(frame) + 1)])
    for key in (*ANCHORS, CANONICAL):
        found = ((frame.date == key[0]) & (frame.time == key[1]) & (frame.spacecraft == key[2])).sum()
        if found != 1:
            raise ValueError(f"Required event {key} occurs {found} times")
    return frame


def select_events(events: pd.DataFrame, maximum: int, seed: int) -> pd.DataFrame:
    """Deterministically spread selection across time, spacecraft, and references.

    A seeded farthest-point design is used over normalized time plus categorical
    spacecraft/reference novelty. Required anchors are inserted first.
    """
    if maximum < 3:
        raise ValueError("maximum must accommodate the three required events")
    if len(events) <= maximum:
        return events.copy().reset_index(drop=True)
    required_mask = events["is_guide_field_study"] | events["is_canonical"]
    chosen = list(events.index[required_mask])
    candidates = [i for i in events.index if i not in chosen]
    time_ns = events.timestamp.astype("int64").to_numpy(dtype=float)
    t = (time_ns - time_ns.min()) / max(time_ns.max() - time_ns.min(), 1)
    rng = __import__("numpy").random.default_rng(seed)
    jitter = {i: float(rng.uniform(0, 1e-10)) for i in candidates}

    def distance(i: int, j: int) -> float:
        return abs(t[i] - t[j]) + 0.35 * (events.spacecraft[i] != events.spacecraft[j]) + 0.45 * (
            events.reference_paper[i] != events.reference_paper[j]
        )

    while len(chosen) < maximum:
        scores = []
        for i in candidates:
            novelty = min(distance(i, j) for j in chosen)
            ref_count = sum(events.reference_paper[j] == events.reference_paper[i] for j in chosen)
            sc_count = sum(events.spacecraft[j] == events.spacecraft[i] for j in chosen)
            scores.append((novelty - 0.025 * ref_count - 0.01 * sc_count + jitter[i], i))
        _, picked = max(scores)
        chosen.append(picked)
        candidates.remove(picked)
    result = events.loc[chosen].sort_values("timestamp", kind="stable").reset_index(drop=True)
    result["selection_method"] = "required+seeded_farthest_stratification"
    return result

