# GhostStream current EDMOND release audit

**Audit date:** 2026-08-01 UTC (2026-07-31 America/New_York)  
**Scientific status:** **supporting evidence unchanged; no new independent replication**

## Question

Can the advertised current EDMOND v6.01 archive be recovered and tested with the already frozen GhostStream-April solution without changing any parameter?

## Frozen scientific rule

The evaluation used the existing external-archive rule unchanged:

- epoch solar longitude: 36.901963°;
- Sun-centered ecliptic longitude: −149.3763247°;
- ecliptic latitude: +7.3230377°;
- geocentric speed: 37.641692 km s⁻¹;
- radiant drifts: −0.1029483°/° and −0.0230546°/°;
- geocentric-speed drift: fixed to 0;
- residual widths: 0.7369°, 0.6250°, and 1.1596 km s⁻¹;
- three-sigma ellipsoid: standardized squared score ≤ 9;
- activity half-width: 4°;
- expanded antihelion source: Sun-centered longitude 120°–240°, |β| ≤ 35°, and 15–50 km s⁻¹; and
- orbit evaluated only after radiant–speed–time selection.

No value was fitted or retuned using EDMOND.

## Acquisition result

The public EDMOND page advertises v6.01 (May 2025), including **13,513 refined 2024 orbits**, and links `U2_2024_EDM.zip`. The canonical attachment returns HTTP 404.

A parallel audit probed **432 deterministic live and legacy candidate paths**. Every 2024 candidate returned 404; no body reached the ZIP-validation stage. In the same run, the linked 2023 file returned HTTP 200, began with the `PK` ZIP signature, passed full CRC validation, and exposed the expected UFOOrbit-style CSV schema. This isolates the failure to the missing 2024 asset rather than general network, host, ZIP, or parser failure.

**2024 verdict:** `CLEAN_ACQUISITION_NEGATIVE — SCIENTIFIC TEST NOT RUN`

This is not a scientific non-replication. The 2024 population is unknown because the advertised file was not obtained.

## Integrity of the surviving annual links

All linked annual ZIPs for 2001–2023 were downloaded, CRC-checked, and inspected. They are technically readable, but they do **not** match the counts advertised on the v6.01 page:

- valid linked years: 23 of 24;
- rows in linked 2001–2023 CSVs: **481,252**;
- advertised rows for those same years: **614,758**;
- coverage relative to the page table: **78.283%**;
- years whose linked CSV count exactly matches the advertised count: **0 of 23**;
- `_Version` values in the linked rows: `513` for 257,305 rows, `516` for 223,941 rows, plus six malformed control-character rows; and
- 2024: HTTP 404.

Therefore, the surviving attachments are described below as the **currently linked files**, not as a complete v6.01 release. The `_Version` values and count mismatch are consistent with stale or mixed earlier exports, although the exact semantics of `_Version` should be confirmed with the EDMOND maintainers.

## Frozen-template result on all usable linked files

The frozen selector was applied to all 23 usable annual files:

- raw rows: **481,252**;
- valid exact-time-deduplicated rows: **458,754**;
- selected candidate events: **6**;
- selected years: 2014 (1), 2016 (2), 2017 (2), and 2022 (1);
- exact UTC overlaps with the previously reported six-event Shober EDMOND table: **6 of 6**; and
- additional selected events: **0**.

Thus, the full set of currently linked files reproduces exactly the prior six EDMOND events and adds no new candidate.

### Activity test

| | Core | Non-core |
|---|---:|---:|
| Inside frozen activity window | 6 | 1,060 |
| Outside frozen activity window | 95 | 116,164 |

- one-sided Fisher exact p = **3.3785 × 10⁻⁴**;
- Haldane–Anscombe odds ratio = **7.455**; and
- 48-position shifted-window empirical p = **0.06122**.

The source-preserving activity enrichment is strong, but only six events are selected. The prespecified standalone rule requires at least eight members and p ≤ 0.01. The membership requirement fails.

### Post-selection orbit check

Using standard Southworth–Hawkins orbital dissimilarity to the frozen GMN orbit:

- median D_SH = **0.03601**;
- 90th percentile D_SH = **0.07344**;
- maximum D_SH = **0.09806**; and
- 20,000-draw source/time-matched orbit-null p = **4.9998 × 10⁻⁵**.

The orbit is highly compact, but orbital evidence does not override the frozen minimum-member rule.

## Final verdict

**The current EDMOND check does not produce a new replication or a new scientific negative.**

1. The advertised 2024 v6.01 file could not be recovered, so no claim is made about 2024.
2. The surviving linked files are incomplete or stale relative to the v6.01 page table.
3. Applying the frozen solution to every usable linked annual file reproduces exactly the same six previously reported EDMOND events.
4. Those six events show strong activity and orbital enrichment but still fail the prespecified minimum of eight members.
5. EDMOND therefore remains supplementary robustness evidence, not a clean third independent instrument and not a standalone confirmation.

The overall GhostStream candidate status is unchanged: the main evidence remains the recurring GMN detection plus the primary CAMS–SonotaCo external support.

## Reopen condition

Reopen this test only when a file is obtained that:

1. is demonstrably the advertised current 2024/v6.01 export;
2. passes ZIP signature and CRC checks;
3. exposes the required trajectory and orbital fields;
4. has its row count and release provenance documented; and
5. is evaluated with the frozen selector above, without retuning.

## Reproducibility

- `recover_current_edmond.py`: exhaustive acquisition and validation audit;
- `recover_current_edmond_fast.py`: parallel deterministic path audit;
- `audit_linked_release_integrity.py`: page-count and `_Version` integrity audit;
- `evaluate_linked_v601_archives.py`: frozen-template evaluation of usable linked annual files; and
- GitHub Actions artifacts retain the full machine-readable probe, integrity, member, and statistical outputs for the corresponding runs.
