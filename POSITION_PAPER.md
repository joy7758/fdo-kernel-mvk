# Position Statement — MVK v0.2

This document clarifies the structural scope and design intent of MVK v0.2.

MVK v0.2 binds:

    metadata + threshold (τ) + initial_state (S0)

into a deterministic object identity:

    object_id = H(metadata || τ || S0)

The checkpoint chain is anchored from:

    C0 = H(object_id || H(S0))

and extended as:

    Cn = H(Cn-1 || H(Sn))

## Design Rationale

The purpose of v0.2 is to establish object-level causal closure
between:

- declared constraints
- initial state
- state transitions

This ensures that:

- constraints cannot be altered post-hoc
- initial conditions are immutable
- replay verification is complete
- tampering at any structural layer fails closed

## Explicit Non-Goals

v0.2 does NOT bind:

- implementation version of transition function P
- code signatures
- runtime environment
- hardware characteristics

These concerns belong to higher-layer models
and are intentionally excluded to preserve minimality.

## Why Minimal Binding?

The objective of MVK is structural demonstrability,
not production hardening.

Binding additional layers (e.g., implementation fingerprinting)
would increase complexity and move beyond
the minimal executable object model.

v0.2 therefore serves as a formally minimal,
causally closed executable object kernel.
