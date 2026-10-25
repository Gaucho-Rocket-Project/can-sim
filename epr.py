from can_interface import *
from utils import *
import time

def epr(fault_after: float | None = None) -> None:
    """Electronic Pressure Regulator (EPR) emulator: *reports* synthetic readiness/safe state."""
    with can.Bus(channel="vcan0", interface="socketcan") as bus:
        start = time.monotonic()
        next_send = start
        last_mcu_heartbeat = None
        last_state = None
        log("EPR", "Running: mocked tank status, safety and vent-request flags")
        while True:
            t = time.monotonic()
            msg = bus.recv(timeout=0.05)
            if is_valid_message_frame(msg, MCU_SHUTDOWN_LEN) and msg.arbitration_id == MCU_SHUTDOWN:
                send(bus, EPR_STATUS, EPR_SAFE, 0, 1)
                log("EPR", "Shutdown received; SAFE, vent requested")
                return
            elif is_valid_message_frame(msg, MCU_HEARTBEAT_LEN) and msg.arbitration_id == MCU_HEARTBEAT:
                last_mcu_heartbeat = t
            # Create fault after specified time
            injected_fault = fault_after is not None and t - start >= fault_after
            ready = fresh(last_mcu_heartbeat, t) and not injected_fault
            state = EPR_READY if ready else EPR_SAFE
            virtual_tank_signal = 70 if ready else 0
            vent_requested = 0 if ready else 1

            if t >= next_send:
                send(bus, EPR_STATUS, state, virtual_tank_signal, vent_requested)
                next_send = t + PERIOD

            if state != last_state:
                log("EPR", f"state={'READY' if ready else 'SAFE'} | "
                             f"virtual tank={virtual_tank_signal} | "
                             f"vent-request flag={vent_requested}")
                last_state = state
