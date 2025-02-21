from typing import Any
from dataclasses import dataclass, field

from datetime import datetime
from mineme_core.game.user import User
from mineme_core.network.command_cooldown import CommandCooldown

type session_token = str


@dataclass
class SessionData:
    address: Any = None
    notification_queue: list[str] = field(default_factory=list)
    user: User = field(default_factory=User)
    authenticated: bool = False
    command_cooldowns: CommandCooldown = field(default_factory=CommandCooldown)

    def __post_init__(self):
        self.last_activity = datetime.now()


class SessionHandler:
    def __init__(self):
        self.sessions: dict[session_token, SessionData] = {}

    def add(self, token: session_token, session: SessionData):
        self.sessions[token] = session

    def get(self, token: session_token):
        return self.sessions.get(token)
        
    def items(self):
        return self.sessions.items()

    def remove(self, token: session_token):
        return self.sessions.pop(token)
    
    def remove_from_address(self, address):
        session_token = None
        for token, session in self.sessions.items():
            if session.address == address:
                session_token = token
                break

        self.remove(session_token)
            
    def __len__(self):
        return len(self.sessions)
        