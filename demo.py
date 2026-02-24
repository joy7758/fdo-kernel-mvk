import json
from pathlib import Path

from kernel.checkpoint import checkpoint_chain
from kernel.drift import l1_distance
from kernel.gate import ConformanceFailure, enforce_drift_bound
from kernel.object_model import MEDO, transition


def main() -> None:
    root_dir = Path(__file__).resolve().parent
    medo = MEDO(
        metadata={"id": "medo-001", "name": "fdo-kernel-mvk"},
        initial_state={"x": 0, "y": 0},
        threshold=3,
    )

    states = [dict(medo.initial_state)]
    drifts = []

    for _ in range(5):
        next_state = transition(states[-1])
        drift = l1_distance(states[-1], next_state)
        enforce_drift_bound(drift, medo.threshold)
        states.append(next_state)
        drifts.append(drift)

    attempted_state = {"x": states[-1]["x"] + 5, "y": states[-1]["y"]}
    attempted_drift = l1_distance(states[-1], attempted_state)
    rollback_state = dict(states[-1])
    try:
        enforce_drift_bound(attempted_drift, medo.threshold)
    except ConformanceFailure:
        pass

    checkpoints = checkpoint_chain(states)
    bundle = {
        "metadata": medo.metadata,
        "threshold": medo.threshold,
        "transition_count": 5,
        "accepted_states": states,
        "drifts": drifts,
        "checkpoints": checkpoints,
        "final_checkpoint": checkpoints[-1],
        "drift_event": {
            "attempted_state": attempted_state,
            "drift": attempted_drift,
            "rollback_state": rollback_state,
        },
    }

    with open(root_dir / "audit_bundle.json", "w", encoding="utf-8") as handle:
        json.dump(bundle, handle, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
