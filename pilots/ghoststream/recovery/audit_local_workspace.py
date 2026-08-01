#!/usr/bin/env python3
"""Read-only recovery audit for the missing GhostStream core analysis pipeline.

This tool is intended to run on Brandon's Mac, where the original project was
created. It does not modify Git, copy files, upload data, or open network
connections. It inventories likely source files, archives, notebooks, session
exports, Git worktrees/reflogs/dangling objects, and command-history matches.

Potential secret-bearing files are excluded from content inspection and are
reported only as redacted metadata when their names match the search terms.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import stat
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence

TERMS = (
    "ghoststream",
    "ghost stream",
    "antihelion",
    "specification curve",
    "geographic split",
    "cluster bootstrap",
    "year/night bootstrap",
    "source-preserving",
    "shifted-window",
    "orbit-null",
    "uncertainty clone",
    "gmn trajectory",
    "meteor stream",
    "april stream",
    "ghoststream-april-36.9",
)

NAME_TERMS = (
    "ghost",
    "stream",
    "antihelion",
    "bootstrap",
    "specification",
    "geographic",
    "activity_profile",
    "clone",
    "gmn",
    "meteor",
)

TEXT_SUFFIXES = {
    ".py", ".ipynb", ".r", ".R", ".jl", ".m", ".sh", ".zsh", ".bash",
    ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".ini",
    ".cfg", ".csv", ".tsv", ".log", ".out", ".err", ".html", ".xml",
    ".sql", ".js", ".ts", ".tsx", ".jsx", ".java", ".cpp", ".c", ".h",
}
ARCHIVE_SUFFIXES = {".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar"}
SECRET_NAME_PATTERNS = (
    re.compile(r"(^|[._-])(env|secret|secrets|credential|credentials|token|tokens|key|keys)([._-]|$)", re.I),
    re.compile(r"id_(rsa|ed25519|ecdsa)", re.I),
    re.compile(r"\.pem$", re.I),
    re.compile(r"\.p12$", re.I),
)
SKIP_DIR_NAMES = {
    ".cache", "node_modules", ".venv", "venv", "env", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "Library/Caches", ".Trash", "Applications",
}
MAX_TEXT_BYTES = 5 * 1024 * 1024
MAX_HASH_BYTES = 2 * 1024 * 1024 * 1024
DEFAULT_START = dt.datetime(2026, 7, 24, tzinfo=dt.timezone.utc)
DEFAULT_END = dt.datetime(2026, 8, 2, tzinfo=dt.timezone.utc)


@dataclasses.dataclass
class FileHit:
    path: str
    size_bytes: int
    modified_utc: str
    sha256: str | None
    name_match: bool
    content_terms: list[str]
    kind: str
    secret_name_redacted: bool
    source_root: str


@dataclasses.dataclass
class CommandResult:
    command: str
    returncode: int
    stdout: str
    stderr: str


def utc_iso(timestamp: float) -> str:
    return dt.datetime.fromtimestamp(timestamp, tz=dt.timezone.utc).isoformat()


def sha256_file(path: Path) -> str | None:
    try:
        size = path.stat().st_size
        if size > MAX_HASH_BYTES:
            return None
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except (OSError, PermissionError):
        return None


def is_secret_name(path: Path) -> bool:
    name = path.name
    return any(pattern.search(name) for pattern in SECRET_NAME_PATTERNS)


def is_skipped_dir(path: Path) -> bool:
    parts = path.parts
    for part in parts:
        if part in SKIP_DIR_NAMES:
            return True
    as_posix = path.as_posix()
    return any(token in as_posix for token in ("/Library/Caches/", "/.Trash/", "/node_modules/"))


def classify(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in ARCHIVE_SUFFIXES:
        return "archive"
    if suffix == ".ipynb":
        return "notebook"
    if suffix in {".py", ".r", ".jl", ".m", ".sh", ".zsh", ".bash"}:
        return "source"
    if suffix in TEXT_SUFFIXES:
        return "text"
    return "other"


def read_content_terms(path: Path) -> list[str]:
    if is_secret_name(path):
        return []
    if path.suffix not in TEXT_SUFFIXES:
        return []
    try:
        size = path.stat().st_size
        if size > MAX_TEXT_BYTES:
            return []
        text = path.read_text(errors="replace").lower()
    except (OSError, PermissionError, UnicodeError):
        return []
    return [term for term in TERMS if term in text]


def name_matches(path: Path) -> bool:
    lowered = path.name.lower()
    return any(term in lowered for term in NAME_TERMS)


def walk_root(root: Path, start: dt.datetime, end: dt.datetime) -> Iterable[FileHit]:
    if not root.exists():
        return
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            if current.is_symlink():
                continue
            if current.is_dir():
                if current != root and is_skipped_dir(current):
                    continue
                try:
                    children = list(current.iterdir())
                except (OSError, PermissionError):
                    continue
                stack.extend(children)
                continue
            if not current.is_file():
                continue
            info = current.stat()
        except (OSError, PermissionError):
            continue

        modified = dt.datetime.fromtimestamp(info.st_mtime, tz=dt.timezone.utc)
        in_window = start <= modified <= end
        nmatch = name_matches(current)
        content = read_content_terms(current) if (in_window or nmatch) else []
        archive = current.suffix.lower() in ARCHIVE_SUFFIXES
        if not (nmatch or content or (archive and in_window)):
            continue

        secret = is_secret_name(current)
        yield FileHit(
            path=str(current),
            size_bytes=info.st_size,
            modified_utc=modified.isoformat(),
            sha256=None if secret else sha256_file(current),
            name_match=nmatch,
            content_terms=content,
            kind=classify(current),
            secret_name_redacted=secret,
            source_root=str(root),
        )


def run(command: Sequence[str], cwd: Path | None = None, timeout: int = 60) -> CommandResult:
    try:
        result = subprocess.run(
            list(command), cwd=cwd, text=True, capture_output=True, timeout=timeout, check=False
        )
        return CommandResult(
            command=shlex.join(command),
            returncode=result.returncode,
            stdout=result.stdout[-2_000_000:],
            stderr=result.stderr[-500_000:],
        )
    except Exception as exc:
        return CommandResult(
            command=shlex.join(command),
            returncode=999,
            stdout="",
            stderr=f"{type(exc).__name__}: {exc}",
        )


def git_audit(repo: Path) -> list[CommandResult]:
    commands = [
        ["git", "status", "--short", "--untracked-files=all"],
        ["git", "branch", "--all", "--verbose", "--no-abbrev"],
        ["git", "worktree", "list", "--porcelain"],
        ["git", "reflog", "--all", "--date=iso", "--format=%H%x09%gd%x09%gs%x09%cd"],
        ["git", "fsck", "--full", "--no-reflogs", "--unreachable", "--lost-found"],
        ["git", "log", "--all", "--since=2026-07-20", "--until=2026-08-05", "--name-status", "--format=commit %H%nDate: %cI%nSubject: %s"],
        ["git", "stash", "list", "--date=local"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    results = [run(command, cwd=repo, timeout=180) for command in commands]

    # Inspect dangling commits and blobs only by metadata/text preview. Do not restore or modify refs.
    fsck = next((item for item in results if item.command.startswith("git fsck")), None)
    if fsck:
        object_ids = []
        for line in fsck.stdout.splitlines():
            match = re.search(r"(?:unreachable|dangling) (?:commit|blob) ([0-9a-f]{40,64})", line)
            if match:
                object_ids.append(match.group(1))
        for object_id in object_ids[:500]:
            object_type = run(["git", "cat-file", "-t", object_id], cwd=repo)
            if object_type.stdout.strip() == "commit":
                results.append(run(["git", "show", "--stat", "--oneline", "--decorate", object_id], cwd=repo))
            elif object_type.stdout.strip() == "blob":
                size = run(["git", "cat-file", "-s", object_id], cwd=repo)
                try:
                    size_int = int(size.stdout.strip())
                except ValueError:
                    continue
                if size_int <= MAX_TEXT_BYTES:
                    preview = run(["git", "cat-file", "-p", object_id], cwd=repo)
                    lowered = preview.stdout.lower()
                    if any(term in lowered for term in TERMS):
                        results.append(preview)
    return results


def history_audit(home: Path) -> list[dict[str, object]]:
    paths = [home / ".zsh_history", home / ".bash_history"]
    findings: list[dict[str, object]] = []
    for path in paths:
        if not path.is_file():
            continue
        try:
            lines = path.read_text(errors="replace").splitlines()
        except (OSError, PermissionError):
            continue
        matches = []
        for number, line in enumerate(lines, 1):
            lowered = line.lower()
            if any(term in lowered for term in TERMS + NAME_TERMS):
                # Redact common inline secret assignment patterns.
                redacted = re.sub(
                    r"(?i)(api[_-]?key|token|password|secret)=([^\s]+)", r"\1=[REDACTED]", line
                )
                matches.append({"line_number": number, "text": redacted[-4000:]})
        findings.append({"path": str(path), "match_count": len(matches), "matches": matches[-1000:]})
    return findings


def default_roots(home: Path, repo: Path) -> list[Path]:
    candidates = [
        repo,
        repo.parent,
        home / "Desktop",
        home / "Downloads",
        home / "Documents",
        home / "Library" / "Application Support" / "OpenCode",
        home / ".local" / "share" / "opencode",
        home / ".config" / "opencode",
        home / ".opencode",
    ]
    unique: list[Path] = []
    seen = set()
    for path in candidates:
        resolved = str(path.expanduser())
        if resolved not in seen:
            seen.add(resolved)
            unique.append(Path(resolved))
    return unique


def markdown_report(report: dict[str, object]) -> str:
    hits = report["file_hits"]
    source_hits = [item for item in hits if item["kind"] in {"source", "notebook"}]
    archives = [item for item in hits if item["kind"] == "archive"]
    lines = [
        "# GhostStream local recovery audit",
        "",
        f"Generated: {report['generated_utc']}",
        "",
        "## Summary",
        "",
        f"- File candidates: **{len(hits)}**",
        f"- Source/notebook candidates: **{len(source_hits)}**",
        f"- Archive candidates: **{len(archives)}**",
        f"- Git commands executed: **{len(report['git_results'])}**",
        "",
        "This report is an inventory only. A match does not prove that a file is the original pipeline.",
        "",
        "## Highest-priority source/notebook candidates",
        "",
        "| Path | Modified UTC | Bytes | Terms | SHA-256 |",
        "|---|---|---:|---|---|",
    ]
    for item in source_hits[:200]:
        terms = ", ".join(item["content_terms"])
        digest = item["sha256"] or "not hashed"
        lines.append(
            f"| `{item['path']}` | {item['modified_utc']} | {item['size_bytes']} | {terms} | `{digest}` |"
        )
    lines.extend(["", "## Archive candidates", "", "| Path | Modified UTC | Bytes | SHA-256 |", "|---|---|---:|---|"])
    for item in archives[:200]:
        digest = item["sha256"] or "not hashed"
        lines.append(f"| `{item['path']}` | {item['modified_utc']} | {item['size_bytes']} | `{digest}` |")
    lines.extend([
        "",
        "## Next manual review",
        "",
        "1. Preserve the full report directory before opening candidates.",
        "2. Review source/notebook candidates in modification-time order.",
        "3. Inspect Git reflog, worktrees, stashes, and dangling commits/blobs recorded in `git_results.json`.",
        "4. Hash and copy promising directories to a separate recovery location before editing.",
        "5. Never commit credentials, `.env` files, tokens, or personal session data.",
        "6. Compare recovered code chronology and output files against the preserved reports before trusting it.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.home() / "Desktop" / "isef",
        help="Local isef repository path (default: ~/Desktop/isef)",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--root", type=Path, action="append", default=[], help="Additional search root; repeatable")
    parser.add_argument("--start", default=DEFAULT_START.isoformat(), help="UTC ISO timestamp")
    parser.add_argument("--end", default=DEFAULT_END.isoformat(), help="UTC ISO timestamp")
    args = parser.parse_args()

    repo = args.repo.expanduser().resolve()
    output = args.output_dir.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    start = dt.datetime.fromisoformat(args.start.replace("Z", "+00:00"))
    end = dt.datetime.fromisoformat(args.end.replace("Z", "+00:00"))
    if start.tzinfo is None or end.tzinfo is None:
        raise SystemExit("--start and --end must include a timezone")
    home = Path.home().resolve()

    roots = default_roots(home, repo) + [path.expanduser().resolve() for path in args.root]
    unique_roots = []
    seen = set()
    for root in roots:
        key = str(root)
        if key not in seen:
            seen.add(key)
            unique_roots.append(root)

    file_hits: list[FileHit] = []
    for root in unique_roots:
        file_hits.extend(walk_root(root, start, end) or [])

    # Deduplicate nested-root hits by absolute path, preferring richer term matches.
    best: dict[str, FileHit] = {}
    for hit in file_hits:
        existing = best.get(hit.path)
        if existing is None or len(hit.content_terms) > len(existing.content_terms):
            best[hit.path] = hit
    ordered = sorted(
        best.values(),
        key=lambda item: (
            item.kind not in {"source", "notebook"},
            -len(item.content_terms),
            item.modified_utc,
            item.path,
        ),
    )

    git_results = git_audit(repo) if (repo / ".git").exists() else []
    report = {
        "generated_utc": dt.datetime.now(tz=dt.timezone.utc).isoformat(),
        "host": os.uname().nodename if hasattr(os, "uname") else "unknown",
        "repo": str(repo),
        "search_window": {"start": start.isoformat(), "end": end.isoformat()},
        "roots": [str(path) for path in unique_roots],
        "terms": list(TERMS),
        "file_hits": [dataclasses.asdict(item) for item in ordered],
        "git_results": [dataclasses.asdict(item) for item in git_results],
        "history_results": history_audit(home),
        "privacy": {
            "network_used": False,
            "files_modified": False,
            "files_copied": False,
            "secret_named_files_content_inspected": False,
            "note": "Review the report before sharing; shell commands and paths may contain personal information.",
        },
    }
    (output / "ghoststream_local_recovery_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    (output / "GHOSTSTREAM_LOCAL_RECOVERY_AUDIT.md").write_text(markdown_report(report))
    (output / "git_results.json").write_text(
        json.dumps(report["git_results"], indent=2) + "\n"
    )

    print(
        json.dumps(
            {
                "verdict": "RECOVERY_INVENTORY_COMPLETE",
                "repo_exists": repo.exists(),
                "git_repo_detected": (repo / ".git").exists(),
                "file_candidates": len(ordered),
                "source_or_notebook_candidates": sum(
                    item.kind in {"source", "notebook"} for item in ordered
                ),
                "archive_candidates": sum(item.kind == "archive" for item in ordered),
                "output_dir": str(output),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
