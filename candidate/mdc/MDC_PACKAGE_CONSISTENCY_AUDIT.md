# GhostStream recovered MDC package consistency audit

**Verdict:** `PASS_RECOVERED_MDC_PACKAGE_INTERNALLY_CONSISTENT`

- Checks: **151**
- Passed: **151**
- Failed: **0**
- Lookup rows: **95**

## Recovered evidence

- immutable source snapshots: 13 + 35 files
- January–July 2026 blind matrix: one April survivor; no non-April survivors
- historical v2 method-control no-go preserved
- corrected independent 2024 method controls: 3/3 passed
- exact primary reproduction: 101 total events and exact 95-event lookup
- exact internal downstream reproduction: source null, bootstrap, activity, geography, and 81/81 specification cells
- recovered external reproduction: 6 CAMS + 4 SonotaCo, exact pooled 10-event set, and current JPL screen
- formal submission remains blocked pending independent review

## Package manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `pilots/ghoststream/RESULTS.md` | 14396 | `60d4111050fdb72798541b9075720e5ae11d30305c44be9467f9d51f72611e83` |
| `pilots/ghoststream/april_stream/candidate_solution.json` | 21287 | `a8ad20cb42da5180c653feff2e4f0347cc1e7bd4d0c1e6df0bd8e73d7077687e` |
| `pilots/ghoststream/april_stream/edmond_2024/linked_v601_frozen_summary.json` | 3848 | `53ef2295cc4a076ae11cf54df348129c801a6ccb622149730c98b1b2ab6fb9f4` |
| `pilots/ghoststream/april_stream/mdc/GhostStream_April_95_GMN_lookup.csv` | 11464 | `0f021d95df56901ba119114d9b7c3816abbb3c86354638f23a69eed71b1aa6d3` |
| `pilots/ghoststream/april_stream/mdc/GhostStream_April_mean_legacy.txt` | 446 | `c327333469911555360656b8c9659ee1afa90e7100bb511034b95f871377558d` |
| `pilots/ghoststream/april_stream/mdc/GhostStream_April_mean_submission.json` | 2158 | `ad674924a6f6730f7a1c78b6825d670b6c4bdf7f8aed3a58c7a382b15460aded` |
| `pilots/ghoststream/april_stream/mdc/MANUSCRIPT_DRAFT.md` | 32882 | `85aaa852f384eb81fef77952d65018e70d8dd13f83d448463a81c8abe80408a7` |
| `pilots/ghoststream/april_stream/mdc/MDC_OFFICIAL_CHECKER_REPORT.md` | 3590 | `99b71ffb837de61598319afb61a8d01490869810fc37a43f257ba1f930347c3a` |
| `pilots/ghoststream/april_stream/mdc/README.md` | 7637 | `0e2a50aeddf343cc007d1d243c92a9e34bc3049087478312ee24458d09786790` |
| `pilots/ghoststream/april_stream/mdc/SUBMISSION_CHECKLIST.md` | 7943 | `771707862e02458e6e5d45c237f963b47b30b1a0ccb616657f7ec10dca9715c7` |
| `pilots/ghoststream/april_stream/mdc/calculation_audit.json` | 1307 | `bcfc50adf58d70d73983e1ebae51a719ea8ae882d43938fd7220b2f8e6d3ff9c` |
| `pilots/ghoststream/april_stream/mdc/exact_official_checker_summary.json` | 2130 | `580c9c0906c5d925d0071bd8770eb9a56c28ce5e51c66c34cfa9c0232f8f494a` |
| `pilots/ghoststream/april_stream/mdc/live_mdc_novelty_refresh_summary.json` | 1506 | `6d2c2b145a63048938244f0a5c7fb7c078d48c53a46959ec68b89b4b577573ee` |
| `pilots/ghoststream/reconstruction/METHOD_CONTROL_RECONCILIATION.md` | 3309 | `8ef2f773e3dcc29776c4c38d7d8f552c0d96e428ef66b0ca73510b220dc32fef` |
| `pilots/ghoststream/reconstruction/blind_wrapper_fix.json` | 2142 | `bed9b6de2a6280c2e47af17f52f95070de7f90d0a1175b3d2c8e32da05f96adf` |
| `pilots/ghoststream/reconstruction/blind_wrapper_repaired/run_month_year_v3.py` | 2638 | `94f04270aca54d1056841390fd6bbb0cdfc25187c065c6bf886307c8effab217` |
| `pilots/ghoststream/reconstruction/exact_blind_rediscovery/blind_rediscovery.json` | 6489 | `9ebe9063b4f690ea418313571ae2a0a9714cc5ba52a777452327879a9033cfea` |
| `pilots/ghoststream/reconstruction/exact_downstream/downstream_reproduction.json` | 5353 | `76199073253bed52dd74da4875581b255f8f843b3a735f64bd0fe6e34fc5de79` |
| `pilots/ghoststream/reconstruction/exact_external/external_reproduction.json` | 6352 | `bc77b935a95ad88f9d96a49035eae963f57471efbb5cd879e2f17a6a6bc6ee56` |
| `pilots/ghoststream/reconstruction/exact_method_controls/method_controls.json` | 4234 | `0779b0d23591e33786c40b54d88d73b9e07445c25d7380ca677b257974a0ef26` |
| `pilots/ghoststream/reconstruction/exact_method_controls_v3/method_controls_v3.json` | 3906 | `92286925d47d22c382792e2094b74767436cfeb75ae8ba282a00d7c423c4b00c` |
| `pilots/ghoststream/reconstruction/exact_recovered/exact_reproduction.json` | 1997 | `a94a8682ba3a7380a7bc2b23c673e4ea498d4a577ac81667566785cf1ceaade8` |
| `pilots/ghoststream/recovered_pipeline/SOURCE_MANIFEST.json` | 9535 | `7f35fcd6c07843d93d5aa5697f440745720eaf6e73f00121e1bef07d88bc7140` |
| `pilots/ghoststream/recovery/CURRENT_RECOVERY_STATUS.md` | 7973 | `d81c3a7ae550a75ad835d5fb0632b2d69f97195ef98c8d70583b5c3f5288fd89` |
| `pilots/ghoststream/reproducibility_gap_summary.json` | 10052 | `62592d4c07596bb38014604e785d9616c1bc67f8aefadb13284119c4f46117af` |
| `pilots/ghoststream/results/ghoststream_final_summary.json` | 17028 | `d26e983432f887cd20a567be6bd62559662e46dd0d2448c58d4f4a85efe6de6e` |

## Claim boundary

This audit establishes internal consistency between the draft MDC package and the recovered computational evidence. It does not constitute IAU submission, official recognition, independent scientific review, a complete EDMOND v6.01 replication, or parent-body identification.
