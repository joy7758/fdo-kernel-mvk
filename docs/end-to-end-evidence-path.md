# End-to-End Evidence Path

This walkthrough shows the local bridge from MVK execution proof to an Agent
Evidence Profile-compatible evidence handoff:

```text
MVK execution -> audit_bundle.json -> AEP-compatible bundle -> offline verification -> reviewer handoff
```

## Commands

```bash
make demo
make verify-demo
make export-aep
make verify-aep
```

`make demo` runs the MVK demo and writes `audit_bundle.json`. `make
verify-demo` replays and verifies that bundle as a causally closed object.

`make export-aep` converts the MVK audit bundle into a local AEP-compatible
directory. Expected outputs:

- `audit_bundle.json`
- `mvk-aep-bundle/manifest.json`
- `mvk-aep-bundle/records.jsonl`
- `mvk-aep-bundle/artifacts/audit_bundle.<12-char-sha256-prefix>.json`
- `mvk-aep-bundle/mvk-aep-receipt.json`

`make verify-aep` verifies the local bundle by recomputing payload hashes,
record hashes, the previous-record chain, the bundle root hash, manifest counts,
manifest event types, and the referenced audit-bundle artifact digest. It writes
or updates `mvk-aep-bundle/mvk-aep-receipt.json` and prints the receipt JSON.

## Layer Boundary

This bridge is intentionally minimal, unsigned, and local. It keeps
`fdo-kernel-mvk` focused on execution integrity: deterministic execution, replay
verification, checksum/checkpoint integrity, rollback evidence, and tamper
detection.

Signed export, signed manifests, portable receipts, offline verification
tooling, and reviewer handoff packs remain the responsibility of
[agent-evidence](https://github.com/joy7758/agent-evidence).
