from dataclasses import dataclass, field

from mineme_core.console import Console
from mineme_core.view import ViewHandler
from mineme_core.network.network import MineSocket


@dataclass
class ClientContext:
    view_handler: ViewHandler = field(default_factory=ViewHandler)
    client_socket: MineSocket = field(default_factory=MineSocket)
    console: Console = field(default_factory=Console)
    session_token: str = ''
    running: bool = True
