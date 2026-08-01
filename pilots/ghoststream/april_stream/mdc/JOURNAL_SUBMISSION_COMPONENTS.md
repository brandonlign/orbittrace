# GhostStream journal-submission components

Prepared: 2026-08-01

## Status

**Draft components only — do not submit.**

The scientific package is internally consistent, but external scientific review, authorship, acknowledgment, data-release, and journal selection remain unresolved. Every bracketed field below must be completed before use.

## Working title

**An Uncatalogued Annual April Meteor Stream Identified in Global Meteor Network Trajectories**

This title is accurate without claiming official discovery or established-shower status.

Alternative, if the method becomes the primary contribution:

**A Source-Preserving Blind Search Identifies an Uncatalogued Annual April Meteor-Stream Candidate**

Do not use “new meteor shower,” “discovery of,” an invented shower name, or an IAU designation until the relevant status is formally assigned.

## Recommended article type

- Planetary and Space Science: **Research Paper / full-length article**
- MNRAS: **Paper**, not Letter
- WGN: standard research article under current editor guidance

## Short significance statement

A blind search of public Global Meteor Network trajectories identified a compact annual late-April meteor-stream candidate that recurs in five years. The final validation separates radiant–speed–time activity selection from orbital testing, preserves the structured antihelion background, and survives measurement-error cloning, disjoint geographic splits, a frozen 81-cell specification curve, and historical CAMS/SonotaCo comparison. The work provides both a candidate stream and a reproducible validation framework for weak-stream searches in structured sporadic backgrounds.

## Draft Planetary and Space Science highlights

Elsevier highlights normally require short standalone bullets. Recheck the current journal-specific character limit before submission.

- Blind GMN search finds a recurrent late-April meteor-stream candidate
- Five GMN years pass frozen activity and post-selection orbital tests
- Source-preserving null avoids using orbital elements to select activity
- All 81 prespecified analysis variants support the candidate
- CAMS and SonotaCo provide historical radiant–orbit support

Do not include the EDMOND result in the highlights because its currently linked release is incomplete or stale and its role is supplementary.

## Draft keywords

- meteor streams
- meteor showers
- Global Meteor Network
- video meteor orbits
- antihelion source
- orbital similarity
- weak-signal detection
- reproducible astronomy

Recheck each target journal's keyword limit.

## Journal-neutral cover-letter core

> Dear Editor,
>
> Please consider the manuscript, “An Uncatalogued Annual April Meteor Stream Identified in Global Meteor Network Trajectories,” for publication as a full-length research article in [JOURNAL].
>
> The manuscript reports a blind search of public Global Meteor Network trajectories that identified a compact annual late-April meteor-stream candidate recurring in five GMN years from 2022 through 2026. The analysis was frozen before historical validation. Its final activity test uses radiant, geocentric speed, and solar longitude but no orbital elements; orbital coherence is evaluated afterward against source- and time-matched null samples inside an expanded antihelion background. The candidate survives measurement-error cloning, hierarchical year/night bootstrapping, disjoint geographic station groups, and all 81 prespecified reasonable analysis variants. Smaller CAMS and SonotaCo samples provide historical support.
>
> A checksum-locked comparison against the official IAU Meteor Data Center catalogue version 2026-06-25 found no hard duplicate, activity-compatible radiant–speed near match, or orbit-incomplete near match under the frozen screen. The manuscript nevertheless describes the result only as an uncatalogued candidate. It does not claim official IAU recognition, established-shower status, an official name, absolute flux, a parent body, or a detected geocentric-speed drift.
>
> The exact 95-event lookup table, mean record, analysis code, and reproducibility materials will be archived at [REPOSITORY AND DOI]. The committed mean record passes the current official MDC radiant/orbit consistency programs with zero flagged errors in both the distributed binaries and a fresh compilation of the official source. A separate fail-closed package audit passed 111/111 internal-consistency checks.
>
> This manuscript is original, is not under consideration elsewhere, and has been approved by all authors. [CONFLICT-OF-INTEREST STATEMENT.] [FUNDING STATEMENT.] Substantive use of generative-AI assistance in planning, software development, auditing, and manuscript preparation is disclosed in the manuscript and cover letter; all authors take full responsibility for the submitted content.
>
> We believe the paper is appropriate for [JOURNAL] because [ONE JOURNAL-SPECIFIC SENTENCE].
>
> Thank you for your consideration.
>
> Sincerely,  
> [CORRESPONDING AUTHOR]  
> [AFFILIATION]  
> [EMAIL]  
> [ORCID, IF AVAILABLE]

## Planetary and Space Science journal-specific sentence

