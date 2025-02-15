from dataclasses import dataclass, field

from datetime import datetime
from mineme_core.game.user import User
from mineme_core.network.network import *

type session_token = str


@dataclass
class SessionData:
    user: User = field(default_factory=User)
    authenticated: bool = False
    command_delays: dict[PacketType, datetime] = field(default_factory=dict)
    last_activity: datetime = field(default=datetime.now())

    def __post_init__(self):
        now = datetime.now()
        for type in PacketType:
            self.command_delays[type] = now

    def set_command_delay(self, type):
        self.command_delays[type] = datetime.now()
