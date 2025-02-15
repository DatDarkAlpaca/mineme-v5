from dataclasses import dataclass, field
from mineme_core.game.user import User


@dataclass
class ClientData:
    user: User = field(default_factory=User)
    authenticated: bool = False
