# GhostStream absolute-flux data requirements

## Decision

A physical meteor flux or ZHR cannot be reconstructed from the public GMN trajectory catalogue alone.

The public trajectory table contains multi-station Level 3 products. The RMS flux pipeline instead operates on station-night Level 2 products so that it can determine:

- every single-station meteor associated with the shower;
- clear observing intervals;
- camera astrometry and photometry;
- limiting meteor magnitude;
- radiant elevation and distance from the camera field;
- angular-velocity detection efficiency;
- masked field of view;
- atmospheric collecting area; and
- time-area product (TAP).

Under the GMN data policy, Level 2 data remain owned by the station operators and are not publicly distributed without consent. The preferred route is therefore for GMN collaborators to run the frozen GhostStream configuration internally and return flux products, rather than transferring private station data.

## Scientifically unbiased station sample

Do **not** select station nights only because they contain one of the 95 confirmed multi-station members. That would condition the exposure sample on a detection and bias the flux upward.

The requested analysis population is:

- every GMN station-night for which the official flux pipeline can produce valid exposure;
- years 2022, 2023, 2024, 2025, and 2026;
- solar longitude 32°–43° for the principal run;
- explicit activity bounds 35.902°–39.902° for the core result; and
- all zero-detection nights retained.

A separate 316-row member station-night manifest is maintained only to confirm that all cameras which contributed the 95 trajectories are represented. It is not an inclusion filter.

## Frozen shower parameters

The custom internal code `GSA` is used only to operate RMS before an MDC code exists.

| Quantity | Value |
|---|---:|
| Activity beginning | 35.902° solar longitude |
| Reference/maximum epoch | 38.652° |
| Activity end | 39.902° |
| RA at reference epoch | 248.503° |
| dRA/dλ⊙ | +0.887° per degree |
| Dec at reference epoch | −14.579° |
| dDec/dλ⊙ | −0.158° per degree |
| Vg at reference epoch | 37.573 km/s |
| dVg/dλ⊙ | −0.029 km/s per degree |
| Initial association radius | 3.0° |
| Reference height | use RMS velocity-dependent height model |

The reference radiant was propagated from the 95-member MDC arithmetic-mean record to solar longitude 38.652° using the measured daily motion.

## Mass-index requirement

Flux normalized to limiting magnitude +6.5 depends materially on population index `r`, equivalently mass index `s`:

`r = 10^((s - 1)/2.5)`

The mass index must not be guessed and silently frozen. The internal run should:

1. estimate the mass index from the candidate's calibrated single-station magnitude distribution using the RMS method;
2. report its uncertainty and completeness range; and
3. repeat the flux computation over at least `s = 1.7, 1.8, 1.9, 2.0, 2.1`.

Corresponding population indices are approximately 1.905, 2.089, 2.291, 2.512, and 2.754.

## Preferred collaboration route: internal GMN run

GMN collaborators retain the Level 2 station-night archives and run the current RMS flux code with the supplied custom shower catalogue entry.

Requested returned products:

1. Per-station fixed-bin ECSV files.
2. Combined fixed-bin flux CSV/ECSV.
3. Per bin:
   - solar-longitude boundaries and TAP-weighted center;
   - shower meteor count;
   - time-area product;
   - flux at limiting magnitude +6.5;
   - Poisson confidence interval;
   - mean limiting meteor magnitude;
   - equivalent limiting mass;
   - radiant elevation and field-center distance;
   - angular velocity;
   - number and IDs of contributing stations.
4. Camera-tally report.
5. Every excluded station-night and the exclusion reason.
6. The mass-index fit and sensitivity-grid outputs.
7. RMS commit SHA and complete configuration used.
8. Hashes of all returned tables.

Station coordinates and privately owned Level 2 files do not need to leave the GMN environment.

## Alternative route: consented minimal Level 2 package

If station operators consent to data transfer, each complete station-night directory must include enough information for the official RMS pipeline to reproduce both meteor association and exposure.

### Meteor and timing data

- `FTPdetectinfo_*` containing all detections, not only selected members;
- accurate capture/night start and end times;
- frame timing information where required;
- all nights in the requested window, including zero-candidate nights.

### Astrometric and photometric calibration

- station `.config` for that night;
- `platepar_cmn2010.cal` or the applicable plate solution;
- `platepars_all_recalibrated.json` when available;
- `platepars_flux_recalibrated.json` when available;
- `CALSTARS_*` products;
- FF files needed for star/cloud and sensor characterization, unless equivalent precomputed metadata are supplied;
- mask and flat-field products used by the station.

### Precomputed substitutes accepted by RMS

Where raw calibration images are not transferred, provide the complete precomputed equivalents used by the flux pipeline, including:

- clear-sky/flux time intervals;
- sensor-characterization metadata;
- recalibrated meteor and flux platepars;
- collection-area metadata for the candidate reference height and mass-index grid; and
- any fixed-bin flux metadata already calculated.

A partial directory containing only `FTPdetectinfo` and a nominal platepar is not sufficient for publication-quality flux.

## Required quality controls

- Preserve the official RMS cloud detection and sporadic-rate rejection.
- Retain nights with no associated stream meteors when exposure is valid.
- Use fixed solar-longitude bins shared across stations and years.
- Report results with and without the stations contributing the largest TAP.
- Repeat after excluding every geographic region in turn.
- Repeat with association radii 2°, 3°, and 4°.
- Repeat over the mass-index sensitivity grid.
- Inspect the magnitude distribution for the completeness rollover.
- Publish the camera tally and station-night exclusion log.

## Outputs that would close the current limitation

A defensible result would provide:

- an absolute flux profile in meteoroids per 1000 km² per hour;
- equivalent ZHR with mass-index uncertainty propagated;
- a physical activity maximum and width;
- interannual flux variation from 2022–2026;
- a quantitative demonstration that the stream is not caused by a small number of high-TAP cameras; and
- an archive sufficient for another RMS user to reproduce the combined result.

Until these products exist, the manuscript must retain the current wording: the four-degree profile is **source-normalized relative activity**, not absolute flux or ZHR.
