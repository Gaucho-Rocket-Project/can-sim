#!/usr/bin/env python3

import argparse
import multiprocessing
import time

from utils import *
from mcu import mcu
from etc import etc
from epr import epr


def start_all(fault_after: float | None) -> None:
    processes = [
        multiprocessing.Process(target=epr, args=(fault_after,), name="EPR Module"),
        multiprocessing.Process(target=etc, name="ETC Module"),
        multiprocessing.Process(target=mcu, name="MCU Module"),
    ]
    started = []
    try:
        for process in processes:
            process.start()
            started.append(process)
        shutdown_deadline = None
        while True:
            for process in processes:
                process.join(timeout=0.1)
                if process.exitcode is not None:
                    if process.exitcode != 0:
                        raise RuntimeError(f"{process.name} exited with {process.exitcode}")
                    if shutdown_deadline is None:
                        shutdown_deadline = time.monotonic() + 5.0
            if all(process.exitcode == 0 for process in processes):
                return
            if shutdown_deadline is not None and time.monotonic() >= shutdown_deadline:
                raise RuntimeError("Timed out waiting for simulator tasks to shut down")
    finally:
        for process in started:
            if process.is_alive():
                process.terminate()
        for process in started:
            process.join(timeout=1.0)
            if process.is_alive():
                process.kill()
                process.join()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("role", choices=["mcu", "epr", "etc", "all"])
    parser.add_argument("--fault-after", type=float, default=None,
                        help="Seconds until pressurizer reports a synthetic fault")
    args = parser.parse_args()
    if args.role == "mcu":
        mcu()
    elif args.role == "epr":
        epr(args.fault_after)
    elif args.role == "etc":
        etc()
    else:
        start_all(args.fault_after)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
