# GhostStream expert review bundle record

Built: 2026-08-01 UTC

## Verdict

`PASS_EXPERT_REVIEW_BUNDLE_BUILT`

## Source

- Branch: `agent/ghoststream-pilot`
- Exact bundled branch commit: `e65437383099b696b28606bcf2cf3e65aad2f0f0`
- Included scientific files: **22**
- ZIP members including README and manifest: **24**

## Bundle integrity

The deterministic inner review ZIP is:

- File: `GhostStream_Expert_Review_Bundle.zip`
- Size: **57,983 bytes**
- SHA-256: `5ecf86b507e0d677bda37eb5716aede0ff4adab54eb8e804e4f73e654a105a14`
- ZIP CRC test: **passed**
- Embedded `MANIFEST.json` source commit: `e65437383099b696b28606bcf2cf3e65aad2f0f0`

The GitHub Actions artifact wrapper is:

- Workflow run: `30679946992`
- Artifact name: `ghoststream-expert-review-bundle`
- Artifact ID: `8811845053`
- Artifact size: **57,657 bytes**
- Artifact SHA-256: `59da18d6539d2a0ca8f13bac0609ae29cb2296439ef5908ff2aa307cedebaa44`
- Artifact expiration: **2026-08-31 02:24:45 UTC**

The artifact wrapper contains the inner review ZIP, the build-result JSON, and the build log. The inner ZIP hash above is the identifier that should be recorded when sending the package to a reviewer.

## Included review set

The bundle contains:

- expert review packet;
- candidate dossier and frozen candidate JSON;
- manuscript, 95-row lookup table, mean records, and calculation audit;
- exact official MDC checker report and machine-readable result;
- live IAU MDC novelty refresh and machine-readable result;
- passing 111-check MDC package consistency audit and summary;
- bootstrap, specification-curve, activity-profile, and geographic-split reports;
- CAMS/SonotaCo/EDMOND external-evidence synthesis and event table; and
- the current EDMOND linked-release integrity audit.

It excludes raw monthly catalogues, raw downloads, temporary development logs, GitHub workflows, and internal outreach drafts.

## Sending rule

Before sending, record:

1. recipient;
2. date sent;
3. exact inner ZIP SHA-256;
4. source branch commit;
5. any files sent separately; and
6. the review response or lack of response.

Any scientific edit after this bundle was built requires a new bundle and new hashes.
