import json
from typing import Dict, List

try:
    from .checkpoint import checkpoint_chain
    from .drift import l1_distance
    from .object_model import transition
except ImportError:
    from checkpoint import checkpoint_chain
    from drift import l1_distance
    from object_model import transition

State = Dict[str, int]


def _load_bundle(path: str) -> Dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def verify_bundle(path: str = "audit_bundle.json") -> bool:
    bundle = _load_bundle(path)
    states: List[State] = bundle["accepted_states"]
    transition_count: int = bundle["transition_count"]
    threshold: int = bundle["threshold"]

    replayed_states: List[State] = [states[0]]
    for _ in range(transition_count):
        replayed_states.append(transition(replayed_states[-1]))
    if replayed_states != states:
        print("TAMPER DETECTED")
        return False

    replayed_drifts = [l1_distance(states[i], states[i + 1]) for i in range(len(states) - 1)]
    if replayed_drifts != bundle["drifts"]:
        print("TAMPER DETECTED")
        return False
    if any(drift > threshold for drift in replayed_drifts):
        print("TAMPER DETECTED")
        return False

    replayed_checkpoints = checkpoint_chain(states)
    if replayed_checkpoints != bundle["checkpoints"]:
        print("TAMPER DETECTED")
        return False
    if replayed_checkpoints[-1] != bundle["final_checkpoint"]:
        print("TAMPER DETECTED")
        return False

    event = bundle["drift_event"]
    event_drift = l1_distance(states[-1], event["attempted_state"])
    if event_drift != event["drift"] or event_drift <= threshold:
        print("TAMPER DETECTED")
        return False
    if event["rollback_state"] != states[-1]:
        print("TAMPER DETECTED")
        return False

    print("VERIFIED: Causally Closed Object")
    return True


if __name__ == "__main__":
    verify_bundle()
