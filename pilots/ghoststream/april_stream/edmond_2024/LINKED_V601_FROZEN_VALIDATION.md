# Full linked EDMOND v6.01 frozen validation

**Verdict:** `LINKED_EDMOND_ARCHIVES_PROVIDE_SUPPORT_BUT_NOT_FULL_FROZEN_PASS`

## Scope

The public EDMOND v6.01 page advertises a 2024 annual archive containing 13,513 refined orbits, but the linked `U2_2024_EDM.zip` attachment returns HTTP 404. The missing file was not inferred, reconstructed, or replaced.

Instead, the unchanged GhostStream April template was applied to every annual ZIP that the same public page links and that independently passed ZIP-signature, CRC, CSV-schema, and finite-field checks. This evaluated the complete usable linked series from **2001 through 2023**. No parameter, width, activity interval, quality rule, or threshold was fit from EDMOND.

## Acquisition result

- Validated annual archives: **23** (`2001–2023`)
- Unavailable annual archive: **2024 only** (`HTTP 404`)
- The separate recovery audit tested **434** candidate URLs and found no CRC-valid 2024 archive.
- In that same run, the neighboring official 2023 attachment was a valid ZIP containing 17,587 CSV rows before validation and exact-time deduplication.
- 2023 archive SHA-256: `e50c52c6101222196bdfa49ed4f0ffebf481d1446469495ff8b2381b8a3f259e`

This is a clean acquisition negative for the missing 2024 attachment, not a scientific negative for the stream.

## Frozen selection

The evaluation used the values already frozen in `candidate_solution.json`:

- epoch solar longitude: **36.901963°**
- Sun-centered ecliptic longitude: **−149.3763247°**
- ecliptic latitude: **+7.3230377°**
- geocentric speed: **37.641692 km/s**
- angular drifts: **−0.1029483°/°** and **−0.0230546°/°**
- external geocentric-speed drift: **0 km/s/°**
- residual dispersions: **0.7369°**, **0.6250°**, and **1.1596 km/s**
- radiant-speed core: standardized squared score **≤ 9**
- activity interval: **±4°** in solar longitude

Exact `_localtime` duplicates were resolved before selection using only EDMOND quality fields (`_QA`, `_Qc`, `_dGP`, `_Nts`, `_Nos`) and source order. Candidate coordinates and orbital distance did not enter duplicate resolution. Orbit was not used to select members.

## Result

The frozen template selected exactly **six** events:

| Year | Members |
|---:|---:|
| 2014 | 1 |
| 2016 | 2 |
| 2017 | 2 |
| 2022 | 1 |

No member was selected in any other validated annual file, including 2023.

All six selected UTC events are exact matches to the six events previously preserved from the independent Shober EDMOND subset. The full linked annual archives therefore add **zero new selected events**, but they independently reproduce the previously extracted six-member set from the public annual series.

### Frozen activity test

Within the expanded antihelion source, the pooled table was:

| | Frozen radiant-speed core | Outside core |
|---|---:|---:|
| Inside ±4° activity interval | 6 | 1,060 |
| Outside activity interval | 95 | 116,164 |

- one-sided Fisher exact p: **0.0003378529**
- Haldane–Anscombe odds ratio: **7.4554**
- selected members: **6**

The activity enrichment is strong, but the preexisting standalone gate required both **N ≥ 8** and **p ≤ 0.01**. The member-count requirement fails.

### Shifted-window audit

Forty-eight equally spaced frozen-geometry comparison windows were evaluated.

- shifted windows equaling or exceeding the observed odds ratio: **2**
- plus-one empirical p: **3/49 = 0.0612245**

This narrowly misses a conventional 0.05 localization threshold. It is the second reason this result is not promoted to a full frozen pass.

### Post-selection orbit test

Using standard Southworth–Hawkins `D_SH` only after radiant-speed-time selection:

- median `D_SH`: **0.036005**
- q90 `D_SH`: **0.073441**
- maximum `D_SH`: **0.098060**
- source/time-matched null trials: **20,000**
- null trials as compact or more compact: **0**
- plus-one orbit-null p: **4.99975 × 10⁻⁵**

The orbital evidence is decisive and was not used to create the selected set.

## Latest-year cross-check

A separate narrow audit of the two latest usable annual files found:

- 2022: one selected event, the already known `_20220428_215139`; activity p = **0.00944**
- 2023: zero selected events
- pooled 2022–2023: one member; activity p = **0.03289**

This is consistent with the complete 2001–2023 evaluation and adds no new event.

## Interpretation

The full public linked archive series confirms that the earlier six EDMOND events were not artifacts of the Shober subset extraction. The unchanged template recovers exactly those six and no others. Their activity enrichment and orbital compactness are strong, but the evidence does not satisfy the frozen standalone member-count gate and the supplemental shifted-window localization audit is slightly above 0.05.

EDMOND remains supporting evidence, not a fully independent third instrument, because it is a compiled archive that may share upstream network provenance with other historical video-meteor catalogues.

The primary GhostStream conclusion is unchanged:

> GhostStream identified a high-confidence uncatalogued annual April meteor-stream candidate in GMN, with primary external historical support from CAMS and SonotaCo and additional orbitally strong support from six EDMOND events.

The missing 2024 attachment provides no evidence for or against the stream.

## Reproduce

```bash
python pilots/ghoststream/april_stream/edmond_2024/evaluate_linked_v601_archives.py \
  --output-dir edmond_linked_evaluation \
  --workers 4
```

Supporting acquisition audits:

```bash
python pilots/ghoststream/april_stream/edmond_2024/recover_current_edmond.py \
  --output-dir edmond_recovery

python pilots/ghoststream/april_stream/edmond_2024/audit_archive_indices.py \
  --output-dir edmond_archive_audit
```

## Preserved CI evidence

- Full linked evaluation workflow run: `30677912275`
- Full linked evaluation artifact: `8811142249`
- Artifact SHA-256: `52db19192755c95b40d486fabc0054f9b82d0032f521a09fd2ca37aa548f48ca`
- Initial recovery workflow run: `30677260504`
- Recovery artifact: `8810993046`
- Recovery artifact SHA-256: `55cb868d4f4f0b67daf125034174e5b36bf7add65d3294c9b88fa7b419d95735`
