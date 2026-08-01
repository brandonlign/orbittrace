# GhostStream external expert outreach

Prepared: 2026-08-01

## Objective

Obtain three distinct kinds of review without mass-emailing the meteor community:

1. **GMN methodology and data-use review** — confirm trajectory conventions, catalogue limitations, acknowledgments, and whether GMN collaborators should be invited.
2. **Independent meteor-stream review** — challenge the antihelion interpretation, orbit conventions, duplicate risk, and evidentiary threshold.
3. **IAU MDC procedural review** — confirm the submission record, lookup-table format, duplicate/nomenclature procedure, and whether the package is ready for provisional submission.

The contacts below are public professional contacts from official institutional or project pages. No message has been sent.

## Recommended sequence

### Step 1 — Denis Vida: GMN methodology and collaboration review

**Why first:** Denis Vida founded and coordinates the Global Meteor Network and is currently an Adjunct Research Professor and Research Scientist at Western University. He can assess whether the public GMN catalogue has been used correctly, whether any server-side or Level 2 validation is practical, and what acknowledgment/authorship process is appropriate.

**Public professional contact:** `dvida@uwo.ca`

**Subject:** Request for technical review of a candidate meteor stream found in public GMN trajectories

**Draft message:**

> Dear Dr. Vida,
>
> My name is Brandon Li, and I am a high school student conducting a computational meteor-stream project using the public Global Meteor Network trajectory catalogues.
>
> A blind search identified a compact annual late-April candidate that recurs in GMN data from 2022–2026. I froze the solution before historical validation, excluded orbital elements from the final activity selection, tested it inside an expanded antihelion background, and evaluated measurement uncertainty, geographic station splits, and 81 prespecified analysis settings. The current package contains 95 confirmed GMN members. Historical CAMS and SonotaCo data provide additional support.
>
> Before contacting the IAU Meteor Data Center, I would be grateful for a critical GMN-specific review. The most important questions are whether the trajectory/radiant conventions and catalogue-level quality controls are appropriate, whether the candidate could reflect a GMN processing or association artifact, and what acknowledgment, data-use, or collaborator process GMN would expect.
>
> I have prepared a concise review packet, manuscript draft, 95-row lookup table, frozen candidate record, and complete reproducibility audit. The package has passed the official MDC consistency programs and a 111-check internal consistency audit, but I am not treating those mechanical checks as scientific approval.
>
> Would you be willing to review the packet, or recommend a GMN colleague who should? I would especially value direct criticism or a no-go judgment if the analysis is not scientifically defensible.
>
> Thank you for your time.
>
> Best regards,  
> Brandon Li  
> John L. Miller Great Neck North High School

**Attach or link initially:**

- `EXPERT_REVIEW_PACKET.md`
- `mdc/MANUSCRIPT_DRAFT.md`
- `mdc/GhostStream_April_95_GMN_lookup.csv`
- `candidate_solution.json`

Do not initially attach the full branch archive unless requested.

### Step 2 — Pavel Koten: independent meteor-stream and orbit review

**Why second:** Pavel Koten is the current President of IAU Commission F1, heads the Meteor Physics Group at the Astronomical Institute of the Czech Academy of Sciences, and studies video meteor trajectories, meteor-shower activity, and processing methods. His group is institutionally separate from GMN and has published on systematic differences among video meteor orbit catalogues.

**Public professional contact:** `pavel.koten@asu.cas.cz`  
**Alternate institutional listing:** `koten@asu.cas.cz`

**Subject:** Request for independent review of an uncatalogued late-April meteor-stream candidate

**Draft message:**

> Dear Dr. Koten,
>
> My name is Brandon Li, and I am a high school student working on a computational search for weak meteor streams in public video-meteor catalogues.
>
> A blind search of Global Meteor Network trajectories identified a late-April candidate with 95 confirmed GMN members across 2022–2026. The final activity test uses radiant, speed, and solar longitude but no orbital elements; orbital compactness is tested afterward against source- and time-matched null samples. The signal also survives measurement-error cloning, disjoint GMN geographic splits, and 81 prespecified analysis settings. CAMS and SonotaCo provide a smaller historical sample.
>
> I am seeking an independent expert review before any IAU Meteor Data Center submission. The central questions are whether the candidate is genuinely distinct from the antihelion complex or a known minor shower under another convention, whether the coordinate and node/perihelion transformations are correct across catalogues, and whether the robust membership solution and arithmetic-mean MDC record are represented appropriately.
>
> I have prepared an expert review packet that explicitly lists the strongest objections and all current limitations. A checksum-locked comparison against the current MDC catalogue found no hard duplicate or radiant–speed–activity near match, but I understand that an automated catalogue screen cannot replace expert knowledge of the literature or alternate conventions.
>
> Would you be willing to review the packet, or suggest another independent meteor-stream specialist? A critical no-go assessment would be just as valuable as support.
>
> Thank you for considering this request.
>
> Best regards,  
> Brandon Li  
> John L. Miller Great Neck North High School

