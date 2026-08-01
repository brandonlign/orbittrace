# Recover and reproduce the missing GhostStream core GMN pipeline

## Problem

The GhostStream branch preserves a strong results package and reproducible later audits, but not the core source-to-result software or immutable input manifests that generated the central GMN discovery and validation results.

Publication, formal IAU MDC submission, public reproducibility release, and scientific-review outreach are paused.

## Authoritative status files

- `pilots/ghoststream/REPRODUCIBILITY_GAP_AUDIT.md`
- `pilots/ghoststream/reproducibility_gap_summary.json`
- `pilots/ghoststream/recovery/RECOVERY_CHECKLIST.md`
- `pilots/ghoststream/recovery/CURRENT_RECOVERY_STATUS.md`

## Immediate task

Run the read-only local inventory on Brandon's Mac:

```bash
cd /Users/Brandon/Desktop/isef
python3 pilots/ghoststream/recovery/audit_local_workspace.py \
  --repo /Users/Brandon/Desktop/isef \
  --output-dir /Users/Brandon/Desktop/ghoststream_recovery_audit
```

Preserve the audit output and record promising source/notebook/archive candidates with original path, modification time, byte count, and SHA-256.

## Required recovery scope

- GMN acquisition and immutable manifests
- parsing, quality filters, coordinate transforms, and exact-time deduplication
- blind candidate generation and control/injection gates
- frozen April membership selection
- source-preserving antihelion activity test
- shifted-window and post-selection orbital nulls
- uncertainty clone trials
- year/night bootstrap
- geographic split
- March–May activity profile
- 81-cell specification curve
- CAMS/SonotaCo acquisition and selection
- parent-body screen and report generation
- exact seeds, environment, station mapping, and intermediate tables

## Clean rerun gate

- [ ] recover or independently reconstruct core code
- [ ] preserve exact input manifests and hashes
- [ ] audit recovered code for hard-coded results and post-result changes
- [ ] add fail-closed input/schema/count validation
- [ ] regenerate the 95-member lookup from source catalogues
- [ ] regenerate all primary statistics under frozen rules
- [ ] document every discrepancy without retuning
- [ ] add persistent end-to-end CI
- [ ] rebuild manuscript, reports, figures, and hashes
- [ ] build a new code-inclusive expert-review bundle
- [ ] obtain external scientific review of the reproduced implementation

## Stop rules

Do not submit to a journal or the MDC, mint a reproducibility DOI, or send the superseded review bundle while this issue remains open.

If the clean rerun weakens or eliminates the candidate, revise the verdict rather than modifying thresholds to preserve the previous result.
