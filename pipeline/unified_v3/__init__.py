"""Unified v3 multiscale recurrence detector."""

from .config import V3Config
from .method import build_multiscale_catalogue, generate_multiscale_candidates

__all__ = ["V3Config", "build_multiscale_catalogue", "generate_multiscale_candidates"]
