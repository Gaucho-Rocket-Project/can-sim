import csv
from bisect import bisect_right

def load_thrust_profile(filename: str) -> tuple[list[float], list[float]]:
    """Load CSV time/value pairs and validate the profile."""
    times: list[float] = []
    values: list[float] = []
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not {"time", "value"}.issubset(reader.fieldnames):
            raise ValueError("CSV must contain 'time' and 'value' columns")
        for row in reader:
            t = float(row["time"])
            value = float(row["value"])
            if not (0 <= value <= 100):
                raise ValueError("Thrust values must be between 0 and 100")
            if t < 0 or (times and t <= times[-1]):
                raise ValueError("Times must be nonnegative and strictly increasing")
            times.append(t)
            values.append(value)
    if not times or times[0] != 0:
        raise ValueError("Profile must begin at time 0")
    return times, values

def get_thrust(elapsed: float, times: list[float], values: list[float]) -> int:
    """Linearly interpolate requested thrust at elapsed time."""
    if elapsed <= times[0]:
        return round(values[0])
    if elapsed >= times[-1]:
        return round(values[-1])
    i = bisect_right(times, elapsed)
    t0, t1 = times[i - 1], times[i]
    v0, v1 = values[i - 1], values[i]
    alpha = (elapsed - t0) / (t1 - t0)
    return round(v0 + alpha * (v1 - v0))

def log(node: str, message: str) -> None:
    '''
    prints debugging information.

    `node`: identifies which virtual device generated the message

    `message`: contains the actual information.
    '''
    print(f"[{node:8s}] {message}", flush=True)