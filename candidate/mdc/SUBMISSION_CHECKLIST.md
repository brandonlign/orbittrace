# Pre-submission checklist

Formal MDC submission remains blocked pending the unchecked package, review, authorship, data-preservation, and delivery items below. The computational recovery, discovery lineage, primary/internal/external analyses, and corrected method controls are complete; this checklist does not imply official recognition or submission readiness.

## Computational recovery and reproducibility

- [x] Original recovery/discovery source preserved from immutable commit `4175e5187fcc6faf3d1befb099a9e35be96850f2`.
- [x] Original novel-search/downstream source preserved from immutable commit `39972b5fe0cf4d47092d3caa2b3ced12bedb065e`.
- [x] File-level SHA-256 source manifest committed.
- [x] Original Python environment and deterministic random seeds recovered.
- [x] Actual January–July 2026 blind-search matrix rerun from the recovered scanner.
- [x] April was the only full-gate survivor across January–July 2026.
- [x] Blind April survivor passed untouched 2025 and 2024 validation, clone stability, orbital compactness, and the automated IAU veto.
- [x] Original arbitrary-year wrapper preserved unchanged; minimal year-key/reporting repair separately documented and hashed.
- [x] Exact primary validator rerun regenerated 101 total GMN events.
- [x] Exact significant-year lookup rerun matched all 95 committed timestamps, with zero missing and zero additional events.
- [x] Recovered source-preserving activity and source/time orbit-null audit passed.
- [x] Recovered 20,000-replicate year/night bootstrap passed.
- [x] Recovered corrected March–May activity profile passed.
- [x] Recovered three-group geographic replication passed.
- [x] Recovered frozen specification curve passed 81/81 eligible cells.
- [x] Recovered CAMS and SonotaCo scripts regenerated the exact preserved ten-event pooled ID set.
- [x] Current JPL screen completed: 729/729 valid broad-compatible orbits, zero at D ≤ 0.15.
- [x] Historical v2 method-control output audited honestly: 3/3 named showers recovered and injection passed, but the aggregate verdict remained `NO_GO_DEGENERATE_PARENT_CLUSTER`.
- [x] The v2 degeneracy-rule contradiction was documented: Eta Aquariids target prevalence exceeded the global 30% largest-cluster ceiling.
- [x] A correction was frozen before independent 2024 holdouts, retaining the exact clustering setting, recovery thresholds, hidden labels, and 30% ceiling while applying it to non-target clusters.
- [x] Corrected independent-year method-control holdout passed 3/3 named showers and 3/3 non-target degeneracy checks.
- [ ] Code-inclusive expert-review bundle includes and validates the final blind-search and method-control evidence.

## Scientific checks

- [x] Candidate originated from the recovered January–July 2026 blind month/year search rather than a targeted final-template query.
- [x] January–July 2026 matrix produced one full-gate survivor, in April, and no additional non-April survivors.
- [x] Frozen historical GMN replication completed.
- [x] Exact-time duplicate solutions removed.
- [x] Activity test repeated without orbital elements.
- [x] Expanded antihelion-source null passed.
- [x] Measurement-uncertainty clone gate passed: 1,000/1,000 final-template trials and 500/500 blind-lineage trials.
- [x] RA and declination drift resolved; geocentric-speed drift correctly marked unresolved.
- [x] Checksum-locked official IAU MDC catalogue version 2026-06-25 parsed 1,072 shower records / 2,174 solutions and found zero hard duplicates, zero activity-compatible radiant–speed near matches, and zero orbit-incomplete near matches.
- [x] CAMS and SonotaCo primary external support documented with separate archive-specific limitations.
- [x] Uniform zero-speed-drift external rerun completed.
- [x] Shober EDMOND subset adds six non-overlapping, orbitally compact supporting meteors.
- [x] EDMOND provenance limitation is explicit; it is not counted as a fully independent third instrument.
- [x] Current EDMOND-link integrity audit completed: linked 2001–2023 files cover 78.283% of advertised rows, embed versions 513/516 rather than 601, and are not represented as a complete v6.01 replication.
- [x] March–May source-normalized activity profile replaces raw month-boundary interpretation.
- [x] Three disjoint GMN geographic station groups pass activity and orbit gates.
- [x] Official EDMOND 2024 page/link audit documented; advertised attachment was unavailable and no scientific inference was drawn from the missing file.
- [ ] External meteor expert reviews coordinate, orbit, node/perihelion, and radiant-drift conventions.
- [ ] External expert reviews historical/literature-only duplicate-shower risk.
- [ ] Independent network reruns the frozen solution or applies its own preregistered search.
- [ ] Absolute exposure/flux profile models station uptime, weather, limiting magnitude, radiant elevation, and collecting area using consented GMN Level 2 data.
- [ ] Final duplicate search includes any newly added MDC solutions immediately before submission.

## Data and package checks

- [x] Lookup-table row count equals N = 95.
- [x] All lookup times are UTC and unique.
- [x] All lookup radiants are geocentric J2000 values.
- [x] SCLO is reported in the 0–360° convention.
- [x] Submitted semimajor axis is `a = 1.420285 AU`, computed from the submitted six-decimal `q = 0.080114 AU` and `e = 0.943593`, then rounded to six decimals; the separate full-precision derivation is preserved in `calculation_audit.json`.
- [x] Exact official MDC checker rerun used the committed mean record; the distributed binaries and a fresh build of the distributed Fortran source produced identical comparison files and zero orbital/geocentric errors.
- [x] Shober EDMOND source file MD5 verified against the Zenodo record.
- [x] Exact cross-source duplicate audit found zero duplicate UTC events among the 16 external members.
- [x] Machine-readable candidate solution records bootstrap intervals and unresolved speed drift.
- [x] Historical 111-check package audit recomputed the lookup and identified no numerical discrepancy after the submitted semimajor-axis correction.
- [x] Corrected 2024 method-control evidence is committed with run, artifact, source, environment, and result hashes.
- [x] Blind-discovery evidence is committed with run, artifact, original/repaired wrapper hashes, environment, validation member IDs, and result summary.
- [ ] Recovered package audit passes against the current source manifest, exact primary, exact downstream, exact external, method-control, blind-lineage, manuscript, and MDC files.
- [ ] Code-inclusive expert bundle is built and checksum-validated from the current branch.
- [ ] Confirm the preferred GMN catalogue version string and citation.
- [ ] Preserve hashes or archived copies for every GMN monthly source catalogue used in the final submission analysis, subject to data-use rules.
- [ ] Regenerate and checksum-lock the final sent package after all manuscript edits are complete.

## Authorship and publication

- [ ] Confirm authors and contribution order.
- [ ] Confirm GMN acknowledgment and whether network collaborators should be invited.
- [ ] Add corresponding-author email.
- [ ] Select journal.
- [ ] Obtain mentor and independent expert approval before contacting the MDC.
- [ ] Replace “manuscript in preparation” with the actual submitted reference.
- [ ] Complete a final human review of the manuscript, code/data availability, acknowledgments, and generative-AI disclosure.

## MDC delivery

- [ ] Ask MDC contacts whether JSON or the legacy text mean record is preferred.
- [ ] Allow the MDC to assign the provisional designation, IAU number, and code.
- [ ] Send the reviewed mean record, lookup table, manuscript, and requested supporting files together.
- [ ] Preserve the sent package and email receipt.
- [ ] Track the one-year publication deadline from the actual submission date.
