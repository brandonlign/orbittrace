#!/usr/bin/env python3
"""Diagnose the official GMN Datasette query transport without analysis changes."""
from __future__ import annotations

import importlib.util
import ssl
import urllib.parse
import urllib.request
from pathlib import Path

SCRIPT = Path("pilots/ghoststream/reconstruction/reproduce_primary_gmn.py")
spec = importlib.util.spec_from_file_location("ghoststream_reproduce_primary", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {SCRIPT}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

context = ssl._create_unverified_context()
queries = [
    ("scalar", "select 1 as probe_value"),
    ("meteor_scalar", "select count(*) as meteor_rows from meteor where shower_iau_no = -1"),
    ("membership", module.membership_sql()),
]

for name, sql in queries:
    url = module.API + "?" + urllib.parse.urlencode({"sql": sql, "_size": "max"})
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "GhostStream-query-probe/1.0",
            "Accept": "text/csv,*/*;q=0.1",
            "Accept-Encoding": "identity",
        },
    )
    print(f"=== {name} ===")
    print(f"URL_LENGTH={len(url)} SQL_LENGTH={len(sql)}")
    with urllib.request.urlopen(request, context=context, timeout=240) as response:
        payload = response.read()
        print(f"STATUS={getattr(response, 'status', 200)}")
        print(f"CONTENT_TYPE={response.headers.get('Content-Type', '')}")
        print(f"BYTES={len(payload)}")
        print(payload[:3000].decode("utf-8", errors="replace"))
