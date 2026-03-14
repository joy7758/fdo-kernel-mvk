#!/usr/bin/env python3
import hashlib
import json
import string
import sys

OBJECT_PATH = "object.json"
TRACE_PATH = "trace.json"
GENESIS_HASH = "GENESIS"
CHECKSUM_FIELD = "checksum"
LEGACY_CHECKSUM_FIELD = "signature"
TRACE_CHECKSUM_FIELD = "object_checksum"
LEGACY_TRACE_CHECKSUM_FIELD = "object_signature"


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_checksum(obj):
    canonical_obj = dict(obj)
    canonical_obj.pop(CHECKSUM_FIELD, None)
    canonical_obj.pop(LEGACY_CHECKSUM_FIELD, None)
    return sha256_text(canonical_json(canonical_obj))


def normalize_object_fields(obj):
    if LEGACY_CHECKSUM_FIELD in obj and CHECKSUM_FIELD not in obj:
        obj[CHECKSUM_FIELD] = obj.pop(LEGACY_CHECKSUM_FIELD)
    else:
        obj.pop(LEGACY_CHECKSUM_FIELD, None)


def trace_checksum(trace):
    return trace.get(TRACE_CHECKSUM_FIELD) or trace.get(LEGACY_TRACE_CHECKSUM_FIELD)


def is_sha256_hex(value):
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(char in string.hexdigits for char in value)


def load_json(path, fail_message):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print(fail_message)
        sys.exit(1)


def save_json(path, data, fail_message):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.write("\n")
    except Exception:
        print(fail_message)
        sys.exit(1)


def ensure_id_and_checksum(obj):
    normalize_object_fields(obj)
    current_hash = sha256_text(obj.get("input", ""))

    if not obj.get("id"):
        obj["id"] = current_hash

    if not obj.get(CHECKSUM_FIELD):
        obj[CHECKSUM_FIELD] = compute_checksum(obj)

    return current_hash


def load_previous_hash():
    try:
        with open(TRACE_PATH, "r", encoding="utf-8") as f:
            trace = json.load(f)
            value = trace.get("current_hash")
            return value if value else GENESIS_HASH
    except Exception:
        return GENESIS_HASH


def fail_conformance():
    print("CONFORMANCE_FAIL")
    sys.exit(1)


def fail_replay():
    print("REPLAY_FAIL")
    sys.exit(1)


def run():
    obj = load_json(OBJECT_PATH, "CONFORMANCE_FAIL")
    normalize_object_fields(obj)

    if obj.get("payload") != "sha256" or obj.get("constraint") != "hash-match":
        fail_conformance()

    current_hash = ensure_id_and_checksum(obj)

    if obj.get("id") != current_hash:
        fail_conformance()
    if obj.get(CHECKSUM_FIELD) != compute_checksum(obj):
        fail_conformance()

    previous_hash = load_previous_hash()
    if previous_hash != GENESIS_HASH and not is_sha256_hex(previous_hash):
        fail_conformance()

    obj["state"] = "executed"
    obj[CHECKSUM_FIELD] = compute_checksum(obj)
    trace = {
        "current_hash": current_hash,
        TRACE_CHECKSUM_FIELD: obj[CHECKSUM_FIELD],
        "previous_hash": previous_hash,
        "status": "EXECUTION_OK",
    }

    save_json(OBJECT_PATH, obj, "CONFORMANCE_FAIL")
    save_json(TRACE_PATH, trace, "CONFORMANCE_FAIL")

    print("EXECUTION_OK")


def tamper():
    obj = load_json(OBJECT_PATH, "CONFORMANCE_FAIL")
    normalize_object_fields(obj)
    if not obj.get("id") or not obj.get(CHECKSUM_FIELD):
        fail_conformance()

    obj["input"] = f"{obj.get('input', '')}-tampered"
    save_json(OBJECT_PATH, obj, "CONFORMANCE_FAIL")

    run()


def replay():
    obj = load_json(OBJECT_PATH, "REPLAY_FAIL")
    trace = load_json(TRACE_PATH, "REPLAY_FAIL")
    normalize_object_fields(obj)

    if trace.get("status") != "EXECUTION_OK":
        fail_replay()

    recomputed_hash = sha256_text(obj.get("input", ""))

    if obj.get("id") != recomputed_hash:
        fail_replay()
    if obj.get(CHECKSUM_FIELD) != compute_checksum(obj):
        fail_replay()

    if trace.get("current_hash") != recomputed_hash:
        fail_replay()
    if trace_checksum(trace) != obj.get(CHECKSUM_FIELD):
        fail_replay()

    previous_hash = trace.get("previous_hash")
    if previous_hash != GENESIS_HASH and not is_sha256_hex(previous_hash):
        fail_replay()

    print("REPLAY_PASS")


def main():
    if len(sys.argv) != 2:
        print("CONFORMANCE_FAIL")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "--run":
        run()
        return

    if cmd == "--tamper":
        tamper()
        return

    if cmd == "--replay":
        replay()
        return

    print("CONFORMANCE_FAIL")
    sys.exit(1)


if __name__ == "__main__":
    main()