> The paper combines small-body orbital analysis, meteor-network observations, and a general validation design for weak meteoroid-stream structure, fitting the journal's scope in meteoroids, interplanetary matter, and solar-system dynamics.

## MNRAS journal-specific sentence

Use only if the external reviewers judge the method and result broadly significant:

> The paper contributes a general source-preserving discovery and confirmation framework for weak astronomical populations in structured backgrounds, demonstrated through a recurrent meteor-stream candidate with independent historical support.

## WGN journal-specific sentence

> The paper directly addresses meteor-shower identification, video-network trajectory analysis, catalogue comparison, and the interpretation of weak stream structure within the antihelion source.

## Draft pre-submission inquiry for Planetary and Space Science

> Dear Editor,
>
> I am seeking a brief pre-submission assessment of whether a full manuscript on a rigorously validated meteor-stream candidate would fit Planetary and Space Science.
>
> The study uses a blind search of public Global Meteor Network trajectories and identifies a compact annual late-April candidate recurring in five GMN years. The validation separates non-orbital activity selection from post-selection orbital testing inside a preserved antihelion background, and includes measurement-error cloning, hierarchical bootstrap uncertainty, disjoint geographic station groups, an 81-cell frozen specification curve, current IAU catalogue screening, and historical CAMS/SonotaCo support.
>
> The paper is not framed as official discovery or established-shower status. Its broader contribution is a reproducible approach to weak meteoroid-stream detection under a structured sporadic background.
>
> Would a full-length Research Paper of this scope be appropriate for editorial consideration? I can provide the abstract or manuscript if useful.
>
> Best regards,  
> [NAME AND AFFILIATION]

A pre-submission inquiry is not peer review or acceptance. Do not start the formal MDC publication clock based only on a positive inquiry response.

## Data-availability plan

The final paper should not claim that all data are newly hosted by the authors when the primary observations remain maintained by external networks.

### Public source data

The data-availability statement should identify:

- GMN public trajectory catalogues used for discovery and validation;
- legacy CAMS orbit catalogue used for historical support;
- permanent SonotaCo annual catalogues used for historical support;
- the Shober shower-removed EDMOND subset and its Zenodo record;
- official IAU MDC shower catalogue snapshot;
- official IAU MDC checker archive; and
- any JPL small-body catalogue/query used in the parent screen.

For every external source, provide:

- official URL or DOI;
- access date;
- exact file or query scope;
- checksum when a stable file was downloaded;
- license or data-use terms when available; and
- whether redistribution in the authors' archive is permitted.

### Author-created reproducibility archive

Before journal submission, create a public, immutable archive containing at minimum:

- analysis and audit code required to reproduce published tables and figures;
- frozen configuration and candidate solution;
- 95-event GMN lookup table;
- permitted derived tables and member manifests;
- package and catalogue checksums;
- environment or dependency specification;
- exact commands for the published workflow;
- final manuscript-linked figures and their generating scripts;
- machine-readable result summaries; and
- a clear statement identifying data that must be redownloaded from the original providers.

Recommended release mechanism:

1. create a clean standalone public repository or release directory containing only GhostStream;
2. tag the exact paper release;
3. archive the release with Zenodo or another long-term repository;
4. obtain a DOI;
5. verify the archived files against the final manuscript; and
6. record the DOI and release hash in the paper and cover letter.

Do not make the entire multi-project private `isef` repository public merely to release GhostStream. It contains unrelated branches, internal development history, temporary workflows, and potentially unnecessary metadata.

## Draft data-availability statement

> The public meteor-trajectory and catalogue data used in this study are available from their original providers: the Global Meteor Network, the CAMS orbit catalogue, the SonotaCo meteor-orbit catalogues, the cited Shober EDMOND Zenodo record, and the IAU Meteor Data Center. Exact source files, access dates, and checksums are listed in the reproducibility archive. The frozen analysis code, configurations, 95-event lookup table, permitted derived data, machine-readable results, and figure-generation scripts are archived at [REPOSITORY DOI]. Data that cannot be redistributed under the original provider's terms can be retrieved from the cited source and verified against the archived checksums.

This wording must be revised after the actual repository DOI and redistribution review exist.

## Draft code-availability statement

> The code used for catalogue parsing, candidate validation, source-preserving activity tests, orbital-null tests, measurement-error cloning, hierarchical bootstrap analysis, geographic replication, specification-curve analysis, catalogue comparison, official-checker reproduction, and package auditing is archived at [REPOSITORY DOI] under [LICENSE]. The archived release identifies the exact commit and dependency environment used for the paper.

Choose a software license only after confirming that the repository contains no code copied from incompatible sources and no provider-restricted material.

## Current author-contribution statement

