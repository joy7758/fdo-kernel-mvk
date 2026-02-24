from dataclasses import dataclass
from typing import Dict

State = Dict[str, int]


@dataclass(frozen=True)
class MEDO:
    metadata: Dict[str, str]
    initial_state: State
    threshold: int


def transition(state: State) -> State:
    return {"x": state["x"] + 1, "y": state["y"] + 1}
