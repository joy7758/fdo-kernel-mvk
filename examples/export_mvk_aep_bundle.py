#!/usr/bin/env python3
"""Export an MVK audit bundle as a local AEP-compatible evidence bundle."""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

SCHEMA_VERSION = "0.1.0"
PROFILE = "agent-evidence-profile"
CAPTURE_MODE = "mvk-aep-bridge"
SOURCE_RUNTIME = "fdo-kernel-mvk"
RECEIPT_NAME = "mvk-aep-receipt.json"
EVENT_TYPES = [
    "mvk.audit_bundle.observed",
    "mvk.execution.verified",
    "mvk.rollback.verified",
]


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def sha256_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")


def write_records(path: Path, records: Sequence[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True))
            handle.write("\n")


def read_records(path: Path) -> List[Dict[str, Any]]:
    records = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            record = json.loads(stripped)
            if not isinstance(record, dict):
                raise ValueError("record line %d is not a JSON object" % line_number)
            records.append(record)
    return records


def git_output(repo_root: Path, args: Sequence[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root)] + list(args),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    value = result.stdout.strip()
    return value or None


def git_dirty(repo_root: Path) -> Optional[bool]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--porcelain"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return bool(result.stdout.strip())


def safe_count(value: Any) -> Optional[int]:
    if isinstance(value, list):
        return len(value)
    return None


def safe_max_int(value: Any) -> Optional[int]:
    if isinstance(value, list) and all(isinstance(item, int) for item in value):
        return max(value) if value else None
    return None


def digest_or_none(value: Any) -> Optional[str]:
    if value is None:
        return None
    return sha256_digest(value)


def derive_run_id(bundle: Dict[str, Any]) -> str:
    object_id = str(bundle.get("object_id", "unknown"))
    final_checkpoint = str(bundle.get("final_checkpoint", "unknown"))
    return "mvk-%s-%s" % (object_id[:12], final_checkpoint[:12])


def record_hash_input(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": record.get("schema_version"),
        "run_id": record.get("run_id"),
        "event_type": record.get("event_type"),
        "timestamp": record.get("timestamp"),
        "payload_hash": record.get("payload_hash"),
        "prev_hash": record.get("prev_hash"),
    }


def bundle_root_hash(record_hashes: Iterable[str]) -> str:
    hashes = list(record_hashes)
    if not hashes:
        return sha256_digest({"records": []})
    chain_state = None
    for record_hash in hashes:
        chain_state = sha256_digest({"prev_root": chain_state, "record_hash": record_hash})
    return str(chain_state)


def build_payloads(
    bundle: Dict[str, Any],
    artifact_ref: str,
    audit_bundle_digest: str,
) -> List[Dict[str, Any]]:
    drift_event = bundle.get("drift_event")
    if not isinstance(drift_event, dict):
        drift_event = {}

    rollback_state = drift_event.get("rollback_state")
    payload_base = {
        "object_id": bundle.get("object_id"),
        "threshold": bundle.get("threshold"),
        "transition_count": bundle.get("transition_count"),
        "accepted_state_count": safe_count(bundle.get("accepted_states")),
        "checkpoint_count": safe_count(bundle.get("checkpoints")),
        "drift_count": safe_count(bundle.get("drifts")),
        "final_checkpoint": bundle.get("final_checkpoint"),
        "audit_bundle_digest": audit_bundle_digest,
        "artifact_ref": artifact_ref,
    }

    observed_payload = dict(payload_base)
    observed_payload.update(
        {
            "drift_event_digest": digest_or_none(drift_event),
            "rollback_state_digest": digest_or_none(rollback_state),
        }
    )

    execution_payload = dict(payload_base)
    execution_payload.update(
        {
            "max_drift": safe_max_int(bundle.get("drifts")),
            "verification_scope": [
                "deterministic_transition_replay",
                "drift_threshold",
                "checkpoint_chain",
            ],
        }
    )

    rollback_payload = {
        "object_id": bundle.get("object_id"),
        "threshold": bundle.get("threshold"),
        "drift_count": safe_count(bundle.get("drifts")),
        "drift_event_digest": digest_or_none(drift_event),
        "attempted_drift": drift_event.get("drift"),
        "rollback_state_digest": digest_or_none(rollback_state),
        "final_checkpoint": bundle.get("final_checkpoint"),
        "audit_bundle_digest": audit_bundle_digest,
        "artifact_ref": artifact_ref,
    }

    return [observed_payload, execution_payload, rollback_payload]


