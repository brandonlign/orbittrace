# Requested internal GMN flux run for the GhostStream April candidate

## Purpose

Run the current RMS physical-flux pipeline on GMN Level 2 station-night data for an uncatalogued late-April meteor-stream candidate. The underlying Level 2 data can remain within GMN. Only aggregate and per-station flux products are requested.

This document is a technical run specification, not an email and not authorization to contact station operators.

## Candidate configuration

Use the generated custom flux catalogue entry with internal code `GSA`. This is not an official IAU code.

- solar-longitude analysis range: 32°–43°;
- supported activity core: 35.902°–39.902°;
- reference epoch: 38.652°;
- RA at reference: 248.502564°;
- dRA/dλ⊙: +0.887078°/degree;
- Dec at reference: −14.579393°;
- dDec/dλ⊙: −0.157506°/degree;
- Vg at reference: 37.573416 km/s;
- dVg/dλ⊙: −0.029349 km/s/degree;
- initial association radius: 3.0°;
- use RMS velocity-dependent reference height;
- years: 2022–2026.

## Inclusion rule

Include every station-night in the requested solar-longitude interval that passes the standard RMS flux quality controls, whether it contains zero, one, or multiple GSA-associated meteors.

Do not restrict the run to stations or nights known to contain the 95 confirmed multi-station members.

## Required analysis grid

### Mass index

Estimate the candidate's mass index using the calibrated single-station magnitude distribution. Independently rerun the flux result at:

- s = 1.7;
- s = 1.8;
- s = 1.9;
- s = 2.0;
- s = 2.1.

### Association radius

Rerun at:

- 2°;
- 3° primary;
- 4°.

### Temporal bins

Return fixed solar-longitude bins no wider than 0.1° for the machine-readable station products. Adaptive combined bins may also be reported, but should not replace fixed-bin output.

### Leave-out checks

Repeat the combined result after excluding:

- each geographic region in turn;
- each of the five years in turn;
- the five stations with the largest total TAP in turn; and
- all station-nights whose limiting magnitude or cloud metrics fall in the poorest accepted decile.

## Required output tables

### Per-station fixed-bin table

For every accepted station and bin:

- station ID;
- UTC interval;
- solar-longitude boundaries and TAP-weighted center;
- associated meteor count;
- TAP;
- flux and confidence interval;
- limiting meteor magnitude;
- equivalent limiting mass;
- radiant elevation;
- radiant distance from field center;
- angular velocity;
- mass/population index used;
- all applied corrections;
- quality and exclusion flags.

### Combined table

For every combined bin:

- total meteor count;
- total TAP;
- physical flux at +6.5 limiting magnitude;
- equivalent ZHR;
- confidence interval;
- number of contributing stations;
- station IDs or a separate membership table;
- TAP-weighted limiting magnitude, radiant elevation, radiant distance, and angular velocity.

### Audit products

- camera-tally report;
- list of all candidate meteors and their single-station associations;
- station-night exclusion table with reason;
- mass-index fit data and completeness cut;
- RMS repository commit SHA;
- custom shower catalogue used;
- command line/configuration used;
- SHA-256 hashes of all returned files.

## Acceptance criteria

The absolute-flux stage passes only when:

1. the candidate has nonzero combined TAP across the supported four-degree activity core;
2. the flux excess remains after mass-index and association-radius sensitivity tests;
3. no single station supplies more than 25% of the total TAP or detections without a leave-out result showing the signal persists;
4. at least two geographically separated station groups independently contribute positive flux bins;
5. the magnitude distribution has an explicit completeness threshold;
6. all zero-detection but valid-exposure station nights are retained; and
7. the run is reproducible from the returned configuration and fixed-bin tables.

## Return format

Preferred: one compressed archive containing machine-readable CSV/ECSV/JSON tables and plots. Private station coordinates may be omitted or obfuscated. Station IDs are sufficient for reproducibility audits provided GMN retains the internal coordinate mapping.
