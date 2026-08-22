"""Unified recurrent hierarchy detector, version 1.

This experimental lane combines the existing recurrent-EOM parent extraction
with compact leaf descendants from the same density hierarchy.  It is kept
separate from the frozen paper snapshots and governance evidence.
"""

from .method import UnifiedConfig, cluster_hierarchy

__all__ = ["UnifiedConfig", "cluster_hierarchy"]
