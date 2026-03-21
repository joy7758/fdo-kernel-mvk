# Governance Runtime vs Execution Integrity

This document summarizes an architectural alignment between two layers
emerging in modern AI agent systems:

1. Governance Runtime
2. Execution Integrity Kernel

The distinction became clear during discussions with the DOF
(Deterministic Observability Framework) project.

---

## Layer Separation

Modern agent systems often mix multiple responsibilities inside a single framework.

However the stack becomes clearer if we separate five concerns:

identity / persona
interaction semantics
governance / verification
execution integrity
audit

Governance answers:

**what actions are allowed**

Execution integrity answers:

**what actually happened during runtime**

---

## Governance Runtime

The governance layer sits upstream of execution.

Key ideas:

- policy enforcement before execution
- deterministic verification gates
- rule based hallucination detection
- AST validation for generated code
- formal verification hooks

Instead of reading execution traces during enforcement,
the governance layer operates on current requests and decisions.

## Execution Integrity (MVK)

The MVK kernel focuses on deterministic runtime reconstruction.

Core properties:

- append-only execution trace
- deterministic state transitions
- replay verification
- explicit non-deterministic boundaries

Typical event chain:

state_before
-> action_decision
-> tool_call
-> tool_result
-> state_after

Each transition is hashed:

H_i = hash(state_before_i || event_i || state_after_i)

The final run hash is derived from the ordered sequence of transition hashes.

This allows deterministic replay verification.

---

## Binding Point

The two systems connect through cryptographic binding.

Execution Kernel:

produces deterministic runtime traces

Governance Runtime:

produces attestations about whether actions were allowed

Binding occurs through:

execution context hash
governance decision hash
attestation proof hash

This creates a verifiable relationship between:

what governance approved
what actually happened

---

## Conceptual Stack

The emerging agent runtime architecture may look like:

Persona
-> Interaction
-> Governance Runtime
-> Execution Integrity Kernel
-> Audit

---

## Why this separation matters

Separating execution history from enforcement prevents a class of attacks
where trace manipulation could influence runtime decisions.

Execution traces remain immutable records.

Governance systems enforce policy independently.

---

## Future Work

Possible integration experiments:

- mapping MVK events to DOF execution steps
- binding MVK run hashes to governance attestations
- cross-verifying replay traces with governance proofs
