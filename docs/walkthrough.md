# Reproducible Walkthrough

This walkthrough demonstrates deterministic execution,
conformance enforcement, rollback, and independent replay verification.

## 1. Run Demo

```bash
python3 demo.py
```

Expected result:

- 5 accepted transitions
- 1 drift event triggering rollback
- audit_bundle.json generated

## 2. Replay Verification

```bash
python3 kernel/verify.py
```

Expected output:

```text
VERIFIED: Causally Closed Object
```

## 3. Tamper Detection

Modify audit_bundle.json and rerun verification.

Expected output:

```text
TAMPER DETECTED
```
