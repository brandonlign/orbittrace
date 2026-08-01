#!/usr/bin/env python3
"""Refresh the GhostStream duplicate-shower audit against the live IAU MDC JSON.

The candidate and all thresholds are fixed in this source file before the live
catalogue is downloaded. The script does not alter the candidate solution.
It reports both complete-orbit hard matches and orbit-incomplete radiant/time
near matches so missing catalogue elements cannot silently count as novelty.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
import urllib.request
from pathlib import Path
from typing import Any

URL = "https://ceresiaumdc.ta3.sk/downloads/lists_shw_data/streamfulldata.json"
USER_AGENT = "GhostStream-live-MDC-refresh/1.0 (+https://github.com/brandonlign/isef)"
MAX_BYTES = 30 * 1024 * 1024

# Frozen GhostStream candidate.
EPOCH = 36.901963
ACTIVITY_HALF_WIDTH = 4.0
CENTER_SLR = -149.3763247 % 360.0
CENTER_BETA = 7.3230377
CENTER_VG = 37.641692
DRIFT_SLR = -0.1029483
DRIFT_BETA = -0.0230546
DRIFT_VG = -0.0293492
CANDIDATE_ORBIT = {
    "q": 0.079202,
    "e": 0.946296,
    "inc": 24.709376,
    "peri": 333.493819,
    "node": 37.937477,
}

# Conservative duplicate screen, fixed before retrieval.
HARD_MAX_RADIANT_SEP_DEG = 5.0
HARD_MAX_SPEED_DIFF_KMS = 5.0
HARD_MAX_DSH = 0.15
NEAR_MAX_RADIANT_SEP_DEG = 5.0
NEAR_MAX_SPEED_DIFF_KMS = 5.0


def finite(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def wrap360(x: float) -> float:
    return x % 360.0


def circular_delta(a: float, b: float) -> float:
    return (a - b + 180.0) % 360.0 - 180.0


def interval_segments(start: float, end: float) -> list[tuple[float, float]]:
    start, end = wrap360(start), wrap360(end)
    if start <= end:
        return [(start, end)]
    return [(start, 360.0), (0.0, end)]


def intervals_overlap(a0: float, a1: float, b0: float, b1: float) -> bool:
    return any(max(x0, y0) <= min(x1, y1) for x0, x1 in interval_segments(a0, a1) for y0, y1 in interval_segments(b0, b1))


def activity_compatible(solution: dict[str, Any]) -> tuple[bool, str]:
    begin = finite(solution.get("LoSb"))
    end = finite(solution.get("LoSe"))
    mean = finite(solution.get("LoS"))
    candidate_begin = EPOCH - ACTIVITY_HALF_WIDTH
    candidate_end = EPOCH + ACTIVITY_HALF_WIDTH
    if begin is not None and end is not None:
        return intervals_overlap(begin, end, candidate_begin, candidate_end), "published_interval"
    if mean is not None:
        # With no published bounds, require the mean epoch to lie within two
        # candidate half-widths. This is deliberately more permissive than the
        # candidate's own membership interval.
        return abs(circular_delta(mean, EPOCH)) <= 2.0 * ACTIVITY_HALF_WIDTH, "mean_epoch_fallback"
    return False, "missing_epoch"


def angular_separation(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    l1, b1, l2, b2 = map(math.radians, (lon1, lat1, lon2, lat2))
    cosine = math.sin(b1) * math.sin(b2) + math.cos(b1) * math.cos(b2) * math.cos(l1 - l2)
    return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))


def candidate_at(sol: float) -> tuple[float, float, float]:
    delta = circular_delta(sol, EPOCH)
    return (
        wrap360(CENTER_SLR + DRIFT_SLR * delta),
        CENTER_BETA + DRIFT_BETA * delta,
        CENTER_VG + DRIFT_VG * delta,
    )


def d_sh(orbit: dict[str, float]) -> float:
    q1, e1 = CANDIDATE_ORBIT["q"], CANDIDATE_ORBIT["e"]
    i1, w1, n1 = (math.radians(CANDIDATE_ORBIT[k]) for k in ("inc", "peri", "node"))
    q2, e2 = orbit["q"], orbit["e"]
    i2, w2, n2 = (math.radians(orbit[k]) for k in ("inc", "peri", "node"))
    cos_i = math.cos(i1) * math.cos(i2) + math.sin(i1) * math.sin(i2) * math.cos(n1 - n2)
    I = math.acos(max(-1.0, min(1.0, cos_i)))
    denom = math.cos(I / 2.0)
    arg = math.cos((i1 + i2) / 2.0) * math.sin((n1 - n2) / 2.0) / denom if abs(denom) > 1e-15 else 0.0
    Pi = w1 - w2 + 2.0 * math.asin(max(-1.0, min(1.0, arg)))
    return math.sqrt(
        (e1 - e2) ** 2
        + (q1 - q2) ** 2
        + (2.0 * math.sin(I / 2.0)) ** 2
        + (((e1 + e2) / 2.0) * 2.0 * math.sin(Pi / 2.0)) ** 2
    )


def fetch() -> bytes:
    req = urllib.request.Request(URL, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Accept-Encoding": "identity",
    })
    with urllib.request.urlopen(req, timeout=90) as response:
        if int(getattr(response, "status", response.getcode())) != 200:
            raise RuntimeError(f"unexpected HTTP status {response.status}")
        declared = response.headers.get("Content-Length")
        if declared and int(declared) > MAX_BYTES:
            raise RuntimeError(f"declared response too large: {declared}")
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise RuntimeError("response exceeded byte cap")
    return data


def flatten(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for shower in payload.get("data", []):
        if not isinstance(shower, dict):
            continue
        for solution in shower.get("solution", []) or []:
            if not isinstance(solution, dict):
                continue
            row = {
                "IAUNo": shower.get("IAUNo"),
                "Code": shower.get("Code"),
                "Name": shower.get("Name"),
                "ProvName": shower.get("ProvName"),
                "shower_status": shower.get("s"),
                **solution,
            }
            rows.append(row)
    return rows


def evaluate(row: dict[str, Any]) -> dict[str, Any]:
    sol = finite(row.get("LoS"))
    slr = finite(row.get("S_LoR"))
    beta = finite(row.get("LaR"))
    vg = finite(row.get("Vg"))
    compatible, activity_basis = activity_compatible(row)
    radiant_sep = speed_diff = None
    if sol is not None and slr is not None and beta is not None:
        pred_slr, pred_beta, pred_vg = candidate_at(sol)
        radiant_sep = angular_separation(slr, beta, pred_slr, pred_beta)
        if vg is not None:
            speed_diff = abs(vg - pred_vg)
    orbit_values = {key: finite(row.get(key)) for key in ("q", "e", "inc", "peri", "node")}
    orbit_complete = all(value is not None for value in orbit_values.values())
    dsh = d_sh({key: float(value) for key, value in orbit_values.items()}) if orbit_complete else None
    radiant_speed_match = (
        compatible
        and radiant_sep is not None and radiant_sep <= NEAR_MAX_RADIANT_SEP_DEG
        and speed_diff is not None and speed_diff <= NEAR_MAX_SPEED_DIFF_KMS
    )
    hard_match = bool(radiant_speed_match and dsh is not None and dsh <= HARD_MAX_DSH)
    # Ranking score is descriptive only and never determines the hard verdict.
    epoch_delta = abs(circular_delta(sol, EPOCH)) if sol is not None else None
    composite = None
    if epoch_delta is not None and radiant_sep is not None and speed_diff is not None:
        composite = math.sqrt((epoch_delta / 8.0) ** 2 + (radiant_sep / 5.0) ** 2 + (speed_diff / 5.0) ** 2)
    return {
        "IAUNo": row.get("IAUNo"),
        "Code": row.get("Code"),
        "Name": row.get("Name"),
        "ProvName": row.get("ProvName"),
        "AdNo": row.get("AdNo"),
        "status": row.get("s", row.get("shower_status")),
        "LoSb": finite(row.get("LoSb")),
        "LoSe": finite(row.get("LoSe")),
        "LoS": sol,
        "S_LoR": slr,
        "LaR": beta,
        "Vg": vg,
        "activity_compatible": compatible,
        "activity_compatibility_basis": activity_basis,
        "mean_epoch_delta_deg": epoch_delta,
        "drifted_radiant_separation_deg": radiant_sep,
        "drifted_speed_difference_km_s": speed_diff,
        "orbit_complete": orbit_complete,
        "d_sh": dsh,
        "radiant_speed_activity_match": radiant_speed_match,
        "hard_duplicate_match": hard_match,
        "descriptive_composite_score": composite,
        "q": orbit_values["q"],
        "e": orbit_values["e"],
        "inc": orbit_values["inc"],
        "peri": orbit_values["peri"],
        "node": orbit_values["node"],
    }


def serializable_top(rows: list[dict[str, Any]], key: str, n: int = 20) -> list[dict[str, Any]]:
    return sorted((r for r in rows if r.get(key) is not None), key=lambda r: float(r[key]))[:n]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    raw = fetch()
    payload = json.loads(raw)
    if payload.get("source") != "IAU Meteor Data Center":
        raise RuntimeError("unexpected catalogue source")
    if not isinstance(payload.get("data"), list):
        raise RuntimeError("catalogue data is not a list")
    if payload.get("count") != len(payload["data"]):
        raise RuntimeError(f"declared shower count {payload.get('count')} != parsed {len(payload['data'])}")

    flattened = flatten(payload)
    evaluated = [evaluate(row) for row in flattened]
    hard = [row for row in evaluated if row["hard_duplicate_match"]]
    near = [row for row in evaluated if row["radiant_speed_activity_match"]]
    incomplete_near = [row for row in near if not row["orbit_complete"]]
    nearest_orbits = serializable_top(evaluated, "d_sh", 25)
    nearest_composite = serializable_top(evaluated, "descriptive_composite_score", 25)

    report = {
        "verdict": "NO_CURRENT_IAU_MDC_HARD_DUPLICATE" if not hard else "CURRENT_IAU_MDC_HARD_DUPLICATE_FOUND",
        "catalogue": {
            "url": URL,
            "version": payload.get("version"),
            "declared_shower_records": payload.get("count"),
            "parsed_shower_records": len(payload["data"]),
            "parsed_solutions": len(flattened),
            "byte_count": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        },
        "candidate": {
            "internal_id": "GhostStream-April-36.9",
            "epoch_solar_longitude_deg": EPOCH,
            "activity_interval_deg": [EPOCH - ACTIVITY_HALF_WIDTH, EPOCH + ACTIVITY_HALF_WIDTH],
            "sun_centered_ecliptic_longitude_deg": CENTER_SLR,
            "ecliptic_latitude_deg": CENTER_BETA,
            "geocentric_speed_km_s": CENTER_VG,
            "orbit": CANDIDATE_ORBIT,
        },
        "fixed_duplicate_rules": {
            "activity": "published interval overlaps candidate ±4°, or mean epoch within ±8° when bounds are absent",
            "maximum_drifted_radiant_separation_deg": HARD_MAX_RADIANT_SEP_DEG,
            "maximum_drifted_speed_difference_km_s": HARD_MAX_SPEED_DIFF_KMS,
            "maximum_southworth_hawkins_d": HARD_MAX_DSH,
            "hard_match_requires_complete_orbit": True,
        },
        "hard_duplicate_matches": hard,
        "hard_duplicate_match_count": len(hard),
        "radiant_speed_activity_match_count": len(near),
        "orbit_incomplete_near_match_count": len(incomplete_near),
        "radiant_speed_activity_matches": near,
        "nearest_complete_orbits": nearest_orbits,
        "nearest_descriptive_composite": nearest_composite,
        "previous_audit_reference": {
            "previous_parsed_solutions": 2174,
            "previous_hard_matches": 0,
            "previous_nearest_complete_orbit_code": "NOP",
            "previous_nearest_complete_orbit_d_approx": 0.235,
        },
    }
    (args.output_dir / "live_mdc_novelty_refresh.json").write_text(json.dumps(report, indent=2) + "\n")
    write_csv(args.output_dir / "live_mdc_nearest_complete_orbits.csv", nearest_orbits)
    write_csv(args.output_dir / "live_mdc_radiant_speed_activity_matches.csv", near)
    print(json.dumps({
        "verdict": report["verdict"],
        "catalogue_version": report["catalogue"]["version"],
        "showers": report["catalogue"]["parsed_shower_records"],
        "solutions": report["catalogue"]["parsed_solutions"],
        "sha256": report["catalogue"]["sha256"],
        "hard_duplicate_matches": len(hard),
        "radiant_speed_activity_matches": len(near),
        "orbit_incomplete_near_matches": len(incomplete_near),
        "nearest_complete_orbit": nearest_orbits[0] if nearest_orbits else None,
        "report": str(args.output_dir / "live_mdc_novelty_refresh.json"),
    }, indent=2))
    return 2 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
