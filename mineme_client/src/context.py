import os
from dataclasses import dataclass, field

from mineme_core.console import Console
from mineme_core.view import ViewHandler
from mineme_core.network.ssp_protocol import SSP_Protocol

from client_socket import ClientSocket


@dataclass
class ClientContext:
    view_handler: ViewHandler = field(default_factory=ViewHandler)
    client_socket: None | ClientSocket = None
    console: Console = field(default_factory=Console)
    session_token: str = ""
    running: bool = True

    def __post_init__(self):
        ssp_protocol = SSP_Protocol()
        self.client_socket = ClientSocket(
            int(os.environ.get("SERVER_PORT")),
            os.environ.get("SERVER_ADDRESS"),
            ssp_protocol,
        )
