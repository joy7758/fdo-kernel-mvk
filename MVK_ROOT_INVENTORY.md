# MVK Root Inventory

Pre-refactor root inventory snapshot for `fdo-kernel-mvk`:

- `docs/`
- `examples/`
- `kernel/`
- `tests/`
- `demo.py`
- `mvk.py`
- `object.json`
- `trace.json`
- `tests.sh`
- `POSITION_PAPER.md`
- `audit_bundle.json`

Primary boundary issues:

- execution-integrity package code and prototype entrypoints were mixed together at the repo root
- replay fixtures and generated output lived beside the canonical package surface
- root-level research material competed with package documentation
- stack diagrams still placed execution integrity ahead of governance
