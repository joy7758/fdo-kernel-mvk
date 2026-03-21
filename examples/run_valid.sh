#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 -m examples.demo
python3 -m kernel.verify examples/output/audit_bundle.json
