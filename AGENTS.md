# AGENTS.md

## Repository role

This repository is the execution-integrity kernel for the Execution Evidence Bridge.

It proves runtime execution integrity through deterministic execution, replay validation, checksum/checkpoint verification, and tamper detection.

## Agent instructions

- Treat this repository as the execution-integrity layer, not the evidence packaging layer.
- Use `make demo`, `make verify-demo`, `make export-aep`, and `make verify-aep` for the local bridge path.
- Use `agent-evidence` for offline bundle verification, signed exports, receipts, and review packs.
- Use `digital-biosphere-architecture` as the canonical architecture and AI discovery hub.
- Do not claim legal non-repudiation, compliance certification, AI Act approval, official FDO standard adoption, or production forensic timestamping.

## Useful checks

```bash
python3 -m py_compile examples/export_mvk_aep_bundle.py
bash tests.sh
grep -R "Execution Evidence Bridge" README.md README.zh-CN.md docs llms.txt AGENTS.md
grep -R "not legal non-repudiation" llms.txt AGENTS.md docs
```
