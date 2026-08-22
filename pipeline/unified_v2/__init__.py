"""Exploratory OrbitTrace method v2.

The v2 lane is deliberately separate from ``unified_v1``.  It adds a
multi-year recurrent tree objective and a cross-fitted, uncertainty-aware
membership expansion, but it does not change the frozen v1 evidence.
"""

from .config import V2Config
from .crossfit_membership import expand_candidate
from .features import periodic_physical6_from_raw
from .recurrent_tree import fit_recurrent_hierarchy

__all__ = [
    "V2Config",
    "expand_candidate",
    "fit_recurrent_hierarchy",
    "periodic_physical6_from_raw",
]
