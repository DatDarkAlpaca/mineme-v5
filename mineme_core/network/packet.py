from enum import Enum
from dataclasses import dataclass


class PacketType(Enum):
    REGISTER_USER = 0
    REGISTER_USER_RESPONSE = 1
    REGISTER_PASSWORD = 2
    REGISTER_PASSWORD_RESPONSE = 3
    JOIN_USER = 4
    JOIN_USER_RESPONSE = 5


@dataclass
class Packet:
    type: PacketType
    data: str
