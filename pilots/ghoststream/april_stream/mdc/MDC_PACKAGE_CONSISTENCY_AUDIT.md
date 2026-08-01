# GhostStream MDC package consistency audit

**Verdict:** `PASS_MDC_PACKAGE_INTERNALLY_CONSISTENT`

- Checks: **111**
- Passed: **111**
- Failed: **0**
- Lookup rows: **95**

## Scope

The fail-closed audit mechanically cross-checks the 95-row lookup table, arithmetic-mean JSON, legacy mean record, calculation audit, exact official-checker evidence, live IAU MDC catalogue provenance, EDMOND integrity boundary, candidate JSON, final summary, manuscript, README, and submission checklist.

It independently verifies:

- lookup header, row count, sequential identifiers, unique UTC times, and chronological order;
- arithmetic means and radiant drifts recomputed from the public six-decimal lookup columns;
- the distinction between lookup-table quantization and the underlying full-precision calculation audit;
- consistent member counts (`N = 95` and 101 total selected GMN events);
- submitted orbit fields and `a = q/(1-e)` at the submitted six-decimal precision;
- the separate full-precision semimajor-axis derivation retained in `calculation_audit.json`;
- exact equality between the committed mean and the official-checker input fields;
- zero errors from both the distributed official checker binaries and a fresh build of the official Fortran source;
- the checksum-locked IAU MDC catalogue version, shower/solution counts, and zero duplicate/near-match results;
- the EDMOND claim boundary that the currently linked files are incomplete or stale relative to the advertised v6.01 release; and
- consistent scientific and submission-status wording across all canonical documents.

## Recomputed lookup quantities

```json
{
  "LoSb": 32.95845,
  "LoSe": 40.269068,
  "LoS": 37.149520378947365,
  "Ra": 247.16974634736843,
  "De": -14.342742789473684,
  "Vg": 37.617512526315785,
  "LoR": 247.72599663157894,
  "S_LoR": 210.57647625263155,
  "LaR": 7.338829473684211,
  "dRa": 0.8870783675724828,
  "dDe": -0.15750649890816443,
  "N": 95
}
```

The lookup serializes source columns to six decimals. The audit therefore uses bounded six-decimal quantization tolerances when comparing lookup-derived means and slopes with the full-precision calculation audit. These are representation tolerances, not scientific acceptance thresholds.

## Semimajor-axis correction

The audit detected that the earlier draft submitted `a = 1.420296 AU`, which was derived from unrounded mean q and e but did not equal `q/(1-e)` after q and e were serialized to six decimals.

The corrected submission record uses:

- submitted `q = 0.080114 AU`;
- submitted `e = 0.943593`;
- exact `q/(1-e) = 1.4202847164359038 AU`; and
- submitted `a = 1.420285 AU` after six-decimal rounding.

The separate full-precision calculation remains preserved:

- full-precision mean `q = 0.08011411578947367 AU`;
- full-precision mean `e = 0.9435933578947369`; and
- full-precision `q/(1-e) = 1.4202957807693795 AU`.

The exact official MDC checker reran successfully after this correction. Semimajor axis is not one of the checker's 12 input fields, while the committed radiant, speed, q, e, perihelion, node, inclination, and N remained unchanged.

## Package hashes

| File | Bytes | SHA-256 |
|---|---:|---|
| `pilots/ghoststream/april_stream/mdc/GhostStream_April_95_GMN_lookup.csv` | 11464 | `0f021d95df56901ba119114d9b7c3816abbb3c86354638f23a69eed71b1aa6d3` |
| `pilots/ghoststream/april_stream/mdc/GhostStream_April_mean_submission.json` | 2158 | `ad674924a6f6730f7a1c78b6825d670b6c4bdf7f8aed3a58c7a382b15460aded` |
| `pilots/ghoststream/april_stream/mdc/GhostStream_April_mean_legacy.txt` | 446 | `c327333469911555360656b8c9659ee1afa90e7100bb511034b95f871377558d` |
| `pilots/ghoststream/april_stream/mdc/calculation_audit.json` | 1307 | `bcfc50adf58d70d73983e1ebae51a719ea8ae882d43938fd7220b2f8e6d3ff9c` |
| `pilots/ghoststream/april_stream/mdc/exact_official_checker_summary.json` | 2130 | `580c9c0906c5d925d0071bd8770eb9a56c28ce5e51c66c34cfa9c0232f8f494a` |
| `pilots/ghoststream/april_stream/mdc/MDC_OFFICIAL_CHECKER_REPORT.md` | 3590 | `99b71ffb837de61598319afb61a8d01490869810fc37a43f257ba1f930347c3a` |
| `pilots/ghoststream/april_stream/mdc/live_mdc_novelty_refresh_summary.json` | 1506 | `6d2c2b145a63048938244f0a5c7fb7c078d48c53a46959ec68b89b4b577573ee` |
| `pilots/ghoststream/april_stream/candidate_solution.json` | 9610 | `d79e9ad9a51f6b4b4dad55e1077c82d165db73ad30767f30af67e36522f696c9` |
| `pilots/ghoststream/april_stream/edmond_2024/linked_v601_frozen_summary.json` | 3848 | `53ef2295cc4a076ae11cf54df348129c801a6ccb622149730c98b1b2ab6fb9f4` |
| `pilots/ghoststream/results/ghoststream_final_summary.json` | 3341 | `f9245309ca48c1324032d9ef4a165553eb0bbe989929241d5617bfa1dc27e2d2` |
| `pilots/ghoststream/RESULTS.md` | 14396 | `60d4111050fdb72798541b9075720e5ae11d30305c44be9467f9d51f72611e83` |
| `pilots/ghoststream/april_stream/mdc/MANUSCRIPT_DRAFT.md` | 30096 | `b44dd8fc562ce928dd778ab68f1581a3bb025affc06711013cf361ae122c7806` |
| `pilots/ghoststream/april_stream/mdc/README.md` | 4389 | `f6b19512f6178f4c4702a1fffe0c83b8828d88a2500c06cf9dbdd12c71b944a2` |
| `pilots/ghoststream/april_stream/mdc/SUBMISSION_CHECKLIST.md` | 4384 | `d959505cb15c305864dd474309aa35e5cd5d8dbda9df7101cdec29ef334f8884` |

These hashes identify the exact inputs evaluated by the passing workflow. Later edits require a fresh audit and new manifest.

## Preserved CI evidence

- Workflow run: `30679519051`
- Artifact: `8811703184`
- Artifact SHA-256: `9b60b836a6781e574b50ad7d9b6b6f445ef8feab59250d47ee75adf605a05776`

## Claim boundary

This is an internal-consistency and provenance audit. It does not constitute IAU submission, official recognition, external scientific review, or a new independent replication.
