# Demo Walkthrough

The minimal demo surface shows deterministic execution, replay verification, and tamper detection without turning this repository into a full-stack framework.

## Run

```bash
python3 -m examples.demo
python3 -m kernel.verify examples/output/audit_bundle.json
```

Expected result:

- `examples/output/audit_bundle.json` generated
- `VERIFIED: Causally Closed Object`

## Minimal kernel path

```bash
make run
make replay
make tamper
```

These targets exercise the execution-integrity kernel directly against `examples/runtime/`.
