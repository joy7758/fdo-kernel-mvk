#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 demo.py
python3 - <<'PY'
import json; p='audit_bundle.json'; b=json.load(open(p)); b['accepted_states'][1]['x'] += 1; json.dump(b, open(p,'w'), indent=2, sort_keys=True)
PY
python3 kernel/verify.py
