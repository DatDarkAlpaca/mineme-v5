from enum import Enum, auto
from dataclasses import dataclass, field


class PacketType(Enum):
    INVALID = 0

    REGISTER_USER = auto()
    JOIN_USER = auto()
    LEAVE_USER = auto()

    CHECK_BALANCE = auto()
    MINE = auto()
    GAMBLE = auto()
    ORE = auto()
    PAY = auto()


@dataclass
class Packet:
    type: PacketType = PacketType.INVALID
    data: dict = field(default_factory=dict)


@dataclass
class RecvPacket:
    packet: Packet
    address: str

    def is_valid(self) -> bool:
        return self.packet.type and self.packet.type != PacketType.INVALID

    def get_reason(self) -> str:
        return self.packet.data.get("reason", "server possibly disconnected")

    def get_session_token(self) -> str | None:
        return self.packet.data.get("session_token")
