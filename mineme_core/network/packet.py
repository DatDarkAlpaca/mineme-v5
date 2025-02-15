from enum import Enum, auto
from dataclasses import dataclass, field


class PacketType(Enum):
    INVALID             = auto()

    REGISTER_USER       = auto()
    REGISTER_PASSWORD   = auto()
    JOIN_USER           = auto()
    LEAVE_USER          = auto()
    NOT_AUTH            = auto()

    CHECK_BALANCE       = auto()
    MINE                = auto()


@dataclass
class Packet:
    type: PacketType = PacketType.INVALID
    data: dict = field(default_factory=dict)


@dataclass
class RecvPacket:
    packet: Packet
    address: str
    valid: bool = True

    def get_reason(self) -> str:
        return self.packet.data['reason']
