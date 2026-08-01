# GhostStream generative-AI and software provenance

Prepared: 2026-08-01

## Status

**Required pre-submission disclosure record — not yet final.**

This project used generative-AI assistance substantially during research planning, software development, source discovery, auditing, interpretation checks, and manuscript preparation. It would be inaccurate to describe the use as limited to spelling, grammar, or superficial language editing.

The final authors remain responsible for every scientific choice, code path, numerical result, citation, interpretation, and statement submitted for publication. AI tools are not authors, reviewers, or independent validators.

Before submission, Brandon must confirm whether any additional AI systems or coding agents not listed here were used on GhostStream and add them to this record.

## Known generative-AI use

### OpenAI ChatGPT

Working environment: OpenAI ChatGPT, including the GPT-5.6 Thinking model available during the final audit stage.

Known uses included:

- brainstorming and ranking research directions;
- designing candidate-generation, confirmation, null, robustness, and stopping-rule workflows;
- drafting and revising Python analysis and audit scripts;
- debugging code and interpreting execution failures;
- locating official data, catalogue, software, journal, and policy sources;
- drafting scientific reports, the manuscript, review packet, outreach drafts, and package documentation;
- checking consistency across numerical summaries and claim boundaries;
- proposing additional tests and identifying possible confounds;
- operating the GitHub connector to create commits, workflows, reports, and reproducibility artifacts; and
- summarizing mechanical test results.

ChatGPT output was not treated as evidence merely because it was generated confidently. Important factual and scientific claims were tied to primary data, official documentation, deterministic calculations, or explicit external sources. Several AI-proposed statements were corrected or narrowed after later audits, including the description of the currently linked EDMOND files and the submitted semimajor-axis value.

### Other AI tools

The following must be confirmed by Brandon before submission:

- [ ] Whether OpenCode or a model used through OpenCode contributed any GhostStream code or prose.
- [ ] Whether GitHub Copilot, Claude, Gemini, Codex, or another coding assistant contributed.
- [ ] Whether any AI search, transcription, translation, image, or document tool contributed material retained in the paper or repository.
- [ ] Exact model or service names when known.
- [ ] Approximate dates and purposes of use.

Do not omit a tool merely because its output was later edited.

## Human scientific responsibility

The human author is responsible for:

- choosing whether to continue or stop the project;
- accepting, rejecting, or modifying AI-proposed analytical designs;
- deciding the frozen candidate and claim boundary;
- reviewing source provenance and licensing;
- deciding which numerical outputs are scientifically meaningful;
- verifying that no threshold was relaxed to preserve a positive result;
- interpreting conflicting or negative evidence;
- approving all code and manuscript content submitted externally;
- resolving authorship and acknowledgment questions; and
- responding to expert and peer review.

Some analytical designs and implementation approaches were initially proposed with AI assistance. They become part of the scientific work only after they are explicitly defined, executed on the data, checked mechanically, and accepted by the human author. This does not make the AI an author or an independent scientific contributor.

## Deterministic software and reproducibility controls

### Project code

The GhostStream repository contains deterministic Python code for data parsing, candidate evaluation, catalogue matching, null tests, robustness analyses, package audits, and evidence bundling. The exact branch history records the implementation and later corrections.

Key reproducibility controls include:

- frozen candidate parameters before external validation;
- exact-time deduplication rules that do not use candidate orbit for selection;
- untouched-year confirmation;
- source-preserving activity tests without orbital elements;
- post-selection orbit tests;
- 1,000 measurement-uncertainty clone trials;
- 20,000 year/night cluster-bootstrap replicates;
- three disjoint geographic GMN groups;
- an 81-cell frozen specification curve;
- checksum-locked external catalogues and reports;
- fail-closed ZIP, CRC, schema, row-count, and field validation;
- machine-readable candidate and package summaries;
- GitHub Actions execution logs and artifacts; and
- a 111-check package consistency audit.

These controls test computational reproducibility and internal consistency. They do not constitute independent scientific replication.

### Official IAU MDC checker

The current official MDC checker archive was downloaded and checksum-verified. The exact committed mean record was evaluated with:

1. the distributed official Linux binaries; and
2. a fresh GNU Fortran build of the distributed `elements.f` and `radiants.f` source.

Both executable forms produced byte-identical comparison outputs and zero orbital/geocentric error records. This validates internal radiant/orbit consistency under the official tolerances only.

### Software environment

Known software used in the final audit includes:

- Python 3.11;
- Python standard-library modules for CSV, JSON, ZIP, hashing, HTTP retrieval, statistics, and subprocess execution;
- GNU Fortran 13.2 for the official MDC checker source build;
- Git and GitHub Actions;
- official IAU MDC Fortran programs;
- deterministic repository scripts under `pilots/ghoststream/`; and
- standard command-line tools supplied by GitHub's Ubuntu runners.

The manuscript must cite or describe external scientific software and algorithms separately where required. A generic AI disclosure is not a substitute for normal software citation.

## Examples of corrections produced by verification rather than trust

The record should preserve examples where mechanical or source verification changed the project:

