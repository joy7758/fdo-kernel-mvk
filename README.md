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
- [AI Agent Runtime & Security Stack](docs/architecture/agent-runtime-stack.md)
- [AI Agent Stack Architecture](docs/architecture/ai-agent-stack-architecture.md)
- [AI Agent Security Architecture](docs/architecture/ai-agent-security-architecture.md)
- [AI Agent Runtime OSI Model](docs/architecture/agent-runtime-osi.md)

```mermaid
flowchart TB
    A["Layer 7<br>Application"] --> B["Layer 6<br>Agent Framework"]
    B --> C["Layer 5<br>Persona / Identity"]
    C --> D["Layer 4<br>Execution Integrity"]
    D --> E["Layer 3<br>Governance / Verification"]
    E --> F["Layer 2<br>Tool & Data"]
    F --> G["Layer 1<br>Infrastructure"]
```

Core layers:
- Application
- Agent Framework
- Persona / Identity
- Execution Integrity
- Governance / Verification
- Tool & Data
- Infrastructure

Key distinction:
- Governance decides what should be allowed.
- Execution integrity proves what actually happened.
