import os

from mineme_core.constants import *
from mineme_core.console import Console
from mineme_core.view import ViewHandler
from mineme_core.network.network import MineSocket


class Application:
    def __init__(self):
        self.view_handler = ViewHandler()
        self.console = Console()
        self.running = True

        self.client_socket = MineSocket(os.environ.get('SERVER_ADDRESS'), int(os.environ.get('SERVER_PORT')))
        self.client_socket.set_timeout(SERVER_TIMEOUT)

    def run(self):
        while self.running:
            self.view_handler.on_render()
            self.view_handler.on_update()
