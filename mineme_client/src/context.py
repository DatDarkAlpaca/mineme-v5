import os
from dataclasses import dataclass, field

from mineme_core.console import Console
from mineme_core.view import ViewHandler
from mineme_core.network.ssp_protocol import SSP_Protocol

from history import CommandHistory
from client_socket import ClientSocket


@dataclass
class ClientContext:
    command_history: CommandHistory = field(default_factory=CommandHistory)
    view_handler: ViewHandler = field(default_factory=ViewHandler)
    console: Console = field(default_factory=Console)
    client_socket: None | ClientSocket = None
    session_token: str = ""
    running: bool = True

    def __post_init__(self):
        ssp_protocol = SSP_Protocol()
        self.client_socket = ClientSocket(
            os.environ.get("SERVER_ADDRESS"),
            int(os.environ.get("SERVER_PORT")),
            ssp_protocol,
        )
