# fdo-kernel-mvk

This repository is a minimal demonstrator for causal closure and replay verifiability. No functional expansion will be accepted.

Architecture index (Layer 0/1/2): `../edo-architecture-index` (replace with public URL after publishing).

## Minimum Verifiable Kernel

`fdo-kernel-mvk` is a minimal implementation of an executable digital object model with replay verification. The kernel is intentionally constrained to deterministic state transitions, deterministic drift checks, and a hash-linked checkpoint chain.

This repository demonstrates causal closure: every accepted state is produced by the declared transition function, bounded by a fixed drift threshold, and anchored in an auditable checkpoint chain.

## Scope Constraints

- No external dependencies.
- Python standard library only.
- Deterministic execution only.
- Core kernel code remains under 200 lines.
- Functional expansion is explicitly forbidden for this demonstrator.

## Repository Layout

- `docs/formal_model.md`: formal tuple, invariants, and verification criteria.
- `kernel/object_model.py`: MEDO tuple and deterministic transition function.
- `kernel/drift.py`: deterministic L1 drift metric.
- `kernel/gate.py`: conformance gate and failure type.
- `kernel/checkpoint.py`: checkpoint chain construction.
- `kernel/verify.py`: replay verifier for transition, drift, and checkpoint integrity.
- `demo.py`: deterministic run, single drift trigger, rollback, and audit bundle output.

## Run

```bash
python3 demo.py
python3 kernel/verify.py
```

`python3 demo.py` generates `audit_bundle.json` as a runtime artifact.

Expected verifier output:

```text
VERIFIED: Causally Closed Object
```