**Attach or link initially:**

- `EXPERT_REVIEW_PACKET.md`
- `mdc/MANUSCRIPT_DRAFT.md`
- `mdc/GhostStream_April_mean_submission.json`
- `mdc/calculation_audit.json`
- `mdc/LIVE_MDC_NOVELTY_REFRESH.md`

### Step 3 — IAU Meteor Data Center shower contacts: procedural and duplicate review

**Why third:** The MDC identifies Mária Hajduková and Regina Rudawska as the contacts for reporting new meteor showers and for reports that establish showers in the Working List. This should be approached after incorporating GMN and independent-review corrections, so the message is a focused pre-submission inquiry rather than an attempt to use the MDC as the first scientific reviewer.

**Official contact:** `mdc_showers@ta3.sk`

**Subject:** Pre-submission inquiry: draft data package for an uncatalogued late-April meteor-stream candidate

**Draft message:**

> Dear Dr. Hajduková and Dr. Rudawska,
>
> I am preparing a possible IAU Meteor Data Center submission for an uncatalogued annual late-April meteor-stream candidate identified in public Global Meteor Network trajectories.
>
> The current draft package contains a 95-event lookup table, a mean-data record, and a manuscript. The exact committed mean record has passed both the distributed official MDC consistency binaries and a fresh compilation of the official Fortran source with zero flagged errors. A checksum-locked refresh of the MDC catalogue version 2026-06-25 found no hard duplicate, activity-compatible radiant–speed near match, or orbit-incomplete near match under the frozen screen.
>
> Before treating this as a formal submission, I would appreciate procedural guidance on three points:
>
> 1. whether the current JSON mean-data structure or the legacy text record is preferred;
> 2. whether calculating the submitted semimajor axis from the submitted rounded q and e is the correct precision convention; and
> 3. whether you see an obvious catalogue or historical duplicate that should be resolved before submission.
>
> The candidate is supported by five GMN years and smaller CAMS/SonotaCo samples, but it is not being described as established or officially recognized. The manuscript and review packet explicitly disclose the antihelion-source question, post-hoc external pooling, unresolved speed drift, and incomplete/stale currently linked EDMOND files.
>
> I would be grateful to know whether the package is in the appropriate form for a provisional shower report and what corrections are required before formal delivery.
>
> Best regards,  
> Brandon Li  
> John L. Miller Great Neck North High School

**Attach or link:**

- `mdc/GhostStream_April_95_GMN_lookup.csv`
- `mdc/GhostStream_April_mean_submission.json`
- `mdc/GhostStream_April_mean_legacy.txt`
- `mdc/MANUSCRIPT_DRAFT.md`
- `EXPERT_REVIEW_PACKET.md`
- `mdc/MDC_OFFICIAL_CHECKER_REPORT.md`

## Optional fourth reviewer — only if requested

### Paul Wiegert: orbital dynamics and parent-body interpretation

**Public professional contact:** `pwiegert@uwo.ca`

Paul Wiegert is a Western University professor whose research includes asteroids, comets, meteor showers, meteoroid streams, and celestial mechanics. He is appropriate for orbital/dynamical interpretation, but he is not the first reviewer needed because no credible parent-body candidate currently exists and he is in the same institutional meteor environment as the GMN team.

Contact him only if the first reviewers recommend a dynamical analysis or identify a plausible parent body.

## Sending rules

- Do not send all three messages simultaneously.
- Send the GMN review first and incorporate substantive corrections.
- Then request the independent Commission F1 review.
- Contact the MDC only after the scientific packet has been revised from those reviews, unless the question is strictly about file format.
- Do not describe the candidate as a discovery, named shower, established shower, or IAU submission in the subject line.
- Keep the first email short; provide the full repository or data archive only if requested.
- Record the exact packet commit and file hashes sent to each reviewer.
- Never interpret silence as approval.
- Preserve all critical feedback, including a no-go verdict, in the project record.

## Public-source basis for the contact order

- The official GMN and Western University pages identify Denis Vida as GMN founder/coordinator and list his Western professional email.
- The IAU lists Pavel Koten as the current President of Commission F1; the Czech Academy meteor group identifies him as its head and publishes his professional email.
- The official MDC contact page identifies Mária Hajduková and Regina Rudawska as the contacts for new meteor-shower reports and lists `mdc_showers@ta3.sk`.
- The IAU Meteor Shower Nomenclature Working Group includes Hajduková, Rudawska, Koten's Commission F1 colleagues, and Denis Vida, reinforcing the need to separate GMN-method review from formal MDC procedure.
