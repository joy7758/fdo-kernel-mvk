# Success-Side Execution Traces

This note captures a roadmap direction for MVK:

**execution traces should not only explain failures, but also explain successful runs that produce the wrong deliverable.**

## Why this matters

Many current systems already capture failure traces:

- exception type
- traceback
- stderr
- task failure distribution

That is useful, but incomplete.

A major missing layer is the **success side**:

A run may technically complete, but still produce the wrong artifact.

Examples:

- a planning document instead of the expected WAV file
- a valid JSON with the wrong semantic content
- a completed tool chain that produced the wrong output
- a generated code path that ran successfully but solved the wrong task

In these cases, a failure log does not exist, but the execution path still needs to be reconstructed.

## Core idea

MVK should eventually support **success-side execution traces** for runs that are:

- technically successful
- operationally wrong
- semantically misaligned with the intended task

This extends the current execution-integrity direction.

## Questions this should help answer

For a "successful but wrong" run, reviewers should be able to inspect:

- what code or tool chain ran
- what imports or tools were used
- what intermediate outputs were produced
- what evidence the system saw
- what the system inferred
- why the final artifact drifted from the intended goal

## Difference from ordinary failure logging

Failure logging answers:

**why did the run crash?**

Success-side tracing answers:

**why did the run succeed but still produce the wrong thing?**

That distinction is important for real agent systems.

## Relation to MVK

Current MVK direction already focuses on:

- append-only execution traces
- deterministic state transitions
- replay verification
- explicit tool and event records

This roadmap note suggests extending that toward:

- successful-run trace inspection
- artifact-level output mismatch analysis
- human-auditable explanation of decision paths

## Example scenarios

### Scenario 1
Expected output:
- WAV file

Actual output:
- planning document

Trace need:
- what code path executed
- whether the system actually entered the synthesis step
- whether the task intent drifted before execution

### Scenario 2
Expected output:
- database update

Actual output:
- successful API calls, but no meaningful external state change

Trace need:
- side-effect diff
- action intent
- environment snapshot before and after

## Suggested rollout

### v1
Keep current kernel behavior unchanged.

### v1.1
Document the distinction between:
- failure traces
- success-side execution traces

### v2
Add example trace schemas for:
- artifact mismatch
- wrong-but-completed runs
- side-effect diff after successful execution

## Short formulation

Failure traces explain crashes.

Success-side execution traces explain **wrong completions**.

Both are necessary for agent auditability.
