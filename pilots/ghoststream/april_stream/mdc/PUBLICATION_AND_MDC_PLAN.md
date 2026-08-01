# GhostStream publication and IAU MDC strategy

Prepared: 2026-08-01

## Decision

**Do not submit the current package to either a journal or the IAU Meteor Data Center yet.**

The internal scientific and package checks are complete, but the principal remaining barriers are external:

1. GMN methodology/data-use review;
2. independent meteor-stream and duplicate-shower review;
3. authorship, acknowledgment, and corresponding-author decisions; and
4. a journal-specific rewrite and disclosure audit.

The recommended publication path after those reviews is:

1. **Default target: Planetary and Space Science — full-length Research Paper**
2. **Conditional stretch target: MNRAS — full Paper, not Letter**
3. **Specialized fallback: WGN, the Journal of the International Meteor Organization**

The journal must be chosen before formal MDC submission. Formal MDC submission should then be coordinated with the selected journal rather than started months earlier.

## Why this is the recommended order

### 1. Planetary and Space Science is the best default target

Planetary and Space Science directly covers solar-system science, celestial mechanics, small bodies, interplanetary dust, and related observational work. It has published dedicated meteoroid/meteor research collections. The GhostStream paper is long, method-heavy, and focused on a meteor-stream candidate rather than a broadly transformative astrophysical result; that is a more natural fit here than a short high-impact astronomy Letter.

The journal currently supports both subscription publication and optional open access. Under Elsevier's standard hybrid model, the subscription route does not require an open-access article processing charge; the exact journal option must still be confirmed at submission because publishing terms can change.

**Use this route when:**

- the GMN reviewer confirms that the catalogue and processing assumptions are defensible;
- the independent reviewer finds no credible duplicate or fatal antihelion objection;
- at least one professional meteor scientist is willing to provide substantive review and, only if contribution warrants it, coauthorship;
- the manuscript is rewritten into a normal journal article rather than a project dossier; and
- the authors prefer a conventional peer-reviewed venue without depending on an APC waiver.

**Main risk:** the editor may judge a single candidate stream and its validation as too specialized or insufficiently broad. The paper must therefore emphasize the generalizable source-preserving search and validation design, not only the existence of one candidate.

### 2. MNRAS is a conditional stretch target, not the default

MNRAS accepts original astronomy and astrophysics research from any author regardless of affiliation or qualifications. Its minimum standard, however, requires clear novelty, significance, broad field contribution, and strong presentation. The current work might meet that standard only if expert review confirms that the stream is genuinely new and that the method contributes beyond a catalogue-specific candidate report.

Submit as a **Paper**, not a Letter:

- MNRAS Papers have no formal page limit but must be concise.
- Letters are limited to five pages and are intended for results with immediate and significant impact.
- GhostStream's source-preserving null, historical replication, bootstrap, specification curve, catalogue audit, and provenance limitations cannot be explained responsibly in five pages.

MNRAS is fully open access. The listed 2025/26 APCs are:

- Paper: **£2,356** for non-members;
- Letter: **£1,122** for non-members; and
- 20% discount for eligible RAS members.

Read-and-publish institutional coverage and discretionary partial/full waivers may be available. A discretionary waiver request must be submitted at the same time as the manuscript but kept separate from editorial review and omitted from the scientific cover letter.

**Use this route only when all of the following are true:**

- both first-stage expert reviews are strongly positive;
- the reviewers judge the method and discovery significant beyond the narrow meteor-catalogue community;
- a qualified professional contributor accepts responsibility for the relevant scientific components and qualifies for authorship, or the reviewers explicitly consider the student-led authorship adequate;
- APC funding, an institutional agreement, or written waiver approval is realistically available; and
- the manuscript is shortened and recast around one central methodological/scientific argument.

**Do not choose MNRAS merely for prestige.** A desk rejection would consume time while the MDC one-year publication clock is running if formal MDC submission had already occurred.

### 3. WGN is the field-specific fallback and may be the fastest defensible route

WGN is the Journal of the International Meteor Organization. It regularly publishes meteor-shower, orbit, video-network, and methodological studies, and the official MDC procedure explicitly recognizes WGN as an acceptable publication venue for shower submissions. WGN submissions are sent to its editor and reviewed for scientific content; its papers are indexed in the NASA Astrophysics Data System.

WGN is the recommended route when experts conclude that:

