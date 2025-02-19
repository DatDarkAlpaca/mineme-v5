from dataclasses import dataclass, field

from datetime import datetime
from mineme_core.game.user import User
from mineme_core.network.command_cooldown import CommandCooldown

type session_token = str


@dataclass
class SessionData:
    address: str = ''
    notification_queue: list[str] = field(default_factory=list)
    user: User = field(default_factory=User)
    authenticated: bool = False
    command_cooldowns: CommandCooldown = field(default_factory=CommandCooldown)
    last_activity: datetime | None = None

    def __post_init__(self):
        self.last_activity = datetime.now()
