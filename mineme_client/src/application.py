from context import ClientContext
from mineme_core.constants import *

from utils.packet_utils import send_leave_packet


class Application:
    def __init__(self):
        self.context = ClientContext()

    def run(self):
        while self.context.running:
            self.context.view_handler.on_render()

        send_leave_packet(self.context)
