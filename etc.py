from can_interface import *
from utils import *
import time

def etc():
    """Electronic Throttle Control (ETC) emulator: evaluates fresh peer status and reports mock actuator."""
    with can.Bus(channel="vcan0", interface="socketcan") as bus:
        next_send = time.monotonic()
        requested = 0
        last_thrust_request = None
        last_mcu_heartbeat = None
        last_press_status = None
        press_state = EPR_STANDBY
        last_mode = None
        log("ETC", "Running: synthetic temperature/pressure and actuator status")
        while True:
            msg = bus.recv(timeout=0.05)
            t = time.monotonic()
            if msg and not msg.is_extended_id:
                if msg.arbitration_id == THRUST_REQUEST and len(msg.data) == 1:
                    requested = min(100, msg.data[0])
                    last_thrust_request = t
                elif msg.arbitration_id == MCU_HEARTBEAT and len(msg.data) == 1:
                    last_mcu_heartbeat = t
                elif msg.arbitration_id == EPR_STATUS and len(msg.data) == 3:
                    press_state = msg.data[0]
                    last_press_status = t

            # Placeholder sensor readings
            virtual_temperature_signal = 25
            virtual_pressure_signal = 70
            enabled = (
                fresh(last_thrust_request, t)
                and fresh(last_mcu_heartbeat, t)
                and fresh(last_press_status, t)
                and press_state == EPR_READY
            )
            mode = THROTTLE_ENABLED if enabled else THROTTLE_INHIBITED
            virtual_actuator_pct = requested if enabled else 0

            if t >= next_send:
                send(bus, ETC_STATUS, mode, virtual_actuator_pct,
                     virtual_temperature_signal, virtual_pressure_signal)
                next_send = t + PERIOD

            if mode != last_mode:
                log("ETC", f"mode={'ENABLED' if enabled else 'INHIBITED'} | "
                                f"virtual actuator={virtual_actuator_pct}% | "
                                f"temp signal={virtual_temperature_signal}, "
                                f"pressure signal={virtual_pressure_signal}")
                last_mode = mode