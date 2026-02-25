# fdo-kernel-mvk

A minimal executable kernel for causally closed digital objects.
A deterministic reference for anti-tamper replay verification.
A stable demonstration target for reproducible auditing.

**Stable Structural Anchor: v0.2.0**

## Problem

AI execution pipelines can be tampered after generation: state rewrites, policy edits, or checkpoint mutation may go unnoticed. MVK addresses this by binding identity (`metadata + threshold + initial_state`) and enforcing replayable deterministic verification over states, drifts, and checkpoints.

## Run In 3 Steps

```bash
python3 demo.py
python3 kernel/verify.py
python3 tests/test_reproducibility.py
```

`demo.py` generates `audit_bundle.json`.

## Expected Output Example

```text
$ python3 kernel/verify.py
VERIFIED: Causally Closed Object

$ python3 tests/test_reproducibility.py
TAMPER DETECTED
reproducibility checks passed
```

## Repository Layout

- `docs/architecture.md`: minimal architecture and module boundaries.
- `docs/formal_model.md`: formal tuple, invariants, and verification criteria.
- `docs/invariants.md`: structural invariants for MVK v0.2.
- `docs/walkthrough.md`: reproducible verification and tamper checks.
- `kernel/object_model.py`: tuple and deterministic transition.
- `kernel/drift.py`: deterministic L1 drift metric.
- `kernel/gate.py`: conformance gate and failure type.
- `kernel/checkpoint.py`: checkpoint chain construction.
- `kernel/verify.py`: independent replay verifier.
- `demo.py`: deterministic run and audit bundle output.

## Citation

If referencing this work, cite:

fdo-kernel-mvk v0.2.0  
Minimum Verifiable Kernel for Executable Digital Objects  
GitHub: https://github.com/joy7758/fdo-kernel-mvk
