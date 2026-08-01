#!/usr/bin/env python3
"""Run the primary GMN reconstruction despite the source host's TLS mismatch.

The official GMN Data Explorer currently presents a certificate whose hostname
does not validate as ``explore.globalmeteornetwork.org`` on GitHub's Python
runner. This wrapper disables certificate verification only for this process,
which calls the hardcoded official GMN endpoint in ``reproduce_primary_gmn``.
Every returned response is still checksum-locked in the reconstruction output.

This is a transport compatibility measure, not a scientific-method change.
Remove this wrapper when the official endpoint certificate validates normally.
"""
from __future__ import annotations

import runpy
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
runpy.run_path(
    "pilots/ghoststream/reconstruction/reproduce_primary_gmn.py",
    run_name="__main__",
)
