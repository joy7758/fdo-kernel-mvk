# MVK Architecture (Minimal)

This document describes the minimal execution and verification architecture of `fdo-kernel-mvk`.

## ASCII Overview

```text
+----------------------+        +-----------------------+
|  Object Identity     |        |  Checkpoint Chain     |
|  (metadata, tau, S0) |        |  hash-linked states   |
+----------+-----------+        +-----------+-----------+
           |                                |
           v                                v
+----------------------+        +-----------------------+
|  Drift Gate          |------->|  Independent Verify   |
|  deterministic bound |        |  replay + integrity   |
+----------------------+        +-----------------------+
```

## Module Summary

### 1) Object Identity
- Inputs: `metadata`, `threshold (tau)`, `initial_state (S0)`.
- Output: `object_id` as a deterministic hash.
- Purpose: bind object definition and policy into one stable identifier.
- Security effect: if policy or initial state changes, identity changes.

### 2) Checkpoint Chain
- Inputs: `object_id` and accepted state sequence.
- Output: hash-linked checkpoints and final checkpoint digest.
- Purpose: provide append-only structural evidence for state evolution.
- Security effect: any checkpoint or state rewrite breaks chain replay.

### 3) Drift Gate
- Inputs: previous state, candidate next state, threshold.
- Output: allow or reject transition.
- Purpose: enforce deterministic drift bound during execution.
- Security effect: out-of-bound transitions are rejected and rollbackable.

### 4) Independent Verification
- Inputs: `audit_bundle.json`.
- Checks:
  - identity recomputation
  - transition replay determinism
  - drift sequence and bound conformance
  - checkpoint chain integrity
  - drift event consistency
- Output: `VERIFIED: Causally Closed Object` or `TAMPER DETECTED`.

## Why This Is Minimal
- No external dependencies.
- Python standard library only.
- Deterministic transition and replay.
- Verification is independent from runtime generation.

## Scope Boundary
- This repository is a stable minimal kernel demonstration.
- It is not a production orchestration system.
- Kernel semantics are intentionally frozen for reproducibility.
