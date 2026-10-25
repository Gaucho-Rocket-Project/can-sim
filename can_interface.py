import can
from can_config import *

def is_valid_message_frame(msg: can.Message | None, expected_length: int) -> bool:
    return (
        msg is not None
        and not msg.is_extended_id
        and not msg.is_remote_frame
        and not msg.is_error_frame
        and msg.dlc == len(msg.data) == expected_length
    )

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