def build_records(
    bundle: Dict[str, Any],
    run_id: str,
    artifact_ref: str,
    audit_bundle_digest: str,
    timestamp: str,
) -> Tuple[List[Dict[str, Any]], str]:
    records = []
    prev_hash = None
    payloads = build_payloads(bundle, artifact_ref, audit_bundle_digest)

    for event_type, payload in zip(EVENT_TYPES, payloads):
        payload_hash = sha256_digest(payload)
        record = {
            "schema_version": SCHEMA_VERSION,
            "run_id": run_id,
            "event_type": event_type,
            "timestamp": timestamp,
            "payload": payload,
            "payload_hash": payload_hash,
            "prev_hash": prev_hash,
        }
        record["record_hash"] = sha256_digest(record_hash_input(record))
        records.append(record)
        prev_hash = record["record_hash"]

    root_hash = bundle_root_hash(record["record_hash"] for record in records)
    for record in records:
        record["bundle_root_hash"] = root_hash

    return records, root_hash


def build_manifest(
    bundle: Dict[str, Any],
    records: Sequence[Dict[str, Any]],
    root_hash: str,
    artifact_ref: str,
    source_runtime_commit: Optional[str],
    source_runtime_dirty: Optional[bool],
) -> Dict[str, Any]:
    object_id = bundle.get("object_id")
    threshold = bundle.get("threshold")
    return {
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE,
        "run_id": records[0]["run_id"] if records else derive_run_id(bundle),
        "record_count": len(records),
        "bundle_root_hash": root_hash,
        "digest_algorithm": "sha256",
        "privacy_mode": "digest_only",
        "redaction": {
            "mode": "digest_only",
            "summary": "Record payloads keep MVK execution evidence digest-oriented.",
        },
        "records_path": "records.jsonl",
        "event_types": [record["event_type"] for record in records],
        "compatibility_targets": {
            "agent_evidence_profile": SCHEMA_VERSION,
            "bundle_layout": "manifest-records-artifacts-receipt",
        },
        "capture_mode": CAPTURE_MODE,
        "source_runtime": SOURCE_RUNTIME,
        "source_runtime_version": None,
        "source_runtime_commit": source_runtime_commit,
        "source_runtime_dirty": source_runtime_dirty,
        "source_schema_fingerprint": None,
        "identity_ref": "mvk:%s" % object_id,
        "policy_ref": "mvk:drift-threshold:%s" % threshold,
        "trace_ref": artifact_ref,
        "export_warnings": [],
        "omitted_sections": [],
    }


def export_bundle(bundle_path: Path, out_dir: Path, repo_root: Path) -> Dict[str, Any]:
    bundle = load_json(bundle_path)
    if not isinstance(bundle, dict):
        raise ValueError("MVK audit bundle must be a JSON object")

    source_runtime_commit = git_output(repo_root, ["rev-parse", "HEAD"])
    source_runtime_dirty = git_dirty(repo_root)
    audit_bundle_digest = sha256_digest(bundle)
    digest_prefix = audit_bundle_digest.split(":", 1)[1][:12]
    artifact_ref = "artifacts/audit_bundle.%s.json" % digest_prefix
    artifact_path = out_dir / artifact_ref

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    write_json(artifact_path, bundle)

    run_id = derive_run_id(bundle)
    records, root_hash = build_records(bundle, run_id, artifact_ref, audit_bundle_digest, utc_now())
    manifest = build_manifest(
        bundle,
        records,
        root_hash,
        artifact_ref,
        source_runtime_commit,
        source_runtime_dirty,
    )

    write_json(out_dir / "manifest.json", manifest)
    write_records(out_dir / "records.jsonl", records)
    return verify_aep_bundle(out_dir, write_receipt=True, emit_stdout=False)


def add_error(errors: List[str], message: str) -> None:
    errors.append(message)


def bundle_path_for_ref(bundle_dir: Path, ref: Any, errors: List[str]) -> Optional[Path]:
    if not isinstance(ref, str) or not ref:
        add_error(errors, "artifact_ref must be a non-empty string")
        return None
    ref_path = Path(ref)
    if ref_path.is_absolute() or ".." in ref_path.parts:
        add_error(errors, "artifact_ref escapes bundle directory: %s" % ref)
        return None
    return bundle_dir / ref_path


def verify_artifact_digest(
    bundle_dir: Path,
    artifact_ref: Any,
    audit_bundle_digest: Any,
    errors: List[str],
    artifact_checks: List[Dict[str, Any]],
) -> None:
    if artifact_ref is None and audit_bundle_digest is None:
        return
    if artifact_ref is None or audit_bundle_digest is None:
        add_error(errors, "artifact_ref and audit_bundle_digest must be present together")
        return

    artifact_path = bundle_path_for_ref(bundle_dir, artifact_ref, errors)
    if artifact_path is None:
        return

    check = {
        "artifact_ref": artifact_ref,
        "expected_digest": audit_bundle_digest,
        "ok": False,
    }
    try:
        artifact_value = load_json(artifact_path)
        actual_digest = sha256_digest(artifact_value)
        check["actual_digest"] = actual_digest
        check["ok"] = actual_digest == audit_bundle_digest
        if actual_digest != audit_bundle_digest:
            add_error(errors, "artifact digest mismatch for %s" % artifact_ref)
    except (OSError, json.JSONDecodeError) as exc:
        check["error"] = str(exc)
        add_error(errors, "artifact could not be read: %s" % artifact_ref)
    artifact_checks.append(check)


