# Preregistered benchmark for the GhostStream validation protocol

## Status

**Protocol only. Not yet executed.**

This benchmark is designed to test whether the prospectively frozen GhostStream workflow improves reliability relative to simpler analysis strategies. Its purpose is not to strengthen the April candidate by changing its thresholds.

## Primary question

Does separating discovery from untouched confirmation reduce false candidate survival while preserving useful recovery of real weak streams?

## Compared workflows

### A. Pooled workflow

All available GMN years are searched and evaluated together. Candidate parameters and significance are obtained from the same pooled sample.

### B. Same-data gated workflow

The existing GhostStream discovery and downstream gates are applied, but discovery and validation use the same years.

### C. Frozen temporal-holdout workflow

Candidate generation uses a designated discovery period. The candidate center, feature scales, drift treatment, activity interval, quality rules, and pass/fail gates are then locked before evaluation in designated untouched years.

### D. Frozen holdout plus external replication

Workflow C is followed by an unchanged-template test in a separate meteor catalogue. The external result is classified as pass, corroboration, or supplementary using rules frozen before that catalogue is opened.

## Evaluation cases

### Known-shower controls

Use the existing Lyrid, Eta Aquariid, and Southern Delta Aquariid controls. Discovery and holdout years must be fixed before rerunning. Recovery is measured against the established shower labels already used by the project.

### Injected weak streams

Use the existing 20-, 40-, and 80-member injection families in real sporadic backgrounds. Injection locations, widths, and random seeds must be fixed before comparison. The same injections are evaluated under every workflow.

### Null controls

Use source-matched sporadic regions and month/year combinations that contain no eligible established shower under the fixed MDC exclusion rules. Null regions are selected without inspecting candidate-survival outcomes.

The April GhostStream candidate is excluded from choosing thresholds or benchmark success criteria.

## Fixed outputs

For each workflow and case, record:

- candidate count entering the validation stage;
- candidate count surviving all applicable gates;
- known-shower recall;
- injection recovery by injected member count;
- null candidate-survival rate;
- median and 90th-percentile orbital compactness of survivors;
- number of parameter changes made after discovery, which must be zero for workflows C and D; and
- compute time.

## Primary comparison

The primary endpoint is the difference in null candidate-survival rate between workflow A and workflow C.

The main secondary endpoint is the difference in known-shower and injection recovery between workflow A and workflow C.

Workflow D is descriptive unless enough independent-catalogue controls exist for a powered comparison.

## Interpretation rules

### Methods contribution supported

A methods contribution is supported only if the frozen holdout workflow produces a clearly lower null-survival rate than the pooled workflow while retaining practically useful recovery across known showers and injections. The size of the improvement and its uncertainty must be reported; crossing an arbitrary p-value alone is insufficient.

### Rigorous validation only

If the holdout workflow lowers recovery without a clear reliability gain, or if the comparison is underpowered, the protocol remains a rigorous validation design rather than a demonstrated new method.

### Negative result

If the pooled workflow performs as well as or better than the frozen workflow on false survival and recovery, no methodology-novelty claim is allowed. The result must be retained as a negative method-control outcome.

## Freeze and governance

Before execution, commit:

- exact discovery and holdout years;
- exact control and null regions;
- injection files and seeds;
- all thresholds and comparison metrics;
- the executable entrypoint; and
- a hash manifest of inputs and configuration.

After execution, no window, threshold, control, exclusion, or success criterion may be altered to improve the comparison. Any later redesign is a new exploratory study and must use new untouched controls.
