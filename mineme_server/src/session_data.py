from dataclasses import dataclass, field

from datetime import datetime
from mineme_core.game.user import User
from mineme_core.network.network import *
from mineme_core.network.command_cooldown import CommandCooldown

type session_token = str


@dataclass
class SessionData:
    user: User = field(default_factory=User)
    authenticated: bool = False
    command_cooldowns: CommandCooldown = field(default_factory=CommandCooldown)
    last_activity: datetime = field(default=datetime.now())
