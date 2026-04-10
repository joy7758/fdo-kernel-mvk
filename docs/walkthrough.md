# Reproducible Walkthrough

This walkthrough demonstrates deterministic execution,
conformance enforcement, rollback, and independent replay verification.

It documents the execution-integrity layer only. For system context, start with
[digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture);
for governance, use
[token-governor](https://github.com/joy7758/token-governor); for concrete
evidence packaging, use
[agent-evidence](https://github.com/joy7758/agent-evidence); for
post-execution review, use [aro-audit](https://github.com/joy7758/aro-audit).

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

## 3. State Tamper Detection

Modify any accepted state in audit_bundle.json and rerun verification.

Expected output:

```text
TAMPER DETECTED
```

## 4. Threshold Tamper Detection

Modify `threshold` in `audit_bundle.json` and rerun verification.

Expected output:

```text
TAMPER DETECTED
```

## 5. Metadata Tamper Detection

Modify `metadata` in `audit_bundle.json` and rerun verification.

Expected output:

```text
TAMPER DETECTED
```