This is a provisional sole-author statement and must be replaced if another contributor qualifies for authorship.

> **Brandon Li:** Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Visualization, Project administration, Writing – original draft, Writing – review and editing.

Before using this statement, Brandon must personally verify that each listed role accurately describes his responsibility rather than merely the execution of an AI-generated suggestion.

### Rules for adding later authors

- Add a contributor only for substantive intellectual, analytical, data, or manuscript responsibility.
- Record contribution roles before submission.
- Require every author to approve the final manuscript and accept accountability.
- A pre-submission reviewer is not automatically an author.
- A person providing access, general supervision, or prestige alone does not qualify.
- If a professional scientist materially redesigns or reruns the analysis, contribution roles and author order must be reconsidered openly.

## Draft acknowledgment framework

Do not insert names until permission and contribution status are resolved.

> The author thanks the Global Meteor Network and its contributing observers and station operators for making calibrated multi-station trajectory catalogues publicly available. The author also acknowledges the providers and maintainers of the CAMS, SonotaCo, IAU Meteor Data Center, NASA/JPL, and cited EDMOND data products used in this study. The author thanks [REVIEWER NAMES, WITH PERMISSION] for critical scientific comments that improved the analysis. Computational validation used GitHub Actions and the official IAU MDC consistency-checker software.

Required before finalization:

- official GMN acknowledgment language;
- whether network collaborators should be invited as authors;
- formal citations for every data provider;
- permission to name external reviewers; and
- school, mentor, program, or computing acknowledgments if applicable.

## Draft funding statement

Current placeholder:

> This research received no dedicated external funding.

Brandon must confirm whether any school program, research program, cloud credits, paid software, institutional support, mentor grant, or family-funded publication cost requires disclosure.

## Draft competing-interests statement

> The author declares no competing financial or non-financial interests that could have influenced the work.

All authors must confirm this independently. Any relationship with data providers, journal editors, reviewers, or organizations that could reasonably be perceived as relevant should be disclosed rather than silently omitted.

## Ethics statement

> This study analyzes astronomical observations and publicly available catalogue data. It does not involve human participants, personal data, animals, clinical materials, or intervention research.

## Generative-AI declaration

Use the target-journal version in `AI_AND_SOFTWARE_PROVENANCE.md`. The final declaration must state that AI assisted not only prose but also planning, code development, debugging, source discovery, and auditing.

Do not use a declaration that says AI was used only “to improve readability.”

## Suggested reproducibility section for the manuscript

A dedicated subsection should state:

- candidate parameters were frozen before external validation;
- which years were discovery, untouched confirmation, and historical replication data;
- exact random seeds and replicate counts;
- exact data snapshots and checksums;
- software and dependency versions;
- official checker archive hash;
- live IAU catalogue version and hash;
- where the public code release is archived;
- that AI-assisted code and prose were reviewed by the author;
- that automated checks are internal validation rather than independent peer review; and
- which analyses are confirmatory versus explicitly post-hoc or exploratory.

## Suggested reviewer policy

Do not suggest as anonymous reviewers anyone who:

- provided substantive pre-submission review;
- contributed unpublished analysis;
- is being considered for authorship;
- has an unresolved conflict with the project; or
- has already seen confidential reviewer-only material.

If Denis Vida, Pavel Koten, or another expert reviews the packet before submission, disclose that relationship where the journal asks for conflicts or reviewer exclusions. Acknowledgment requires permission.

## Final submission file set

Prepare a target-journal directory containing only:

- manuscript source and PDF;
- title page if separate;
- figures at required resolution and format;
- tables or machine-readable supplements;
- highlights if required;
- graphical abstract only if required and scientifically appropriate;
- cover letter;
- author-contribution statement;
- conflict and funding statements;
- data/code availability statements;
- AI declaration;
- supplementary methods/results;
- exact public repository DOI; and
- final internal hash manifest.

Do not upload internal outreach plans, raw AI chat logs, development-only workflows, superseded reports, or reviewer correspondence unless explicitly requested by the editor.

## Remaining blockers

- [ ] GMN technical review completed.
- [ ] Independent meteor-stream review completed.
- [ ] Journal selected.
- [ ] Authorship and corresponding author finalized.
- [ ] Official GMN acknowledgment/data-use language confirmed.
- [ ] Public reproducibility repository created and licensed.
- [ ] DOI minted and verified.
- [ ] All figures regenerated from the final release.
- [ ] AI tool list confirmed by Brandon.
- [ ] Journal-specific disclosure finalized.
- [ ] Final live IAU MDC refresh rerun.
- [ ] Final package audit rerun after manuscript conversion.
- [ ] Formal MDC timing coordinated with the journal pathway.
