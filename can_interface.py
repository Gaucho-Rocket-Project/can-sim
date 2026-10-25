import can

# CAN IDs
THRUST_REQUEST = 0x100
MCU_HEARTBEAT = 0x101
EPR_STATUS = 0x200
ETC_STATUS = 0x300

EPR_STANDBY = 0
EPR_READY = 1
EPR_SAFE = 2

THROTTLE_INHIBITED = 0
THROTTLE_ENABLED = 1

PERIOD = 0.25  # seconds
TIMEOUT = 1.0  # seconds

def send(bus: can.BusABC, can_id: int, *data: int) -> None:
    '''
    CAN transmit function

    Constructs a CAN frame and sends it onto `bus`

    `bus`	    SocketCAN bus interface

    `can_id`	Arbitration ID identifying the message

    `*data`	    Variable number of payload bytes
    '''
    bus.send(
        can.Message(
            arbitration_id=can_id,
            data=bytes(data),
            is_extended_id=False,
        ),
        timeout=0.1,
    )


def fresh(timestamp: float | None, t: float) -> bool:
    '''
    Determines whether the last message received from another node is recent enough to be valid.
    '''
    return timestamp is not None and t - timestamp < TIMEOUT