1. **EDMOND release description**
   - An initial interpretation treated the surviving annual links as a usable v6.01 series.
   - A later integrity audit found 481,252 linked rows versus 614,758 advertised, zero annual row-count matches, and embedded versions 513/516 rather than 601.
   - The claim was corrected to “currently linked incomplete or stale files,” not a complete v6.01 replication.

2. **Official checker audit trail**
   - An older report displayed slightly different last-decimal orbit values from the committed mean record.
   - The current official checker was rerun on the exact committed mean using both distributed binaries and freshly compiled source.
   - The corrected report supersedes the earlier display values.

3. **Submitted semimajor axis**
   - The earlier draft used `a = 1.420296 AU`, derived from unrounded mean q and e.
   - The submitted q and e were rounded to six decimals, making that a internally inconsistent submitted triplet.
   - The corrected submitted record uses `a = 1.420285 AU = q/(1-e)` at the submitted precision, while preserving the full-precision derivation separately.

4. **Package audit execution**
   - An early workflow piped Python output to `tee` without `pipefail`, masking a script exception.
   - The workflow was changed to fail closed, field-name alias bugs were repaired, and the final package passed 111/111 checks.

These examples demonstrate why AI assistance and passing automation must not be conflated with correctness.

## Data and source verification

Before submission, every source used for a factual or methodological claim must be manually checked against the cited primary document or official catalogue.

Current checksum-locked examples include:

- official IAU MDC full shower catalogue version 2026-06-25;
- official IAU MDC consistency-checker archive;
- 95-row GMN lookup table and submitted mean records;
- live novelty-refresh results;
- current EDMOND linked-release integrity results;
- exact expert-review and package bundles; and
- package-wide file hashes.

AI-generated or AI-suggested references must never be cited without opening and verifying the actual source.

## Manuscript figures and images

Current GhostStream scientific outputs are data tables, plots, and diagrams generated from deterministic analysis code or official source data. No AI-generated scientific image should be submitted as observational evidence.

Before submission, verify and document for every figure:

- source data;
- generating script and commit;
- parameters and random seed, if applicable;
- whether any visual element was generated or altered by AI;
- whether any third-party content requires permission; and
- whether the journal requires original data or source files.

If an AI tool contributed to figure layout or graphical design, disclose that use according to the selected journal's current policy and ensure that no observational content was fabricated or altered.

## Draft disclosure for an Elsevier journal

Place a journal-approved version immediately before the references if submitting to Planetary and Space Science or another Elsevier journal:

> **Declaration of generative AI and AI-assisted technologies in the manuscript preparation process**  
> During the preparation of this work, the author used OpenAI ChatGPT to assist with research planning, software drafting and debugging, source discovery, reproducibility auditing, organization, and manuscript editing. All AI-assisted code, factual claims, references, numerical outputs, and interpretations were reviewed and verified by the author using the cited primary sources, deterministic repository analyses, checksum-locked data, and official scientific software where applicable. The author edited the resulting material and takes full responsibility for the content of the publication. AI tools were not treated as authors or independent scientific reviewers.

Because AI also assisted research design and code development, the Methods or Reproducibility section should additionally describe the relevant use and the validation controls. A declaration only about writing would be incomplete.

## Draft disclosure for MNRAS

A journal-approved version should appear in the Methods or Acknowledgments, and the cover letter should separately disclose substantive AI assistance:

> OpenAI ChatGPT was used as an assistive tool during research planning, software drafting and debugging, source discovery, reproducibility auditing, organization, and manuscript editing. The human author defined and approved the final scientific claims and remains responsible for all code, sources, calculations, interpretations, and prose. AI-assisted outputs were checked using deterministic analyses, primary-source verification, checksum-locked inputs, official IAU MDC software, and a fail-closed package audit. The AI system is not an author and was not treated as an independent scientific reviewer.

Confirm the exact required location and wording against the current MNRAS instructions at the time of submission.

## WGN disclosure

The current public WGN author guidance does not provide a detailed generative-AI template comparable to the current MNRAS and Elsevier policies. If WGN is selected:

1. disclose the substantive AI use to the editor before submission;
2. include a transparent statement in the manuscript unless the editor requests another format;
3. describe AI-assisted research/code development in Methods or a reproducibility statement; and
4. preserve full human responsibility and tool provenance.

Lack of a published template is not a reason to omit disclosure.

## Required pre-submission audit

Before any journal or MDC submission:

- [ ] Brandon confirms every AI tool used.
- [ ] The final manuscript identifies substantive AI assistance honestly.
- [ ] The cover letter follows the selected journal's current policy.
- [ ] All retained AI-assisted code has passed the relevant deterministic tests.
- [ ] All references have been opened and verified by a human author.
- [ ] Every numerical statement matches the final checksum-locked package.
- [ ] Every figure has a source and generation record.
- [ ] No AI-generated scientific observation, reference, quotation, or reviewer statement is presented as real.
- [ ] External expert review is described as external only when it was actually performed by the named human reviewer.
- [ ] The authors approve the final disclosure and accept full responsibility.

## Claim boundary

This document records tool use and validation controls. It does not prove that the science is correct, replace external peer review, or grant permission to submit. Transparency about AI assistance is necessary but not sufficient for publication integrity.