- the candidate is scientifically defensible and appropriate for the MDC Working List;
- the result is important to meteor specialists but not broad enough for a general planetary-science or astronomy journal;
- a focused specialist review is more valuable than maximizing journal prestige; or
- publication certainty and timing matter more than broad reach.

The current official author page does not clearly publish a current APC or submission fee. Confirm costs and current formatting directly with the editor at `wgn@imo.net` before committing to this route.

**Tradeoff:** WGN provides the most direct specialist readership and a practical MDC-compatible publication path, but less visibility outside meteor science.

## Journal decision matrix

| Condition after expert review | Recommended route |
|---|---|
| Reviewers endorse both the discovery and a broadly reusable method; professional scientific support and APC funding/waiver are secured | MNRAS Paper |
| Reviewers endorse the discovery and method, but broader impact or APC certainty is insufficient for MNRAS | Planetary and Space Science Research Paper |
| Reviewers endorse the candidate for the meteor community but view it as too specialized for a broader planetary journal | WGN |
| Reviewer identifies a plausible duplicate, coordinate error, or antihelion artifact | No submission; resolve or close the candidate |
| Reviewer requires a fresh independent reduction before publication | Pause journal/MDC submission and obtain that analysis |
| Reviews conflict materially | Preserve both reviews and obtain a third independent opinion before choosing a venue |

## MDC timing strategy

The MDC requires a mean-data record, one lookup table for the shower, and a manuscript or paper. Its procedure also imposes a one-year publication deadline after initial shower submission; an unpublished shower may be moved to the Removed list.

That clock should not begin while the manuscript is still waiting for its first expert review or while authorship is unresolved.

### Recommended sequence

1. **Complete the GMN review.**
   - Verify public trajectory use, quality controls, coordinate conventions, acknowledgment, and whether a GMN contributor should be invited.
2. **Complete an independent meteor-stream review.**
   - Resolve duplicate risk, antihelion interpretation, orbit convention, and evidence threshold.
3. **Freeze authorship and contributions.**
   - Add only people who make substantive intellectual or analytical contributions.
   - A reviewer is not automatically an author.
4. **Select the journal using the decision matrix above.**
5. **Rewrite the manuscript in the target journal's format.**
   - Do not simultaneously submit to multiple journals.
6. **Request a journal pre-submission opinion when useful.**
   - This is particularly useful for MNRAS or Planetary and Space Science before starting the MDC clock.
7. **Rerun all final checks immediately before external submission.**
   - refresh the live MDC catalogue;
   - rebuild the lookup/mean/checker package;
   - rerun the 111-check consistency audit;
   - regenerate a final checksum-locked bundle.
8. **Submit the journal manuscript and coordinate the formal MDC package near the same stage.**
   - Preferred timing: after the journal has passed initial editorial screening or when a final journal-ready version exists, but before the final accepted version is locked so an MDC-assigned designation/code can be inserted if needed.
9. **Track the one-year MDC publication deadline from the exact formal submission date.**
10. **If the first journal rejects the paper, move promptly to the predetermined fallback.**
   - Do not alter scientific thresholds or overstate the candidate to obtain acceptance.

## Recommended manuscript positioning

The paper should not be framed as merely “we found a new shower.” Its strongest defensible contribution is the complete discovery-and-validation architecture:

- blind candidate generation separated from confirmation;
- source-preserving antihelion null without orbital selection;
- untouched-year confirmation;
- post-selection orbital testing;
- measurement-error cloning;
- year/night cluster bootstrap;
- disjoint geographic replication;
- frozen specification curve;
- historical archive replication with explicit post-hoc labeling; and
- checksum-locked current catalogue and submission-package audits.

The candidate is the scientific result; the validation architecture is what can make the paper useful beyond one shower.

### Claims to retain

- high-confidence uncatalogued annual April meteor-stream candidate;
- repeatable in five GMN years;
- historically supported by CAMS and SonotaCo;
- no current official MDC duplicate under the frozen screen;
- orbitally strong supplementary EDMOND evidence with explicit provenance limitations.

### Claims to avoid

- official IAU discovery;
- established shower;
- official or discoverer-chosen name;
- complete EDMOND v6.01 replication;
- fully independent third-network confirmation;
- detected physical geocentric-speed drift;
- absolute flux, ZHR, or mass index;
- known parent body or demonstrated dynamical origin.

## Authorship and collaboration rules

Authorship must be based on substantive contribution, not prestige, access, or favorable review.

A professional scientist may qualify for authorship by making a significant contribution to one or more of:

