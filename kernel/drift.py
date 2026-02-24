from typing import Dict

State = Dict[str, int]


def l1_distance(left: State, right: State) -> int:
    keys = sorted(set(left) | set(right))
    return sum(abs(right.get(key, 0) - left.get(key, 0)) for key in keys)
