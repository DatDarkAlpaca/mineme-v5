import os
from threading import Thread
from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet_handler import PacketHandler

from session_data import SessionHandler


class ServerSocket(MineSocket):
    def __init__(self, host: str, port: int, network_protocol, packet_handler: PacketHandler, session_handler: SessionHandler):
        super().__init__(host, port, network_protocol)

        self.packet_handler = packet_handler
        self.session_handler = session_handler

        self.initialize()

    def initialize(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(int(os.environ.get("SERVER_CAPACITY")))

    def execute(self):
        while True:
            client_socket, client_address = self.socket.accept()
            client_mine_socket = MineSocket(network_protocol=self.network_protocol)
            client_mine_socket.set_socket(client_socket)

            client_thread = Thread(target=lambda: self.handle_client(client_mine_socket), daemon=True)
            client_thread.start()

    def handle_client(self, client_socket: MineSocket):
        while True:
            packet_result = client_socket.receive()
            if not packet_result.is_valid():
                return self.session_handler.remove_from_address(client_socket.socket.getpeername())

            self.packet_handler.execute_packet(client_socket, packet_result)
