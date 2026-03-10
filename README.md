fdo-kernel-mvk

Minimal Deterministic Execution Kernel (Prototype)

An exploration of execution integrity as a first-class layer in the AI agent stack.

## Digital Biosphere Ecosystem

This repository is part of the **Digital Biosphere Architecture**.

Architecture overview:
[digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture)

Commands:
- make run    -> EXECUTION_OK
- make replay -> REPLAY_PASS
- make tamper -> CONFORMANCE_FAIL (fail-closed)

What it proves:
- Deterministic state evolution
- Canonical object signature verification
- Trace-bound replay validation

## AI Agent Stack Architecture

This repository also explores where execution integrity fits in the broader AI agent stack.

See:
- [AI Agent Stack Architecture](docs/architecture/ai-agent-stack-architecture.md)
- [AI Agent Security Architecture](docs/architecture/ai-agent-security-architecture.md)

```mermaid
flowchart TB
    A[Application] --> B[Agent Framework]
    B --> C[Persona / Identity]
    C --> D[Execution Integrity]
    D --> E[Governance / Verification]
    E --> F[Infrastructure]

    G[User workflow and domain logic] -.-> A
    H[Planning, memory, tools, orchestration] -.-> B
    I[Stable operating profile and capability boundary] -.-> C
    J[Deterministic state, signed traces, replay, conformance] -.-> D
    K[Policy gates, approvals, review, audit] -.-> E
    L[Models, tool hosts, storage, compute] -.-> F
```

Core layers:
- Application
- Agent Framework
- Persona / Identity
- Execution Integrity
- Governance / Verification
- Infrastructure

Key distinction:
- Governance decides what should be allowed.
- Execution integrity proves what actually happened.
