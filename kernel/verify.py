import json
from pathlib import Path
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
DEFAULT_BUNDLE = Path(__file__).resolve().parents[1] / "audit_bundle.json"


def _load_bundle(path: Path) -> Dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def verify_bundle(path: str = str(DEFAULT_BUNDLE)) -> bool:
    try:
        bundle = _load_bundle(Path(path))
        states: List[State] = bundle["accepted_states"]
        transition_count: int = bundle["transition_count"]
        threshold: int = bundle["threshold"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        print("TAMPER DETECTED")
        return False
    if not states or transition_count != len(states) - 1:
        print("TAMPER DETECTED")
        return False

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
    if len(replayed_drifts) != transition_count:
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

    try:
        event = bundle["drift_event"]
        event_drift = l1_distance(states[-1], event["attempted_state"])
        event_value = event["drift"]
        rollback_state = event["rollback_state"]
    except (KeyError, TypeError):
        print("TAMPER DETECTED")
        return False
    if event_drift != event_value or event_drift <= threshold:
        print("TAMPER DETECTED")
        return False
    if rollback_state != states[-1]:
        print("TAMPER DETECTED")
        return False

    print("VERIFIED: Causally Closed Object")
    return True


if __name__ == "__main__":
    verify_bundle()
