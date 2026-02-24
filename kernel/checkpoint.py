import hashlib
import json
from typing import Dict, List

State = Dict[str, int]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def state_hash(state: State) -> str:
    encoded = json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(encoded)


def next_checkpoint(previous: str, state: State) -> str:
    return sha256_bytes(bytes.fromhex(previous) + bytes.fromhex(state_hash(state)))


def checkpoint_chain(object_id: str, states: List[State]) -> List[str]:
    if not states:
        return []
    chain: List[str] = []
    current = sha256_bytes(bytes.fromhex(object_id) + bytes.fromhex(state_hash(states[0])))
    chain.append(current)
    for state in states[1:]:
        current = next_checkpoint(current, state)
        chain.append(current)
    return chain
