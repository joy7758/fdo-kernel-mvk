# Runtime Trace → Execution Integrity → Audit Evidence Stack

This note is a boundary map, not a claim that the current repository implements the whole stack.

For public routing, start with
[digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture)
as the architecture hub. From there, use `fdo-kernel-mvk` for execution
integrity, `agent-evidence` for concrete evidence packaging, and `aro-audit`
for post-execution review.

It clarifies the relationship between:

- agent runtime systems
- runtime traces
- execution integrity verification
- audit evidence packaging

## Conceptual stack

Agent Runtime Layer  
↓  
Execution Trace Layer  
↓  
Execution Integrity Layer  
↓  
Audit Evidence Layer

### Agent Runtime Layer

This is where execution happens.

Examples:

- CrewAI
- LangChain agents
- AutoGen
- other orchestration frameworks

These systems may emit runtime events, tool calls, and framework-native logs.

### Execution Trace Layer

This layer captures what happened during execution.

Possible contents:

- ordered steps
- tool calls
- inputs and outputs
- state transitions
- framework-native trace data

This layer answers:

**what actually happened**

### Execution Integrity Layer

This layer checks whether a trace or state transition record is internally trustworthy.

Current MVK scope:

- local JSON object + local trace file
- SHA-256 based `current_hash`
- linked `previous_hash`
- object `checksum`
- deterministic replay verification

Current non-goals in this repository:

- digital signatures
- external anchoring
- live framework trace ingestion
- proof systems

This layer answers:

**can we verify the claimed execution state transition boundary?**

### Audit Evidence Layer

This layer packages verified execution facts into portable evidence objects that can be consumed by audit or compliance tooling.

This repository points toward that layer, but does not yet implement a full portable audit object protocol.

## Current repository boundary

The current MVK code proves a narrow claim:

- a local object can be normalized
- its checksum can be recomputed
- replay can detect tampering against the stored trace boundary

The current MVK code does **not** prove:

- that a live agent runtime emitted the trace
- that the checksum is identity-bound like a digital signature
- that the record was externally anchored
- that the output is already a complete audit evidence object

## Why this separation matters

Keeping these layers separate prevents scope inflation:

- runtime systems focus on execution
- integrity layers focus on verification
- audit layers focus on portability and downstream review
