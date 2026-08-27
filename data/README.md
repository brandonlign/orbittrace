# Data and provenance

The repository contains the derived tables used in the paper. The original catalogues remain with their providers and are not redistributed here. This file records the source locations, coverage, acquisition notes, and checksums needed to identify the data behind the release.

## Global Meteor Network

- Source: [GMN trajectory summary data](https://globalmeteornetwork.org/data/traj_summary_data/)
- Acquisition date used for this release: 2026-08-22
- Discovery input: April 2025–2026
- Canonical and earlier-year confirmation: April 2022–2026
- Earlier recurrence check: 2019–2021
- Activity-profile background: March–May 2022–2026

A convenient raw-data reconstruction is therefore to download the March, April, and May GMN monthly trajectory-summary files for 2019–2026 (2026 data only through the months available at the release date). That superset covers the reported April search/confirmation, the pre-2022 recurrence check, and the March–May activity profile. The optional `gmn-python-api==0.0.13` client can be used separately to acquire files, but it is not part of the pinned release environment because its legacy pandas requirement conflicts with the analysis stack.

The GMN preparation used the same basic quality rules reported in the paper:

- multi-station trajectories only;
- at least two participating stations;
- median trajectory-fit error no greater than 180 arcsec;
- finite geocentric radiant, speed, and orbital elements;
- geocentric speed between 5 and 75 km s⁻¹;
- GMN shower classification marked sporadic;
- when multiple trajectory solutions shared an event time, keep the solution with the lowest fit error, using station count as the tie-breaker.

The prepared-panel columns used by the public ACRF application are:

`event_id`, `year`, `sol_lon_deg`, `lamgeo_deg`, `betgeo_deg`, `vgeo_km_s`, `e`, `q`, `inc`, `peri`, `node`.

The public GMN-derived outputs include `canonical_95.csv`, `acrf_discovery_family_123.csv`, `annual_membership.csv`, `annual_recurrence_2019_2026.csv`, and the activity/radiant/orbit tables listed in [`../figures/README.md`](../figures/README.md).

## CAMS

- Source/version: CAMS v3 as distributed through [IAU MDC Version 2026](https://ceresiaumdc.ta3.sk/)
- Coverage used: 2010–2016
- Selected comparison rows: `cams_match_table.csv`
- Reference date: 2026-08-01 result package

Keep the raw CAMS archive outside this repository, record its SHA-256 hash, and apply the fixed GMN template in `configs/external_replication.json` without refitting it to CAMS.

## SonotaCo

- Primary annual source: `https://www.astro.sk/iaumdcDB/public/data/SNMv3/{yy:03d}a.zip`
- Mirror used by the recovered analysis: `https://ceres.ta3.sk/iaumdcdb/dataDBs/video_offline/iaumdcSNMv3_S{yy:02d}.csv.zip`
- Coverage used: 2007–2025
- Selected comparison rows: `sonotaco_match_table.csv`
- Reference date: 2026-08-01 result package

Download only the needed annual archives, keep the original ZIP files, and record their SHA-256 hashes before parsing. Published event identifiers should be preserved. The OrbitTrace template is fixed by `configs/external_replication.json` and is not refit to SonotaCo.

## EDMOND

- Source page: [EDMOND database](https://meteornews.net/edmond/)
- Archive pattern: `https://meteornews.net/assets/2025-03-29-edmond-database/U2_{year}_EDM.zip`
- Coverage used: 2001–2017
- Selected rows: `edmond_match_table.csv`
- Reference date: 2026-08-01 result package

The linked 2024 archive was not available in the source set used here, so the analysis follows the listed releases. EDMOND is treated as supplementary because it can share upstream observations with other networks.

## IAU MDC duplicate screen

- Source: `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt`
- Catalogue update used: 2026-08-14 20:00 UTC
- Downloaded catalogue SHA-256: `418365d3f005bc6a2ead6e8bc0548dafdc4cc378843c8c2bf351f79af5293dbf`
- Rows screened: 2,179
- Previous 2026-06-25 snapshot cross-check: 2,174 rows
- Result: 0 hard duplicates; nearest complete-orbit alternative NOP-004

The raw MDC text file is not included. The fixed-rule result and its readable summary are in `results/mdc_duplicate_screen.json` and `results/mdc_duplicate_screen.md`.

## Package checksums

These SHA-256 values identify the derived data and result files in the release. They do not substitute for hashes of independently downloaded third-party archives.

On macOS:

```bash
shasum -a 256 data/derived/* results/*
```

On Linux, use `sha256sum` instead.

### `data/derived/`

| File | SHA-256 |
| --- | --- |
| `acrf_baseline_metadata.json` | `461b58fad4ff9487dcb08b013043ad52feb6cc2a38b7b28e4aff1903cc071b11` |
| `activity_profile_metadata.json` | `c1c236daf13809aecd7dce06510a3c094619284f72db29461e765032db12cae7` |
| `activity_profile_year_summary.csv` | `56375ba90f8dc6e53e62c3f979daca7c49766227ad1bfc11d6a4cb4a93b59bbd` |
| `acrf_discovery_family_123.csv` | `c54b465115031847789628ae5b1941924aaaef61f5df1fe0be7d8a5b754c2c69` |
| `annual_recurrence_2019_2026.csv` | `fb64df02664442989f3662863124a1954c1ed0b562f8c006b17f93471c78f61a` |
| `annual_discovery_family_membership.csv` | `dcd9b1af74a05173f814fd1f88f19551c5bfe479fbc9079e2f049e073b22f1cd` |
| `annual_membership.csv` | `1ef6ba524c6a5b05bf6a86983138198d6b23bf04f68c43b095c228a2339090f2` |
| `cams_match_table.csv` | `90745f1cec82986365b3bccbe975ad11bedc3b211f71b7bf382e23d4e25b893e` |
| `canonical_95.csv` | `0f021d95df56901ba119114d9b7c3816abbb3c86354638f23a69eed71b1aa6d3` |
| `edmond_match_table.csv` | `6708cc0dba5cfc978fe39baa905cb65ba8197f068da0bddbb11ccb5c8c948751` |
| `external_replication_summary.json` | `8f69d5dc60904860572aaaff53357cd8c66bf6f57845e2c1f9daf6a8c0646079` |
| `external_zero_speed_table.csv` | `15ba2baa8751f33ffce6e1dec78249f9bbe2acd8d16b4be609b54d9acbb68e62` |
| `geographic_replication.csv` | `62296b1381cd1491a3b6078f5e75512d7fe476dbe859b66cfdb5b2bc257c5729` |
| `gmn_radiant_centroids.csv` | `457368110e71b89b933dc4db43ec299ca9ca0e1173859a99fae663f704e9fef2` |
| `gmn_orbit_template.json` | `aa6e8a3a65fe5a4700a6efd57f261df038195bbbfea8bf6c37d1e74e13b7ab2f` |
| `nop004_comparison.json` | `b59eecd843a67fde8854c5a223006ba3d67e0f9e9ed63397fedafad04c3365d6` |
| `orbit_coherence.csv` | `eabebefc39d5087033d61de951e1fced814e86eeb78eccb689bd37fb2962fb8e` |
| `orbit_coherence_metadata.json` | `a7b3737480258df828775550b75babd5fc6aa9f91458f28301cf8d2c38241528` |
| `sonotaco_match_table.csv` | `3e70d02fdea51e0da476f3bc32bb70febf5b362088cf5e31bc0a2801980c390b` |

### `results/`

| File | SHA-256 |
| --- | --- |
| `acrf_core_hyperparameter_robustness.csv` | `7516e47ecafda8a01ee71f43e087a651960a193660c8080d9f1be63d1a2e23e9` |
| `acrf_core_hyperparameter_robustness.json` | `e47efc5ccc6950621b5983d0e8ea8d8a3650e78fb09a6062b8b53309b6376f98` |
| `acrf_core_hyperparameter_robustness.md` | `e13e904f7f5f7626ea8f01addc11b85437b2daa21e65d5ba1c0ddacb851ae62c` |
| `external_replication.json` | `2df3f79427142838483ee775daeac84f685e21ba9316fdea4245dae409454c66` |
| `mdc_duplicate_screen.json` | `7425dc64b1a31375bb7847195be3ced6b23ee7e686eaad1aa252e996b356f11f` |
| `mdc_duplicate_screen.md` | `05585344f99e0ce9c7eda756c3dda90963e7c74045487bc5250b534e35cdd245` |
| `paper_headline_results.json` | `41fbd18a4c9ebeb4712a37ec43454e31530f08c53376335ab1e1fc059013228b` |

For a raw-data reconstruction, keep a separate manifest of the downloaded source files and their hashes. The MDC hash above is the exact catalogue used for the duplicate screen; the other raw-source hashes depend on the files downloaded from each provider.
