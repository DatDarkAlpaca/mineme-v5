from dataclasses import dataclass, field

from datetime import datetime
from mineme_core.game.user import User

type session_token = str


@dataclass
class SessionData:
    user: User = field(default_factory=User)
    authenticated: bool = False
    last_activity: datetime = field(default=datetime.now())
