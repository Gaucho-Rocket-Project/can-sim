import csv
import sys
from pathlib import Path
import matplotlib.pyplot as plt


def load_thrust_profile(filename: str) -> tuple[list[float], list[float]]:
    """Load time/value columns from a thrust profile CSV."""
    times: list[float] = []
    values: list[float] = []

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames or not {"time", "value"}.issubset(reader.fieldnames):
            raise ValueError("CSV must contain 'time' and 'value' columns")

        for row in reader:
            t = float(row["time"])
            value = float(row["value"])

            if t < 0:
                raise ValueError("Time values must be nonnegative")
            if not (0 <= value <= 100):
                raise ValueError("Thrust values must be between 0 and 100")
            if times and t <= times[-1]:
                raise ValueError("Time values must be strictly increasing")

            times.append(t)
            values.append(value)

    if not times:
        raise ValueError("CSV is empty")
    if times[0] != 0:
        raise ValueError("Profile must begin at time 0")

    return times, values


def main() -> None:
    filename = sys.argv[1] if len(sys.argv) > 1 else "thrust_profile.csv"

    if not Path(filename).exists():
        raise FileNotFoundError(f"Could not find file: {filename}")

    times, values = load_thrust_profile(filename)

    plt.figure(figsize=(8, 4.5))
    plt.plot(times, values, marker="o")
    plt.xlabel("Time (s)")
    plt.ylabel("Requested Thrust (%)")
    plt.title("Thrust Profile")
    plt.ylim(0, 100)
    plt.xlim(left=0)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()