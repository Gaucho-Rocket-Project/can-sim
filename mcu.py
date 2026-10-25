from can_interface import *
from utils import *

import time

def mcu(profile_path: str = "thrust_profile.csv") -> None:
    """TVC MCU emulator using a CSV thrust profile."""
    times, values = load_thrust_profile(profile_path)
    with can.Bus(channel="vcan0", interface="socketcan") as bus:
        t0 = time.monotonic()
        next_send = t0
        heartbeat = 0
        requested = 0
        last_epr_status = None
        last_etc_status = None
        last_log_slot = -1

        log("MCU", f"Loaded thrust profile: {profile_path}")
        
        while True:
            msg = bus.recv(timeout=0.05)
            t = time.monotonic()

            if msg and not msg.is_extended_id:
                if msg.arbitration_id == EPR_STATUS and len(msg.data) == 3:
                    last_epr_status = (t, msg.data[0], msg.data[1], msg.data[2])
                elif msg.arbitration_id == ETC_STATUS and len(msg.data) == 4:
                    last_etc_status = (t, msg.data[0], msg.data[1])

            if t >= next_send:
                elapsed = t - t0
                requested = get_thrust(elapsed, times, values)

                send(bus, THRUST_REQUEST, requested)
                send(bus, MCU_HEARTBEAT, heartbeat)

                heartbeat = (heartbeat + 1) % 256
                next_send = t + PERIOD

            slot = int(t - t0)

            if slot != last_log_slot:
                press = (
                    "READY"
                    if last_epr_status
                    and fresh(last_epr_status[0], t)
                    and last_epr_status[1] == EPR_READY
                    else "NOT READY"
                )

                actuator = (
                    f"{last_etc_status[2]}%"
                    if last_etc_status
                    and fresh(last_etc_status[0], t)
                    else "NO FEEDBACK"
                )

                log(
                    "MCU",
                    f"request={requested:3d}% | "
                    f"press={press} | "
                    f"virtual actuator={actuator}"
                )

                last_log_slot = slot
