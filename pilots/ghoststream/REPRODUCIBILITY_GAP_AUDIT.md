# GhostStream core-pipeline reproducibility gap audit

Audit date: 2026-08-01

## Verdict

**`CORE_ANALYSIS_NOT_REPRODUCIBLE_FROM_CURRENT_BRANCH`**

The current GhostStream branch contains a detailed scientific results package, final member tables, later archive/MDC audit code, official-checker reproduction, and fail-closed package-consistency checks. It does **not** contain the core software and exact input manifests required to regenerate the principal GMN scientific results from source catalogues.

The correct current status is:

> **Internally consistent and extensively audited results package; core discovery and validation pipeline not yet computationally reproducible from the committed branch.**

This gap blocks journal submission, formal IAU Meteor Data Center submission, and a public reproducibility claim until the original pipeline is recovered or the complete analysis is independently reconstructed and rerun.

## Evidence examined

### Branch comparison

The branch `agent/ghoststream-pilot` is 134 commits ahead of `main` and introduces 82 changed files. Every changed file in the branch comparison is marked **added**. No core analysis script appears as deleted, renamed, or replaced.

Therefore the missing implementation was not removed from this branch after producing the reports. It was either:

- executed outside the repository and never committed;
- generated in a temporary environment that was not preserved;
- stored in another local directory, branch, repository, notebook, or chat artifact; or
- represented only through derived outputs and prose reports.

### Repository code search

Repository search for the central analysis terms and exact result values did not locate implementation files for:

- blind GMN candidate generation;
- known-shower recovery and weak-stream injection gates;
- exact GMN monthly catalogue acquisition and hashing;
- GMN trajectory cleaning and exact-time deduplication;
- source-preserving expanded-antihelion activity test;
- shifted-window audit;
- post-selection source/time-matched orbital null;
- measurement-uncertainty clone trials;
- year/night hierarchical bootstrap;
- disjoint geographic station-group validation;
- March–May source-normalized activity profile;
- 81-cell frozen specification curve;
- parent-body screening; or
- the original current/working/removed IAU duplicate audit.

GitHub commit search also found no GhostStream commit on the default branch. The current branch comparison contains reports for those analyses but not their producing code.

## Code that is present

The branch does contain reproducible implementations for later bounded stages, including:

- current-linked EDMOND archive recovery, integrity, and frozen-template evaluation;
- live IAU MDC novelty refresh;
- exact rerun of the official MDC Fortran consistency programs;
- MDC package consistency auditing;
- flux-handoff catalogue/preflight tools;
- expert-review bundle construction; and
- package/document integration and provenance checks.

These scripts support the claims they directly evaluate. They do not regenerate the principal GMN discovery and confirmation results.

## Scientific outputs that are present

The branch preserves:

- the frozen candidate solution;
- the 95-row confirmed GMN lookup table;
- the 101-event multiyear count summary;
- arithmetic-mean submission records;
- external CAMS/SonotaCo/EDMOND member tables;
- reports for bootstrap, activity profile, geographic split, and specification curve;
- machine-readable final summaries;
- exact official-checker evidence; and
- a 111-check internal package-consistency audit.

These artifacts allow extensive internal cross-checking. They are insufficient to independently rerun the analyses because the required source-to-result transformations, raw input manifests, and intermediate tables are absent.

## What the 111-check package audit does and does not prove

### It does prove

- the 95-row lookup and arithmetic means agree within documented serialization precision;
- the submitted orbit is internally consistent;
- the mean record passed the official MDC checker;
- catalogue provenance and claim-boundary fields agree across canonical documents;
- the preserved summaries do not contradict one another on the tested quantities; and
- final package files match the recorded hashes.

### It does not prove

- that the 95 rows were selected by the stated frozen rules from the original GMN catalogues;
- that all eligible GMN events were included and no ineligible events were omitted;
- that the activity p-values, shifted-window results, orbit-null results, bootstrap intervals, geographic splits, clone trials, or 81-cell curve can be regenerated;
- that source-catalogue versions and quality filters are exactly recoverable;
- that random seeds and null-draw procedures are preserved; or
- that the blind discovery chronology can be independently verified from code and immutable inputs.

The package audit must therefore be described as **internal consistency and provenance validation**, not end-to-end scientific reproducibility.

## Missing reproducibility components

### Required source code

At minimum, recover or recreate:

