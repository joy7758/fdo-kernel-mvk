import hashlib
import json
from typing import Dict, List

State = Dict[str, int]
GENESIS = hashlib.sha256(b"GENESIS").hexdigest()


def state_hash(state: State) -> str:
    encoded = json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def next_checkpoint(previous: str, state: State) -> str:
    return hashlib.sha256((previous + state_hash(state)).encode()).hexdigest()


def checkpoint_chain(states: List[State]) -> List[str]:
    chain: List[str] = []
    current = GENESIS
    for state in states:
        current = next_checkpoint(current, state)
        chain.append(current)
    return chain
