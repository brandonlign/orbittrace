# GhostStream recovered MDC package consistency audit

**Verdict:** `PASS_RECOVERED_MDC_PACKAGE_INTERNALLY_CONSISTENT`

- Checks: **132**
- Passed: **132**
- Failed: **0**
- Lookup rows: **95**

## Recovered analysis evidence

- immutable recovered source snapshots: 13 + 35 files
- exact primary reproduction: 101 total events and exact 95-event lookup
- exact internal downstream reproduction: source null, 20,000-replicate bootstrap, activity profile, three geographic groups, and 81/81 specification cells
- recovered external reproduction: 6 CAMS + 4 SonotaCo events, exact 10-event pooled ID set, and current JPL screen
- publication/formal MDC submission remains blocked pending package completion and independent review

## Package manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `pilots/ghoststream/RESULTS.md` | 14396 | `60d4111050fdb72798541b9075720e5ae11d30305c44be9467f9d51f72611e83` |
| `pilots/ghoststream/april_stream/candidate_solution.json` | 9610 | `d79e9ad9a51f6b4b4dad55e1077c82d165db73ad30767f30af67e36522f696c9` |
| `pilots/ghoststream/april_stream/edmond_2024/linked_v601_frozen_summary.json` | 3848 | `53ef2295cc4a076ae11cf54df348129c801a6ccb622149730c98b1b2ab6fb9f4` |
| `pilots/ghoststream/april_stream/mdc/GhostStream_April_95_GMN_lookup.csv` | 11464 | `0f021d95df56901ba119114d9b7c3816abbb3c86354638f23a69eed71b1aa6d3` |
| `pilots/ghoststream/april_stream/mdc/GhostStream_April_mean_legacy.txt` | 446 | `c327333469911555360656b8c9659ee1afa90e7100bb511034b95f871377558d` |
| `pilots/ghoststream/april_stream/mdc/GhostStream_April_mean_submission.json` | 2158 | `ad674924a6f6730f7a1c78b6825d670b6c4bdf7f8aed3a58c7a382b15460aded` |
| `pilots/ghoststream/april_stream/mdc/MANUSCRIPT_DRAFT.md` | 32882 | `85aaa852f384eb81fef77952d65018e70d8dd13f83d448463a81c8abe80408a7` |
| `pilots/ghoststream/april_stream/mdc/MDC_OFFICIAL_CHECKER_REPORT.md` | 3590 | `99b71ffb837de61598319afb61a8d01490869810fc37a43f257ba1f930347c3a` |
| `pilots/ghoststream/april_stream/mdc/README.md` | 7637 | `0e2a50aeddf343cc007d1d243c92a9e34bc3049087478312ee24458d09786790` |
| `pilots/ghoststream/april_stream/mdc/SUBMISSION_CHECKLIST.md` | 6565 | `e2a89860f22fcdb4aa0c4e4953b3dc0bbb9e2b2f6de2dfb7a04148bc4ac342dd` |
| `pilots/ghoststream/april_stream/mdc/calculation_audit.json` | 1307 | `bcfc50adf58d70d73983e1ebae51a719ea8ae882d43938fd7220b2f8e6d3ff9c` |
| `pilots/ghoststream/april_stream/mdc/exact_official_checker_summary.json` | 2130 | `580c9c0906c5d925d0071bd8770eb9a56c28ce5e51c66c34cfa9c0232f8f494a` |
| `pilots/ghoststream/april_stream/mdc/live_mdc_novelty_refresh_summary.json` | 1506 | `6d2c2b145a63048938244f0a5c7fb7c078d48c53a46959ec68b89b4b577573ee` |
| `pilots/ghoststream/reconstruction/exact_downstream/downstream_reproduction.json` | 5353 | `76199073253bed52dd74da4875581b255f8f843b3a735f64bd0fe6e34fc5de79` |
| `pilots/ghoststream/reconstruction/exact_external/external_reproduction.json` | 6352 | `bc77b935a95ad88f9d96a49035eae963f57471efbb5cd879e2f17a6a6bc6ee56` |
| `pilots/ghoststream/reconstruction/exact_recovered/exact_reproduction.json` | 1997 | `a94a8682ba3a7380a7bc2b23c673e4ea498d4a577ac81667566785cf1ceaade8` |
| `pilots/ghoststream/recovered_pipeline/SOURCE_MANIFEST.json` | 9535 | `7f35fcd6c07843d93d5aa5697f440745720eaf6e73f00121e1bef07d88bc7140` |
| `pilots/ghoststream/recovery/CURRENT_RECOVERY_STATUS.md` | 4883 | `2d37545a041ff887ccf163cb47b02dbfed4486025e875b6eda58cf6514abb6e2` |
| `pilots/ghoststream/reproducibility_gap_summary.json` | 6410 | `0b07d56a74a57e87ff729b4b701267314ef2921bcc6716e22599facaf3ebc9f4` |
| `pilots/ghoststream/results/ghoststream_final_summary.json` | 8950 | `2b55b583710d762bf4334ecc84ac87326d0e4da619f976834db2e1f5ee5dd578` |

## Claim boundary

This audit establishes internal consistency between the draft MDC package and the recovered computational evidence. It does not constitute IAU submission, official recognition, independent scientific review, a complete EDMOND v6.01 replication, or parent-body identification.