1. GMN catalogue downloader and immutable manifest builder;
2. parser, quality filter, coordinate transformation, and deduplicator;
3. known-shower exclusion and current/working/removed IAU solution parser;
4. blind candidate-generation algorithm and discovery configuration;
5. frozen April membership selector;
6. expanded-antihelion source-preserving activity test;
7. shifted-window implementation;
8. Southworth–Hawkins or other stated orbit-distance implementation;
9. source/time-matched orbital-null sampler;
10. measurement-uncertainty clone generator and pass gate;
11. year/night hierarchical bootstrap;
12. geographic station parser and disjoint-group evaluator;
13. March–May activity-profile pipeline;
14. 81-cell specification-curve runner;
15. CAMS and SonotaCo acquisition/parsing/selection code;
16. parent-body search implementation; and
17. final report/table generator.

### Required immutable inputs and manifests

Recover or recreate:

- exact GMN monthly source URLs/files for every year/month used;
- byte counts and SHA-256 hashes;
- catalogue schema/version and access dates;
- exact IAU catalogue snapshot used in the original veto;
- CAMS and SonotaCo source files and hashes;
- station-country mapping used for geographic splits;
- uncertainty fields and conventions used for clone generation;
- random seeds and replicate counts;
- frozen configuration before each confirmatory stage;
- exact intermediate event tables before and after each filter; and
- environment/dependency specification.

## Recovery order

### Stage 1 — Search before reconstruction

Search for the original implementation in:

- Brandon's local `isef` project directory and untracked files;
- other Git branches and worktrees;
- OpenCode or coding-agent session exports;
- downloaded ZIPs, temporary directories, notebooks, and shell history;
- Google Drive or other project storage;
- GitHub Actions artifacts from earlier GhostStream runs, if any;
- previous ChatGPT/File Library uploads; and
- machine backups or Time Machine snapshots.

Preserve any recovered directory before modifying it. Hash recovered files and record their original path and modification time.

### Stage 2 — Integrity audit of recovered code

Before relying on recovered code:

- confirm it predates or matches the reported analyses;
- identify hard-coded result values or post-result parameter changes;
- verify that discovery and confirmation data are separated as claimed;
- remove credentials and machine-specific paths;
- run static compilation/tests;
- reproduce at least one small known result; and
- compare produced tables against committed outputs.

### Stage 3 — Full clean rerun

A valid recovery requires a clean environment that:

1. downloads or verifies exact inputs;
2. regenerates the 95-member lookup from source data;
3. reproduces every primary reported statistic within documented numerical tolerance;
4. reproduces the novelty and external-support tables;
5. emits fresh reports and checksums; and
6. fails closed when inputs, schemas, counts, or seeds differ.

### Stage 4 — Independent audit

After the clean rerun:

- compare every regenerated output to the current package;
- explain every discrepancy rather than silently replacing values;
- rerun the official MDC checker and package audit;
- build a new expert-review bundle; and
- provide the recovered/reconstructed code to external reviewers.

## Stop rules

Do not:

- submit the current manuscript to a journal;
- formally report the shower to the MDC;
- claim that code and data reproduce the complete analysis;
- mint a reproducibility DOI for the current partial branch;
- invite experts to approve a supposedly reproducible pipeline without disclosing the gap;
- reconstruct code by copying numerical targets from reports and then present the match as independent reproduction; or
- relax rules when a clean rerun disagrees with the current result.

A reconstruction may use the reports to recover documented definitions, but validation must rely on original inputs, frozen rules, and independent checks—not tuning to reproduce target numbers.

## Current allowed claim

> GhostStream has an internally consistent, extensively audited results package for a high-confidence uncatalogued April meteor-stream candidate. The core GMN discovery and validation software is not presently preserved in the branch, so full computational reproducibility remains an unresolved prerequisite for journal or formal MDC submission.

## Resolution gate

This audit can be closed only when all of the following are true:

- [ ] core analysis source code is committed;
- [ ] exact input manifests and hashes are committed or archived;
- [ ] environment and seeds are documented;
- [ ] a clean end-to-end rerun regenerates the 95-member lookup;
- [ ] primary statistics reproduce within prespecified tolerances;
- [ ] discrepancies are documented;
- [ ] the persistent CI workflow runs the reproducibility checks;
- [ ] external reviewers receive the code-inclusive bundle; and
- [ ] the manuscript/data-availability statements are updated from “planned” to factual.
