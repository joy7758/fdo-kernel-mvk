# Replay Model

MVK models execution integrity as deterministic state evolution plus trace-bound replay validation.

## Deterministic state evolution

- object identity binds metadata, threshold, and initial state
- accepted states are derived through deterministic transitions
- out-of-bound drift fails closed instead of mutating history

## Canonical object checksum

- runtime objects are canonicalized before checksum computation
- checksums bind execution state for integrity verification
- the current SHA-256 usage is an integrity primitive, not an identity signature

## Trace-bound replay validation

- replay recomputes object identity
- replay recomputes state transitions and drift sequence
- replay rebuilds checkpoint chains from the accepted state list
- any mismatch between bundle, state chain, or drift event is treated as tamper
