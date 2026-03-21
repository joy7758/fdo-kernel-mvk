# Reproducible Walkthrough

This walkthrough demonstrates deterministic execution,
conformance enforcement, rollback, and independent replay verification.

## 1. Run Demo

```bash
python3 -m examples.demo
```

Expected result:

- 5 accepted transitions
- 1 drift event triggering rollback
- `examples/output/audit_bundle.json` generated

## 2. Replay Verification

```bash
python3 -m kernel.verify examples/output/audit_bundle.json
```

Expected output:

```text
VERIFIED: Causally Closed Object
```

## 3. State Tamper Detection

Modify any accepted state in `examples/output/audit_bundle.json` and rerun verification.

Expected output:

```text
TAMPER DETECTED
```

## 4. Threshold Tamper Detection

Modify `threshold` in `examples/output/audit_bundle.json` and rerun verification.

Expected output:

```text
TAMPER DETECTED
```

## 5. Metadata Tamper Detection

Modify `metadata` in `examples/output/audit_bundle.json` and rerun verification.

Expected output:

```text
TAMPER DETECTED
```
