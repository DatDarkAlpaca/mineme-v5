import os
from mineme_core.network.mine_socket import MineSocket, Packet


class ClientSocket(MineSocket):
    def __init__(self, port: int, host: str, network_protocol):
        super().__init__(port, network_protocol)
        self.socket.settimeout(float(os.environ.get("CLIENT_TIMEOUT")))
        self.address = host
        self.port = port

    def send(self, packet: Packet) -> None:
        super().send(packet, (self.address, self.port))
