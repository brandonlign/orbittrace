# GhostStream expert review bundle record

Built: 2026-08-01 UTC

## Verdict

`PASS_EXPERT_REVIEW_BUNDLE_BUILT`

## Current sendable bundle

### Source

- Branch: `agent/ghoststream-pilot`
- Exact bundled branch commit: `dd6607bbe4b5a1472d753dc966450e8526795100`
- Included scientific files: **23**
- ZIP members including README and manifest: **25**
- Generative-AI/software provenance included: **yes**

### Bundle integrity

The deterministic inner review ZIP is:

- File: `GhostStream_Expert_Review_Bundle.zip`
- Size: **63,262 bytes**
- SHA-256: `782c539109bf9ec997152b913c13775af4a6d38e366e58031e704457cf0ee80d`
- ZIP CRC test: **passed**
- Embedded `MANIFEST.json` source commit: `dd6607bbe4b5a1472d753dc966450e8526795100`
- Included AI provenance file: `mdc/AI_AND_SOFTWARE_PROVENANCE.md`

The GitHub Actions artifact wrapper is:

- Workflow run: `30680227323`
- Artifact name: `ghoststream-expert-review-bundle`
- Artifact ID: `8811936608`
- Artifact size: **63,091 bytes**
- Artifact SHA-256: `308e96f2f31c138a81f25c1007be0707e74db5157f7f69bb817f8adffe90a0d2`
- Artifact expiration: **2026-08-31 02:33:06 UTC**

The artifact wrapper contains the inner review ZIP, the build-result JSON, and the build log. The inner ZIP hash is the identifier that must be recorded when sending the package to a reviewer.

## Included review set

The bundle contains:

- expert review packet;
- candidate dossier and frozen candidate JSON;
- manuscript, 95-row lookup table, mean records, and calculation audit;
- full generative-AI and software provenance disclosure;
- exact official MDC checker report and machine-readable result;
- live IAU MDC novelty refresh and machine-readable result;
- passing 111-check MDC package consistency audit and summary;
- bootstrap, specification-curve, activity-profile, and geographic-split reports;
- CAMS/SonotaCo/EDMOND external-evidence synthesis and event table; and
- the current EDMOND linked-release integrity audit.

It excludes raw monthly catalogues, raw downloads, temporary development logs, GitHub workflows, publication/outreach strategy drafts, and internal review-response records.

## Superseded bundle

The earlier bundle from commit `e65437383099b696b28606bcf2cf3e65aad2f0f0`, inner ZIP SHA-256 `5ecf86b507e0d677bda37eb5716aede0ff4adab54eb8e804e4f73e654a105a14`, is superseded because it did not include the explicit AI/software provenance record. Do not send it.

## Sending rule

Before sending, record:

1. recipient;
2. date sent;
3. exact inner ZIP SHA-256;
4. source branch commit;
5. any files sent separately; and
6. the review response or lack of response.

Any scientific edit after this bundle was built requires a new bundle and new hashes.
