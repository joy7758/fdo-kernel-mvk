<!-- language-switch:start -->
<p>
  <a href="./README.md">
    <img src="https://img.shields.io/badge/English-Current-1f883d?style=for-the-badge" alt="English">
  </a>
  <a href="./README.zh-CN.md">
    <img src="https://img.shields.io/badge/Chinese-Switch-0f172a?style=for-the-badge" alt="Chinese">
  </a>
</p>
<!-- language-switch:end -->

# fdo-kernel-mvk

Execution Integrity Layer for deterministic, replay-verifiable autonomous object runs.

## Role

`fdo-kernel-mvk` is the execution-integrity layer in the Digital Biosphere Architecture. It focuses on execution truth, deterministic replay, tamper detection, and fail-closed conformance for bounded autonomous object runs.

## Not this repo

- not the governance layer
- not the audit control plane
- not the architecture hub
- not a full agent framework

## Start here

- [docs/boundary.md](docs/boundary.md)
- [docs/replay-model.md](docs/replay-model.md)
- [examples/demo.md](examples/demo.md)
- [examples/fixtures/](examples/fixtures/)

## Depends on

- [digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture)
- [token-governor](https://github.com/joy7758/token-governor)
- [aro-audit](https://github.com/joy7758/aro-audit)

## Run / Replay / Tamper

```bash
make run
make replay
make tamper
```

Expected outputs:

- `make run` -> `EXECUTION_OK`
- `make replay` -> `REPLAY_PASS`
- `make tamper` -> `CONFORMANCE_FAIL`

Canonical stack order:

Persona -> Interaction -> Governance -> Execution Integrity -> Audit

Key distinction:

- Governance decides what should be allowed.
- MVK proves what actually happened.

## Status

- active execution-integrity prototype
- boundary cleanup in progress
