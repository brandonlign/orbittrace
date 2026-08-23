"""Literature comparator registry and scope for OrbitTrace."""
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
    """Return comparator methods with their source and scope details."""

    return (
        ComparatorSpec(
            name="sugar_dbscan_uncertainty",
            family="DBSCAN / uncertainty clones",
            status="archived_reference",
            comparable_output="annual shower family catalogue",
            source="Sugar et al. 2017; archived comparator result",
            notes="Use the pinned source hash, pooled rows, fixed clone count, and equal temporal budget.",
        ),
        ComparatorSpec(
            name="hdbscan_geo_orbit_eom",
            family="HDBSCAN GEO/ORBIT EOM",
            status="archived_reference",
            comparable_output="annual shower family catalogue",
            source="Peña-Asensio & Ferrari 2025; archived comparator adapter and result",
            notes="Keep GEO and ORBIT feature views, EOM/leaf choice, and Hungarian scoring explicit.",
        ),
        ComparatorSpec(
            name="d_criterion_edmond",
            family="orbital D-criterion grouping",
            status="independent_implementation",
            comparable_output="orbital family catalogue",
            source="Rudawska, Matlovič, Tóth & Kornoš 2015 EDMOND identification",
            notes=(
                "Published D_SH=0.05 grouping, D_x=0.15 merging, and minimum-five rule; "
                "independent implementation, not the authors' original code."
            ),
        ),
        ComparatorSpec(
            name="cmor_3d_wavelet",
            family="3-D radiant wavelet",
            status="requires_protocol_alignment",
            comparable_output="radiant-time density cells",
            source="CMOR 3-D wavelet stream-identification literature",
            notes="Align the time/radiant grid and family projection rule before comparing results.",
        ),
        ComparatorSpec(
            name="kde_false_positive_validation",
            family="KDE / orbital false-positive validation",
            status="validation_only",
            comparable_output="significance or false-positive calibration",
            source="Shober & Vaubaillon 2024",
            notes="Use for null and false-positive calibration; a direct catalogue comparison requires a matched protocol.",
        ),
    )


__all__ = ["ComparatorSpec", "literature_comparator_registry"]
