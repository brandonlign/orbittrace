# Official MDC consistency check

The draft 95-member mean record was tested with the radiant and orbital consistency programs distributed by the IAU Meteor Data Center.

Two executable forms were used:

1. the distributed Linux binaries; and
2. a fresh GNU Fortran build of the distributed `elements.f` and `radiants.f` source.

Both forms produced byte-identical comparison outputs and reported no inconsistencies in the submitted radiant, speed, solar longitude, or orbital elements.

## Record checked

| Quantity | Value |
|---|---:|
| Mean solar longitude | 37.149520° |
| RA | 247.169746° |
| Dec | −14.342743° |
| Vg | 37.617513 km/s |
| q | 0.080114 AU |
| e | 0.943593 |
| i | 24.370030° |
| ω | 333.636995° |
| Ω | 37.157321° |
| a | 1.420285 AU |
| N | 95 |

The semimajor axis is calculated from the submitted six-decimal q and e values:

`0.080114 / (1 - 0.943593) = 1.420284716... AU`.

The consistency programs check whether the submitted geocentric and heliocentric quantities agree under the MDC tolerances. They do not evaluate event membership, statistical significance, novelty, or whether the candidate should be accepted as a shower.

Exact hashes, executable provenance, and output comparisons are stored in `exact_official_checker_summary.json`.
