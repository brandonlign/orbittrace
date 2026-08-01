# Pre-submission checklist

## Scientific checks

- [x] Blind candidate generated in untouched 2026 data.
- [x] Frozen historical GMN replication completed.
- [x] Exact-time duplicate solutions removed.
- [x] Activity test repeated without orbital elements.
- [x] Expanded antihelion-source null passed.
- [x] Measurement-uncertainty clone gate passed: 1,000/1,000 trials.
- [x] Twenty-thousand-replicate year/night cluster bootstrap completed.
- [x] RA and declination drift resolved; geocentric-speed drift correctly marked unresolved.
- [x] Frozen 81-cell specification curve completed: 81/81 cells passed.
- [x] Checksum-locked official IAU MDC catalogue version 2026-06-25 parsed 1,072 shower records / 2,174 solutions and found zero hard duplicates, zero activity-compatible radiant–speed near matches, and zero orbit-incomplete near matches.
- [x] CAMS and SonotaCo primary external support documented.
- [x] Uniform zero-speed-drift external rerun completed.
- [x] Shober EDMOND subset adds six non-overlapping, orbitally compact supporting meteors.
- [x] EDMOND provenance limitation is explicit; it is not counted as a fully independent third instrument.
- [x] Current EDMOND-link integrity audit completed: linked 2001–2023 files cover 78.283% of advertised rows, embed versions 513/516 rather than 601, and are not represented as a complete v6.01 replication.
- [x] NASA/JPL parent screen completed.
- [x] March–May source-normalized activity profile replaces raw month-boundary interpretation.
- [x] Three disjoint GMN geographic station groups independently pass activity and orbit gates.
- [x] Official EDMOND 2024 page/link audit documented; advertised attachment was unavailable and no scientific inference was drawn from the missing file.
- [ ] External meteor expert reviews coordinate, orbit, and radiant-drift conventions.
- [ ] Independent network reruns the frozen solution or its own preregistered search.
- [ ] Absolute exposure/flux profile models station uptime, weather, limiting magnitude, radiant elevation, and collecting area using consented GMN Level 2 data.
- [ ] Final duplicate search includes any newly added MDC solutions immediately before submission.

## Data checks

- [x] Lookup-table row count equals N = 95.
- [x] All lookup times are UTC and unique.
- [x] All lookup radiants are geocentric J2000 values.
- [x] SCLO is reported in the 0–360° convention.
- [x] Submitted semimajor axis is `a = 1.420285 AU`, computed from the submitted six-decimal `q = 0.080114 AU` and `e = 0.943593`, then rounded to six decimals; the separate full-precision derivation is preserved in `calculation_audit.json`.
- [x] Exact official MDC checker rerun used the committed mean record; the distributed binaries and a fresh build of the distributed Fortran source produced identical comparison files and zero orbital/geocentric errors.
- [x] Shober EDMOND source file MD5 verified against the Zenodo record.
- [x] Exact cross-source duplicate audit found zero duplicate UTC events among the 16 external members.
- [x] Machine-readable candidate solution records bootstrap intervals and unresolved speed drift.
- [ ] Fail-closed package-wide consistency audit passes across the 95-row lookup, mean JSON, legacy record, calculation audit, checker evidence, catalogue provenance, external-evidence boundaries, manuscript, and final summary.
- [ ] Confirm the preferred GMN catalogue version string and citation.
- [ ] Archive hashes for every GMN monthly source catalogue used in the final submission analysis.
- [ ] Regenerate and checksum-lock the final sent package after all manuscript edits are complete.

## Authorship and publication

- [ ] Confirm authors and contribution order.
- [ ] Confirm GMN acknowledgment and whether network collaborators should be invited.
- [ ] Add corresponding-author email.
- [ ] Select journal.
- [ ] Obtain mentor/expert approval before contacting the MDC.
- [ ] Replace “manuscript in preparation” with the actual submitted reference.

## MDC delivery

- [ ] Ask MDC contacts whether JSON or the legacy text mean record is preferred.
- [ ] Allow the MDC to assign the provisional designation, IAU number, and code.
- [ ] Send mean record, lookup table, and manuscript together.
- [ ] Preserve the sent package and email receipt.
- [ ] Track the one-year publication deadline from the actual submission date.
