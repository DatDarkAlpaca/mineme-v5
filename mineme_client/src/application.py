import os
from context import ClientContext
from mineme_core.constants import *
from mineme_core.network.network import MineSocket

class Application:
    def __init__(self):
        self.context = ClientContext()

        self.context.client_socket = MineSocket(os.environ.get('SERVER_ADDRESS'), int(os.environ.get('SERVER_PORT')))
        self.context.client_socket.set_timeout(CLIENT_TIMEOUT)
    
    def run(self):
        while self.context.running:
            self.context.view_handler.on_render()
            self.context.view_handler.on_update()
