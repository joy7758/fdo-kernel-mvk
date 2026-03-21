# MVK Root Inventory

Pre-refactor root inventory snapshot for `fdo-kernel-mvk`:

- `docs/`
- `examples/`
- `kernel/`
- `tests/`
- legacy root demo script
- legacy root CLI shim
- legacy root object fixture
- legacy root trace fixture
- legacy root test script
- root position paper
- root audit bundle

Primary boundary issues:

- execution-integrity package code and prototype entrypoints were mixed together at the repo root
- replay fixtures and generated output lived beside the canonical package surface
- root-level research material competed with package documentation
- stack diagrams still placed execution integrity ahead of governance
