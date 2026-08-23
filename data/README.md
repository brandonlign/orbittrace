# Data and provenance

This repository contains derived tables only. Raw GMN, CAMS, SonotaCo, EDMOND, and MDC files are not redistributed because their hosting and catalogue terms vary. Download the frozen source versions below, record the downloaded file hashes, and then prepare the panel schema documented in `acrf/application.py`.

## GMN

- Source: [GMN trajectory summary data](https://globalmeteornetwork.org/data/traj_summary_data/)
- Access method: monthly trajectory-summary files; the optional `gmn-python-api==0.0.13` client may be used separately to acquire them. It is not required by the reproducibility environment because its legacy pandas constraint conflicts with the pinned analysis stack.
- Analysis slice: April 2022, 2023, 2024, 2025, and 2026; quality filtering and sporadic-only selection are part of the preparation step.
- Acquisition/freeze date: 2026-08-22.
- The public derived outputs are `canonical_95.csv`, `acrf_discovery_family_123.csv`, and `annual_membership.csv`. The paper figures additionally use the frozen activity, recurrence, radiant-centroid, and orbit-coherence tables listed in `figures/README.md`.

For a raw rerun, download the five monthly files from the GMN monthly directory, preserve their original bytes, and convert them to the prepared-panel columns required by `acrf/application.py`: `event_id`, `year`, `sol_lon_deg`, `lamgeo_deg`, `betgeo_deg`, `vgeo_km_s`, `e`, `q`, `inc`, `peri`, and `node`.

## CAMS

- Source/version: CAMS v3 as distributed through [IAU MDC Version 2026](https://ceresiaumdc.ta3.sk/).
- Coverage used: 2010–2016; the selected comparison rows are in `cams_match_table.csv`.
- Freeze date: 2026-08-01 result package.
- Do not commit the raw CAMS archive. Re-download the release, preserve its archive hash locally, and apply `configs/external_replication.json` without refitting the GMN template.

## SonotaCo

- Primary annual source: `https://www.astro.sk/iaumdcDB/public/data/SNMv3/{yy:03d}a.zip`.
- Video-offline mirror used by the recovered analysis: `https://ceres.ta3.sk/iaumdcdb/dataDBs/video_offline/iaumdcSNMv3_S{yy:02d}.csv.zip`.
- Coverage used: 2007–2025, with the selected comparison rows in `sonotaco_match_table.csv`.
- Freeze date: 2026-08-01 result package.

Download only the needed annual archives, retain the original ZIP files outside this repository, and record SHA-256 hashes before parsing. The parser must preserve the published event identifiers and apply the fixed template in `configs/external_replication.json`.

## EDMOND

- Source page: [EDMOND database](https://meteornews.net/edmond/).
- Frozen archive pattern: `https://meteornews.net/assets/2025-03-29-edmond-database/U2_{year}_EDM.zip`.
- Coverage used: 2001–2017; the selected supplementary rows are in `edmond_match_table.csv`.
- Freeze date: 2026-08-01 result package.
- The linked 2024 archive was unavailable in the frozen acquisition; this is recorded as a provenance limitation, not silently filled from another source.

The EDMOND archive is supplementary and may share upstream observations with other networks. Do not interpret it as a fully independent third network.

## MDC duplicate screen

- Source: `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt`.
- Current catalogue update: 2026-08-14 20:00 UTC.
- Current downloaded catalogue SHA-256: `418365d3f005bc6a2ead6e8bc0548dafdc4cc378843c8c2bf351f79af5293dbf`.
- Current rows screened: 2,179; previous 2026-06-25 snapshot cross-check: 2,174.
- Result: 0 hard duplicates; nearest complete-orbit alternative NOP-004.

The raw MDC text file is not included. The complete fixed-rule result is in `results/mdc_duplicate_screen.json` and `results/mdc_duplicate_screen.md`.

## Derived-file checksums

The checksums below are for public package data and results, not for third-party raw archives. On macOS, recompute them with:

```bash
shasum -a 256 data/derived/* results/*
```

On Linux, use `sha256sum` in the same command.

Frozen `data/derived/` SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `acrf_baseline_metadata.json` | `cd01ee8be549c851422c025196b56f0ca8199345b3c92d9b32fd5d2c6889cdf9` |
| `activity_profile_metadata.json` | `be7356ef578638cb973890af7c3f8af92b9ffe6e8a03360c2aa5d08af06e32e0` |
| `activity_profile_year_summary.csv` | `56375ba90f8dc6e53e62c3f979daca7c49766227ad1bfc11d6a4cb4a93b59bbd` |
| `acrf_discovery_family_123.csv` | `c54b465115031847789628ae5b1941924aaaef61f5df1fe0be7d8a5b754c2c69` |
| `annual_recurrence_2019_2026.csv` | `fb64df02664442989f3662863124a1954c1ed0b562f8c006b17f93471c78f61a` |
| `annual_discovery_family_membership.csv` | `dcd9b1af74a05173f814fd1f88f19551c5bfe479fbc9079e2f049e073b22f1cd` |
| `annual_membership.csv` | `1ef6ba524c6a5b05bf6a86983138198d6b23bf04f68c43b095c228a2339090f2` |
| `cams_match_table.csv` | `90745f1cec82986365b3bccbe975ad11bedc3b211f71b7bf382e23d4e25b893e` |
| `canonical_95.csv` | `0f021d95df56901ba119114d9b7c3816abbb3c86354638f23a69eed71b1aa6d3` |
| `edmond_match_table.csv` | `6708cc0dba5cfc978fe39baa905cb65ba8197f068da0bddbb11ccb5c8c948751` |
| `external_replication_summary.json` | `b6b4376d1890baaab8d22aa7c59c6ba2180a56a573359b94c15b1d45223032a2` |
| `external_zero_speed_table.csv` | `15ba2baa8751f33ffce6e1dec78249f9bbe2acd8d16b4be609b54d9acbb68e62` |
| `geographic_replication.csv` | `62296b1381cd1491a3b6078f5e75512d7fe476dbe859b66cfdb5b2bc257c5729` |
| `gmn_radiant_centroids.csv` | `457368110e71b89b933dc4db43ec299ca9ca0e1173859a99fae663f704e9fef2` |
| `gmn_orbit_template.json` | `aa6e8a3a65fe5a4700a6efd57f261df038195bbbfea8bf6c37d1e74e13b7ab2f` |
| `nop004_comparison.json` | `b59eecd843a67fde8854c5a223006ba3d67e0f9e9ed63397fedafad04c3365d6` |
| `orbit_coherence.csv` | `9b1669650e4ac290e53576ee87cfd2a48a201bdc0689b0f97f342404479b4c8f` |
| `orbit_coherence_metadata.json` | `af0dd33d6f1b5314ba077cb359678a2b47d60a016763f8784efcc6336f4f9949` |
| `sonotaco_match_table.csv` | `3e70d02fdea51e0da476f3bc32bb70febf5b362088cf5e31bc0a2801980c390b` |

Frozen `results/` SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `acrf_core_hyperparameter_robustness.csv` | `7516e47ecafda8a01ee71f43e087a651960a193660c8080d9f1be63d1a2e23e9` |
| `acrf_core_hyperparameter_robustness.json` | `6a911063437a45601c22c26ba94470a1bd5c8bd265eaf52adb992c1fe8ab9872` |
| `acrf_core_hyperparameter_robustness.md` | `060f3a591c61fdf0bc3a368c53aed648bdbea38e060f246110ba193c43231102` |
| `external_replication.json` | `b0b6378a3ca642ecb468ebcfad53a6a10ccba89d1c6cba2820963929eba31853` |
| `mdc_duplicate_screen.json` | `7425dc64b1a31375bb7847195be3ced6b23ee7e686eaad1aa252e996b356f11f` |
| `mdc_duplicate_screen.md` | `b9ca15c2c63ce7e0c7677131a563b9937c10ca01b3e2b43fc743bf479ae877a3` |
| `paper_headline_results.json` | `0a4bd6e4fe4e14599fd5552e75c07dc76e83da18889f69e119d9ebd5f548b05a` |

The raw GMN and external-archive hashes are acquisition-specific and must be recorded in the local reproduction manifest when downloaded. The MDC hash above is the exact frozen catalogue used by the duplicate screen.

The paper-facing result JSONs record the frozen settings and headline numbers; every reproduction run should retain a separate manifest of the raw downloads used.
