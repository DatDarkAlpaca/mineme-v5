from enum import Enum, auto
from dataclasses import dataclass, field


class PacketType(Enum):
    INVALID = auto()

    REGISTER_USER = auto()
    JOIN_USER = auto()
    LEAVE_USER = auto()

    CHECK_BALANCE = auto()
    MINE = auto()
    GAMBLE = auto()
    ORE = auto()
    PAY = auto()

    POLL_NOTIFICATION = auto()


@dataclass
class Packet:
    type: PacketType = PacketType.INVALID
    data: dict = field(default_factory=dict)

    def is_valid(self) -> bool:
        return self.type and self.type != PacketType.INVALID

    def get_reason(self) -> str:
        return self.data.get("reason", "server possibly disconnected")

    def get_session_token(self) -> str | None:
        return self.data.get("session_token")