- research design or interpretation;
- independent duplicate/coordinate audit;
- new analysis or re-reduction;
- major manuscript revision with intellectual responsibility; or
- acquisition and interpretation of nonpublic GMN Level 2 data.

A person who only reviews the paper, introduces the author to the MDC, or provides general encouragement should be acknowledged rather than added as an author.

Before submission, record:

- contributor roles;
- author order;
- corresponding author;
- GMN acknowledgment language;
- data-use permissions; and
- approval of the exact final manuscript by every author.

## Generative-AI and software transparency

The project used generative-AI assistance extensively during research planning, software development, auditing, and manuscript preparation. This must be disclosed honestly according to the selected journal's current policy.

### MNRAS

MNRAS states that AI tools do not qualify for authorship. Its current instructions require disclosure in the cover letter and in the Methods or Acknowledgments when AI assisted with code, data processing, translation, or manuscript content. The human authors remain fully responsible for every result, citation, and statement.

### Elsevier / Planetary and Space Science

Elsevier's June 2026 journal policy requires a separate declaration immediately before the references when generative AI materially assisted manuscript preparation. The declaration should identify the tool, its purpose, the authors' review/editing, and their full responsibility. AI use in the research process should also be described in Methods when relevant.

### Required project action

Before journal submission, create a complete AI/software provenance statement that distinguishes:

- human scientific decisions and interpretation;
- deterministic analysis code and external scientific software;
- generative-AI assistance with code, search, auditing, organization, and prose;
- independent human validation of outputs; and
- exact commits, data hashes, and checker results supporting the claims.

Do not minimize the role of AI, and do not imply that mechanical audits are independent scientific review.

## Cost and timing risk

| Route | Publication charge risk | Editorial risk | Likely audience | Timing implication |
|---|---|---|---|---|
| MNRAS Paper | High unless waiver/institutional coverage | Highest | Broad astronomy/astrophysics | Do not start MDC clock before initial editorial viability is established |
| Planetary and Space Science | Subscription route can avoid OA APC; confirm current terms | Moderate | Planetary, small-body, meteoroid community | Best default balance of fit, rigor, and cost |
| WGN | Current fee not clearly listed; confirm with editor | Lower if specialist review is positive | Meteor specialists and MDC community | Best fallback for publication inside MDC deadline |

## Stop rules

Do not submit the journal or MDC package if any of the following remains unresolved:

- credible known-shower duplicate;
- incorrect coordinate, node, or perihelion convention;
- GMN data-use or acknowledgment objection;
- authorship dispute;
- missing disclosure of substantive generative-AI use;
- manuscript values that differ from the checksum-locked package;
- final live MDC refresh not completed;
- no realistic publication route within the MDC one-year window; or
- expert conclusion that an independent reduction is mandatory first.

## Immediate next actions

1. Send the GMN technical-review request using `EXPERT_REVIEW_OUTREACH.md` only after Brandon approves the exact message and attachments.
2. Record the sent bundle commit and SHA-256 in `EXPERT_REVIEW_LOG.md`.
3. Incorporate and adjudicate the GMN review.
4. Rebuild the review bundle if any scientific file changes.
5. Send the independent meteor-stream review request.
6. Select the journal only after both reviews.
7. Draft the target-journal manuscript, cover letter, data-availability statement, author-contribution statement, and AI disclosure.
8. Contact the MDC for procedural review after scientific revisions, not as the first scientific reviewer.

## Official sources checked

- IAU Meteor Data Center, reporting new showers: `https://ceresiaumdc.ta3.sk/report-new-shower/`
- IAU Meteor Data Center contacts: `https://ceresiaumdc.ta3.sk/contact/`
- MNRAS Instructions to Authors: `https://academic.oup.com/mnras/pages/general_instructions`
- OUP discretionary waiver policy: `https://academic.oup.com/pages/open-research/open-access/charges-licences-and-self-archiving/apc-waiver-policy/waiver-form`
- Planetary and Space Science journal page: `https://www.sciencedirect.com/journal/planetary-and-space-science`
- Elsevier publishing pricing and access models: `https://www.elsevier.com/about/policies-and-standards/pricing`
- Elsevier generative-AI policy for journals: `https://www.elsevier.com/en-au/about/policies-and-standards/generative-ai-policies-for-journals`
- WGN author guidance: `https://www.imo.net/docs/writingforwgn.pdf`
- WGN journal page: `https://www.imo.net/publications/wgn/`
