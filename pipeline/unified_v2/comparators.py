"""Literature comparator registry and scope boundaries for OrbitTrace."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComparatorSpec:
    name: str
    family: str
    status: str
    comparable_output: str
    source: str
    notes: str


def literature_comparator_registry() -> tuple[ComparatorSpec, ...]:
    """Return the methods worth tracking without overstating comparability."""

    return (
        ComparatorSpec(
            name="sugar_dbscan_uncertainty",
            family="DBSCAN / uncertainty clones",
            status="binding_archived",
            comparable_output="annual shower family catalogue",
            source="Sugar et al. 2017; archived PR1356 exact source and result",
            notes="Use the pinned source hash, pooled rows, fixed clone count, and equal temporal budget.",
        ),
        ComparatorSpec(
            name="hdbscan_geo_orbit_eom",
            family="HDBSCAN GEO/ORBIT EOM",
            status="binding_archived",
            comparable_output="annual shower family catalogue",
            source="Peña-Asensio & Ferrari 2025; archived PR1356 comparator adapter",
            notes="Keep GEO and ORBIT feature views, EOM/leaf choice, and Hungarian scoring explicit.",
        ),
        ComparatorSpec(
            name="d_criterion_edmond",
            family="orbital D-criterion grouping",
            status="binding_clean_room_adapter",
            comparable_output="orbital family catalogue",
            source="Rudawska, Matlovič, Tóth & Kornoš 2015 EDMOND identification",
            notes=(
                "Published D_SH=0.05 grouping, D_x=0.15 merging, and minimum-five rule; "
                "clean-room adapter, not the authors' original code."
            ),
        ),
        ComparatorSpec(
            name="cmor_3d_wavelet",
            family="3-D radiant wavelet",
            status="scope_check_required",
            comparable_output="radiant-time density cells",
            source="CMOR 3-D wavelet stream-identification literature",
            notes="Comparable only after fixing a common time/radiant grid and family projection rule.",
        ),
        ComparatorSpec(
            name="kde_false_positive_validation",
            family="KDE / orbital false-positive validation",
            status="validation_only",
            comparable_output="significance or false-positive calibration",
            source="Shober & Vaubaillon 2024",
            notes="Use as a null/false-positive audit, not as a direct candidate catalogue unless protocol is matched.",
        ),
    )


__all__ = ["ComparatorSpec", "literature_comparator_registry"]
