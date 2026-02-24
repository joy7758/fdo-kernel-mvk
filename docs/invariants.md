# Structural Invariants — MVK v0.2

This document defines the non-negotiable structural invariants
for the Minimum Verifiable Kernel (MVK).

An implementation violating any invariant
is not considered causally closed.

---

## 1. Object Identity Invariant

The executable object must possess a deterministic identity:

    object_id = H(metadata || τ || S0)

Where:

- metadata is fully serialized and sorted
- τ is the declared drift threshold
- S0 is the initial state
- H is SHA-256

Any modification of metadata, τ, or S0
must change object_id.

---

## 2. Constraint Binding Invariant

All constraints influencing execution (including τ)
must be cryptographically bound into the object identity.

Constraints must not exist as mutable external parameters.

---

## 3. State Determinism Invariant

For all transitions:

    S_{n+1} = P(S_n)

The transition function P must be deterministic
and depend only on explicitly declared inputs.

No implicit environmental dependencies are allowed.

---

## 4. Checkpoint Integrity Invariant

Checkpoint chain must be constructed as:

    C0 = H(object_id || H(S0))
    Cn = H(C_{n-1} || H(Sn))

Any tampering of states or object definition
must invalidate the chain.

---

## 5. Replay Completeness Invariant

Replay verification must:

1. Recompute object_id
2. Recompute all state transitions
3. Recompute all drift values
4. Recompute checkpoint chain
5. Compare final checkpoint hash

Verification must fail closed.

---

If all invariants hold,
the object is considered causally closed.
