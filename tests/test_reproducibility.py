import json
import subprocess
import unittest
from pathlib import Path

from kernel.verify import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "examples" / "output" / "audit_bundle.json"


class ReproducibilityTests(unittest.TestCase):
    def test_demo_bundle_is_replay_verifiable_and_tamper_detecting(self) -> None:
        subprocess.run(["python3", "-m", "examples.demo"], cwd=ROOT, check=True)
        bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))

        self.assertIn("object_id", bundle)
        self.assertTrue(isinstance(bundle["object_id"], str) and bundle["object_id"])
        self.assertEqual(len(bundle["drifts"]), 5)
        self.assertTrue(verify_bundle(str(BUNDLE)))

        tampered = dict(bundle)
        tampered["threshold"] = bundle["threshold"] + 1
        tampered_path = ROOT / "examples" / "output" / "audit_bundle_tampered.json"
        tampered_path.write_text(json.dumps(tampered, indent=2, sort_keys=True), encoding="utf-8")

        self.assertFalse(verify_bundle(str(tampered_path)))


if __name__ == "__main__":
    unittest.main()
