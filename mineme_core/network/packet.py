from enum import Enum, auto
from dataclasses import dataclass


class PacketType(Enum):
    REGISTER_USER       = auto()
    REGISTER_PASSWORD   = auto()
    JOIN_USER           = auto()
    LEAVE_USER          = auto()
    NOT_AUTH            = auto()


@dataclass
class Packet:
    type: PacketType
    data: str
