from enum import Enum
from dataclasses import dataclass


class PacketType(Enum):
    REGISTER_USER = 0
    REGISTER_PASSWORD = 2
    JOIN_USER = 4
    NOT_AUTH = 5,

    MINE_COMMAND = 6


@dataclass
class Packet:
    type: PacketType
    data: str
