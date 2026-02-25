import json
import subprocess
from pathlib import Path

from kernel.verify import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "audit_bundle.json"

subprocess.run(["python3", str(ROOT / "demo.py")], check=True)
bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))

assert "object_id" in bundle and isinstance(bundle["object_id"], str) and bundle["object_id"]
assert len(bundle["drifts"]) == 5

tampered = dict(bundle)
tampered["threshold"] = bundle["threshold"] + 1
tampered_path = ROOT / "audit_bundle_tampered.json"
tampered_path.write_text(json.dumps(tampered, indent=2, sort_keys=True), encoding="utf-8")

assert verify_bundle(str(tampered_path)) is False
print("reproducibility checks passed")
