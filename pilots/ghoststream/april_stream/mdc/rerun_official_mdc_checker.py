#!/usr/bin/env python3
"""Rerun the current official IAU MDC consistency checker exactly.

The script downloads the official checker archive, verifies the ZIP, reads the
committed GhostStream mean JSON, and runs both the distributed static binaries
and binaries freshly compiled from the distributed Fortran source. Both error
files must be empty in both runs. No candidate or mean value is modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import subprocess
import urllib.request
import zipfile
from pathlib import Path

CHECKER_URL = "https://ceresiaumdc.ta3.sk/downloads/source_programs/checking_program.zip"
USER_AGENT = "GhostStream-exact-MDC-checker-rerun/1.0 (+https://github.com/brandonlign/isef)"
MAX_BYTES = 10 * 1024 * 1024
ROOT = Path(__file__).resolve().parents[4]
MEAN_JSON = ROOT / "pilots/ghoststream/april_stream/mdc/GhostStream_April_mean_submission.json"


def download(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/zip,*/*",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        status = int(getattr(response, "status", response.getcode()))
        if status != 200:
            raise RuntimeError(f"unexpected HTTP status {status}")
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise RuntimeError("checker archive exceeded byte cap")
    if not data.startswith(b"PK"):
        raise RuntimeError("checker archive lacks ZIP signature")
    return data


def mean_record() -> dict[str, float | int]:
    payload = json.loads(MEAN_JSON.read_text())
    solutions = payload["data"]["solution"]
    if len(solutions) != 1:
        raise RuntimeError(f"expected one mean solution, found {len(solutions)}")
    solution = solutions[0]
    return {
        "iau": 0,
        "adno": 0,
        "LoS": float(solution["LoS"]),
        "Ra": float(solution["Ra"]),
        "De": float(solution["De"]),
        "Vg": float(solution["Vg"]),
        "q": float(solution["q"]),
        "e": float(solution["e"]),
        "peri": float(solution["peri"]),
        "node": float(solution["node"]),
        "inc": float(solution["inc"]),
        "N": int(solution["N"]),
    }


def write_inputs(directory: Path, record: dict[str, float | int]) -> None:
    line = (
        f"{record['iau']} {record['adno']} "
        f"{record['LoS']:.9f} {record['Ra']:.9f} {record['De']:.9f} "
        f"{record['Vg']:.9f} {record['q']:.9f} {record['e']:.9f} "
        f"{record['peri']:.9f} {record['node']:.9f} {record['inc']:.9f} {record['N']}\n"
    )
    (directory / "ghoststream_exact.db").write_text(line)
    (directory / "inparams.ele").write_text(
        "Input data file:\n"
        "ghoststream_exact.db\n"
        "Output orbital comparison file:\n"
        "check_orb_exact.d\n"
        "Output orbital error file:\n"
        "errors_orb_exact.inf\n"
        "Tolerance q [AU]:\n"
        "0.05\n"
        "Tolerance e:\n"
        "0.05\n"
        "Tolerance argument of perihelion [deg]:\n"
        "5.0\n"
        "Tolerance node [deg]:\n"
        "5.0\n"
        "Tolerance inclination [deg]:\n"
        "2.5\n"
    )
    (directory / "inparams.rad").write_text(
        "Input data file:\n"
        "ghoststream_exact.db\n"
        "Output geocentric comparison file:\n"
        "check_geo_exact.d\n"
        "Output geocentric error file:\n"
        "errors_geo_exact.inf\n"
        "Tolerance solar longitude [deg]:\n"
        "5.0\n"
        "Tolerance right ascension [deg]:\n"
        "5.0\n"
        "Tolerance declination [deg]:\n"
        "2.5\n"
        "Tolerance geocentric speed [km/s]:\n"
        "1.5\n"
        "Write debug file (0/1):\n"
        "0\n"
    )


def run_programs(directory: Path, elements: Path, radiants: Path) -> dict[str, object]:
    for output in (
        "check_orb_exact.d",
        "errors_orb_exact.inf",
        "check_geo_exact.d",
        "errors_geo_exact.inf",
        "debug.d",
    ):
        (directory / output).unlink(missing_ok=True)
    elements_result = subprocess.run(
        [str(elements.resolve())], cwd=directory, text=True, capture_output=True, check=True
    )
    radiants_result = subprocess.run(
        [str(radiants.resolve())], cwd=directory, text=True, capture_output=True, check=True
    )
    files = {}
    for name in (
        "ghoststream_exact.db",
        "inparams.ele",
        "inparams.rad",
        "check_orb_exact.d",
        "errors_orb_exact.inf",
        "check_geo_exact.d",
        "errors_geo_exact.inf",
    ):
        path = directory / name
        if not path.exists():
            raise RuntimeError(f"expected checker output missing: {path}")
        files[name] = {
            "byte_count": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "text": path.read_text(errors="replace"),
        }
    if files["errors_orb_exact.inf"]["byte_count"] != 0:
        raise RuntimeError(f"orbital checker errors:\n{files['errors_orb_exact.inf']['text']}")
    if files["errors_geo_exact.inf"]["byte_count"] != 0:
        raise RuntimeError(f"geocentric checker errors:\n{files['errors_geo_exact.inf']['text']}")
    return {
        "elements_stdout": elements_result.stdout,
        "elements_stderr": elements_result.stderr,
        "radiants_stdout": radiants_result.stdout,
        "radiants_stderr": radiants_result.stderr,
        "files": files,
        "zero_orbital_errors": True,
        "zero_geocentric_errors": True,
    }


def make_executable(path: Path) -> None:
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    archive = download(CHECKER_URL)
    archive_path = args.output_dir / "checking_program.zip"
    archive_path.write_bytes(archive)
    source_dir = args.output_dir / "official_source"
    with zipfile.ZipFile(archive_path) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"checker ZIP CRC failure: {bad}")
        zf.extractall(source_dir)
        members = [
            {
                "name": item.filename,
                "byte_count": item.file_size,
                "crc32": f"{item.CRC:08x}",
            }
            for item in zf.infolist()
        ]

    record = mean_record()

    static_dir = args.output_dir / "static_run"
    static_dir.mkdir()
    write_inputs(static_dir, record)
    static_elements = source_dir / "elements.exes"
    static_radiants = source_dir / "radiants.exes"
    make_executable(static_elements)
    make_executable(static_radiants)
    static_result = run_programs(static_dir, static_elements, static_radiants)

    compiled_dir = args.output_dir / "compiled_run"
    compiled_dir.mkdir()
    write_inputs(compiled_dir, record)
    compiler = shutil.which("gfortran")
    if compiler is None:
        raise RuntimeError("gfortran is unavailable")
    compiled_elements = compiled_dir / "elements_compiled"
    compiled_radiants = compiled_dir / "radiants_compiled"
    flags = [
        compiler,
        "-std=legacy",
        "-ffixed-line-length-none",
        "-fallow-argument-mismatch",
        "-O2",
    ]
    subprocess.run(flags + [str(source_dir / "elements.f"), "-o", str(compiled_elements)], check=True)
    subprocess.run(flags + [str(source_dir / "radiants.f"), "-o", str(compiled_radiants)], check=True)
    compiled_result = run_programs(compiled_dir, compiled_elements, compiled_radiants)

    # The official distributed executable and a fresh build of the exact source
    # must agree byte-for-byte on the scientific comparison outputs.
    for name in ("check_orb_exact.d", "check_geo_exact.d"):
        static_text = static_result["files"][name]["text"]
        compiled_text = compiled_result["files"][name]["text"]
        if static_text != compiled_text:
            raise RuntimeError(f"static/source-build disagreement in {name}")

    report = {
        "verdict": "PASS_ZERO_ERRORS_EXACT_COMMITTED_MEAN",
        "run_date_utc": "2026-08-01",
        "official_checker": {
            "url": CHECKER_URL,
            "archive_byte_count": len(archive),
            "archive_sha256": hashlib.sha256(archive).hexdigest(),
            "members": members,
        },
        "committed_mean_source": str(MEAN_JSON.relative_to(ROOT)),
        "exact_input_record": record,
        "tolerances": {
            "q_au": 0.05,
            "e": 0.05,
            "peri_deg": 5.0,
            "node_deg": 5.0,
            "inclination_deg": 2.5,
            "solar_longitude_deg": 5.0,
            "right_ascension_deg": 5.0,
            "declination_deg": 2.5,
            "geocentric_speed_km_s": 1.5,
        },
        "distributed_static_binary_run": static_result,
        "fresh_source_build_run": compiled_result,
        "static_and_fresh_build_outputs_identical": True,
        "claim_boundary": (
            "This validates internal consistency of the committed mean radiant, speed, "
            "solar longitude, and orbit only. It does not validate novelty, membership, "
            "significance, official recognition, or the external-replication claim."
        ),
    }
    report_path = args.output_dir / "exact_official_checker_rerun.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "verdict": report["verdict"],
        "archive_sha256": report["official_checker"]["archive_sha256"],
        "exact_input_record": record,
        "static_zero_errors": {
            "orbital": static_result["zero_orbital_errors"],
            "geocentric": static_result["zero_geocentric_errors"],
        },
        "fresh_build_zero_errors": {
            "orbital": compiled_result["zero_orbital_errors"],
            "geocentric": compiled_result["zero_geocentric_errors"],
        },
        "outputs_identical": True,
        "report": str(report_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
