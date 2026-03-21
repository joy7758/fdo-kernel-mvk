# MVK Boundary

`fdo-kernel-mvk` is the execution-integrity layer in the Digital Biosphere Architecture.

## Canonical order

Persona -> Interaction -> Governance -> Execution Integrity -> Audit

## What this layer does

- proves what actually happened during execution
- constrains deterministic state evolution
- supports replay-verifiable integrity checks
- fails closed when trace-bound conformance breaks

## What this layer does not do

- author governance policy
- decide what should be allowed before execution
- package downstream audit receipts
- act as the architecture hub

## Upstream and downstream

- upstream: `token-governor` decides what should be allowed
- this repo: MVK proves what actually happened
- downstream: `agent-evidence` and `aro-audit` consume execution evidence for review and receipts
