class ConformanceFailure(Exception):
    pass


def enforce_drift_bound(drift: int, threshold: int) -> None:
    if drift > threshold:
        raise ConformanceFailure(f"drift {drift} exceeds threshold {threshold}")
