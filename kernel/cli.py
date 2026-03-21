from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import string
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE_DIR = REPO_ROOT / "examples" / "fixtures"
DEFAULT_RUNTIME_DIR = REPO_ROOT / "examples" / "runtime"
GENESIS_HASH = "GENESIS"
CHECKSUM_FIELD = "checksum"
LEGACY_CHECKSUM_FIELD = "signature"
TRACE_CHECKSUM_FIELD = "object_checksum"
LEGACY_TRACE_CHECKSUM_FIELD = "object_signature"


class RuntimeFailure(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(data: object) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_checksum(obj: dict[str, object]) -> str:
    canonical_obj = dict(obj)
    canonical_obj.pop(CHECKSUM_FIELD, None)
    canonical_obj.pop(LEGACY_CHECKSUM_FIELD, None)
    return sha256_text(canonical_json(canonical_obj))


def normalize_object_fields(obj: dict[str, object]) -> None:
    if LEGACY_CHECKSUM_FIELD in obj and CHECKSUM_FIELD not in obj:
        obj[CHECKSUM_FIELD] = obj.pop(LEGACY_CHECKSUM_FIELD)
    else:
        obj.pop(LEGACY_CHECKSUM_FIELD, None)


def trace_checksum(trace: dict[str, object]) -> object:
    return trace.get(TRACE_CHECKSUM_FIELD) or trace.get(LEGACY_TRACE_CHECKSUM_FIELD)


def is_sha256_hex(value: object) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(char in string.hexdigits for char in value)


def load_json(path: Path, fail_message: str) -> dict[str, object]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeFailure(fail_message) from exc


def save_json(path: Path, data: dict[str, object], fail_message: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, sort_keys=True)
            handle.write("\n")
    except Exception as exc:  # noqa: BLE001
        raise RuntimeFailure(fail_message) from exc


def ensure_id_and_checksum(obj: dict[str, object]) -> str:
    normalize_object_fields(obj)
    current_hash = sha256_text(str(obj.get("input", "")))

    if not obj.get("id"):
        obj["id"] = current_hash

    if not obj.get(CHECKSUM_FIELD):
        obj[CHECKSUM_FIELD] = compute_checksum(obj)

    return current_hash


def load_previous_hash(trace_path: Path) -> str:
    try:
        with open(trace_path, "r", encoding="utf-8") as handle:
            trace = json.load(handle)
            value = trace.get("current_hash")
            return value if value else GENESIS_HASH
    except Exception:  # noqa: BLE001
        return GENESIS_HASH


def runtime_paths(runtime_dir: Path) -> tuple[Path, Path]:
    return runtime_dir / "object.json", runtime_dir / "trace.json"


def reset_runtime(fixture_dir: Path = DEFAULT_FIXTURE_DIR, runtime_dir: Path = DEFAULT_RUNTIME_DIR) -> None:
    runtime_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(fixture_dir / "object.json", runtime_dir / "object.json")
    shutil.copyfile(fixture_dir / "trace.json", runtime_dir / "trace.json")


def run_execution(runtime_dir: Path = DEFAULT_RUNTIME_DIR, *, reset: bool = True) -> str:
    object_path, trace_path = runtime_paths(runtime_dir)
    if reset:
        reset_runtime(DEFAULT_FIXTURE_DIR, runtime_dir)

    obj = load_json(object_path, "CONFORMANCE_FAIL")
    normalize_object_fields(obj)

    if obj.get("payload") != "sha256" or obj.get("constraint") != "hash-match":
        raise RuntimeFailure("CONFORMANCE_FAIL")

    current_hash = ensure_id_and_checksum(obj)

    if obj.get("id") != current_hash:
        raise RuntimeFailure("CONFORMANCE_FAIL")
    if obj.get(CHECKSUM_FIELD) != compute_checksum(obj):
        raise RuntimeFailure("CONFORMANCE_FAIL")

    previous_hash = load_previous_hash(trace_path)
    if previous_hash != GENESIS_HASH and not is_sha256_hex(previous_hash):
        raise RuntimeFailure("CONFORMANCE_FAIL")

    obj["state"] = "executed"
    obj[CHECKSUM_FIELD] = compute_checksum(obj)
    trace = {
        "current_hash": current_hash,
        TRACE_CHECKSUM_FIELD: obj[CHECKSUM_FIELD],
        "previous_hash": previous_hash,
        "status": "EXECUTION_OK",
    }

    save_json(object_path, obj, "CONFORMANCE_FAIL")
    save_json(trace_path, trace, "CONFORMANCE_FAIL")
    return "EXECUTION_OK"


def replay_execution(runtime_dir: Path = DEFAULT_RUNTIME_DIR) -> str:
    object_path, trace_path = runtime_paths(runtime_dir)
    obj = load_json(object_path, "REPLAY_FAIL")
    trace = load_json(trace_path, "REPLAY_FAIL")
    normalize_object_fields(obj)

    if trace.get("status") != "EXECUTION_OK":
        raise RuntimeFailure("REPLAY_FAIL")

    recomputed_hash = sha256_text(str(obj.get("input", "")))

    if obj.get("id") != recomputed_hash:
        raise RuntimeFailure("REPLAY_FAIL")
    if obj.get(CHECKSUM_FIELD) != compute_checksum(obj):
        raise RuntimeFailure("REPLAY_FAIL")

    if trace.get("current_hash") != recomputed_hash:
        raise RuntimeFailure("REPLAY_FAIL")
    if trace_checksum(trace) != obj.get(CHECKSUM_FIELD):
        raise RuntimeFailure("REPLAY_FAIL")

    previous_hash = trace.get("previous_hash")
    if previous_hash != GENESIS_HASH and not is_sha256_hex(previous_hash):
        raise RuntimeFailure("REPLAY_FAIL")

    return "REPLAY_PASS"


def tamper_execution(runtime_dir: Path = DEFAULT_RUNTIME_DIR) -> str:
    object_path, trace_path = runtime_paths(runtime_dir)
    if not object_path.exists() or not trace_path.exists():
        run_execution(runtime_dir, reset=True)

    obj = load_json(object_path, "CONFORMANCE_FAIL")
    normalize_object_fields(obj)
    if not obj.get("id") or not obj.get(CHECKSUM_FIELD):
        raise RuntimeFailure("CONFORMANCE_FAIL")

    obj["input"] = f"{obj.get('input', '')}-tampered"
    save_json(object_path, obj, "CONFORMANCE_FAIL")
    return run_execution(runtime_dir, reset=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fdo-kernel-mvk",
        description="Execution integrity kernel for deterministic run, replay, and tamper checks.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("run", "replay", "tamper"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument(
            "--runtime-dir",
            default=str(DEFAULT_RUNTIME_DIR),
            help="Directory containing runtime object and trace files.",
        )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    runtime_dir = Path(args.runtime_dir)

    try:
        if args.command == "run":
            print(run_execution(runtime_dir))
            return 0
        if args.command == "replay":
            print(replay_execution(runtime_dir))
            return 0
        if args.command == "tamper":
            print(tamper_execution(runtime_dir))
            return 0
    except RuntimeFailure as exc:
        print(exc.message)
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
