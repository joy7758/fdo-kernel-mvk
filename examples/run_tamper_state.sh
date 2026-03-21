#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 -m examples.demo
python3 - <<'PY'
import json
from pathlib import Path

p = Path("examples/output/audit_bundle.json")
b = json.loads(p.read_text(encoding="utf-8"))
b["accepted_states"][1]["x"] += 1
p.write_text(json.dumps(b, indent=2, sort_keys=True), encoding="utf-8")
PY
python3 -m kernel.verify examples/output/audit_bundle.json
