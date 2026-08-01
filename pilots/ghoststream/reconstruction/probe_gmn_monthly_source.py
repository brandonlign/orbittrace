#!/usr/bin/env python3
"""Probe the official GMN April monthly catalogue and parser schema."""
from __future__ import annotations

import hashlib
import json

from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_trajectory_reader

content = dd.get_monthly_file_content_by_date("2019-04")
raw = content.encode("utf-8") if isinstance(content, str) else bytes(content)
frame = meteor_trajectory_reader.read_data(content, output_camel_case=True)
frame = frame.reset_index()

print(json.dumps({
    "month": "2019-04",
    "raw_bytes": len(raw),
    "raw_sha256": hashlib.sha256(raw).hexdigest(),
    "rows": int(len(frame)),
    "columns": list(frame.columns),
    "dtypes": {str(key): str(value) for key, value in frame.dtypes.items()},
    "first_row": {
        str(key): (value.isoformat() if hasattr(value, "isoformat") else str(value))
        for key, value in frame.iloc[0].to_dict().items()
    } if len(frame) else None,
}, indent=2, sort_keys=True))
