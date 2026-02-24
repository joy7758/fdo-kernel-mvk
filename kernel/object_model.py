import hashlib
import json
from dataclasses import dataclass
from typing import Dict

State = Dict[str, int]


@dataclass(frozen=True)
class MEDO:
    metadata: Dict[str, str]
    initial_state: State
    threshold: int


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_serialize(obj: object) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def compute_object_id(metadata: Dict[str, str], threshold: int, initial_state: State) -> str:
    return sha256_bytes(
        stable_serialize(metadata)
        + stable_serialize({"threshold": threshold})
        + stable_serialize(initial_state)
    )


def transition(state: State) -> State:
    return {"x": state["x"] + 1, "y": state["y"] + 1}