def verify_records(records: Sequence[Dict[str, Any]], errors: List[str]) -> Tuple[List[str], List[str]]:
    computed_record_hashes = []
    event_types = []
    prev_hash = None

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            add_error(errors, "record %d is not an object" % index)
            continue

        payload = record.get("payload")
        expected_payload_hash = sha256_digest(payload)
        if record.get("payload_hash") != expected_payload_hash:
            add_error(errors, "payload_hash mismatch for record %d" % index)

        expected_record_hash = sha256_digest(record_hash_input(record))
        if record.get("record_hash") != expected_record_hash:
            add_error(errors, "record_hash mismatch for record %d" % index)

        if record.get("prev_hash") != prev_hash:
            add_error(errors, "prev_hash mismatch for record %d" % index)

        computed_record_hashes.append(expected_record_hash)
        event_types.append(record.get("event_type"))
        prev_hash = expected_record_hash

    return computed_record_hashes, event_types


def verify_aep_bundle(
    bundle_dir: Path,
    write_receipt: bool = True,
    emit_stdout: bool = True,
) -> Dict[str, Any]:
    errors = []
    artifact_checks = []
    checked_at = utc_now()
    manifest = None
    records = []
    records_path = bundle_dir / "records.jsonl"

    try:
        manifest_value = load_json(bundle_dir / "manifest.json")
        if not isinstance(manifest_value, dict):
            add_error(errors, "manifest.json is not a JSON object")
        else:
            manifest = manifest_value
            if isinstance(manifest.get("records_path"), str):
                records_path = bundle_dir / manifest["records_path"]
    except (OSError, json.JSONDecodeError) as exc:
        add_error(errors, "manifest.json could not be read: %s" % exc)

    try:
        records = read_records(records_path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        add_error(errors, "records.jsonl could not be read: %s" % exc)

    computed_record_hashes, event_types = verify_records(records, errors)
    computed_root_hash = bundle_root_hash(computed_record_hashes)

    if manifest is not None:
        if manifest.get("record_count") != len(records):
            add_error(errors, "manifest.record_count mismatch")
        if manifest.get("event_types") != event_types:
            add_error(errors, "manifest.event_types mismatch")
        if manifest.get("bundle_root_hash") != computed_root_hash:
            add_error(errors, "manifest.bundle_root_hash mismatch")

    for index, record in enumerate(records):
        if record.get("bundle_root_hash") != computed_root_hash:
            add_error(errors, "bundle_root_hash mismatch for record %d" % index)
        payload = record.get("payload")
        if isinstance(payload, dict):
            verify_artifact_digest(
                bundle_dir,
                payload.get("artifact_ref"),
                payload.get("audit_bundle_digest"),
                errors,
                artifact_checks,
            )

    ok = not errors
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE,
        "capture_mode": CAPTURE_MODE,
        "source_runtime": SOURCE_RUNTIME,
        "checked_at": checked_at,
        "ok": ok,
        "bundle_root_hash": computed_root_hash,
        "record_count": len(records),
        "event_types": event_types,
        "manifest_path": "manifest.json",
        "records_path": path_for_receipt(records_path, bundle_dir),
        "artifact_checks": artifact_checks,
        "errors": errors,
    }

    if write_receipt and bundle_dir.exists():
        write_json(bundle_dir / RECEIPT_NAME, receipt)

    if emit_stdout:
        json.dump(receipt, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")

    return receipt


def path_for_receipt(path: Path, bundle_dir: Path) -> str:
    try:
        return str(path.relative_to(bundle_dir))
    except ValueError:
        return str(path)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export or verify an MVK AEP-compatible bundle.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--bundle", type=Path, help="Path to MVK audit_bundle.json to export.")
    mode.add_argument("--verify", type=Path, help="Path to an exported MVK AEP-compatible bundle.")
    parser.add_argument("--out", type=Path, default=Path("mvk-aep-bundle"), help="Output directory for export mode.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]

    if args.bundle is not None:
        try:
            receipt = export_bundle(args.bundle, args.out, repo_root)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print("EXPORT_FAIL: %s" % exc, file=sys.stderr)
            return 1
        print("EXPORTED: %s" % args.out)
        return 0 if receipt.get("ok") else 1

    receipt = verify_aep_bundle(args.verify, write_receipt=True, emit_stdout=True)
    return 0 if receipt.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
