import os
from mineme_core.network.mine_socket import MineSocket, Packet


class ClientSocket(MineSocket):
    def __init__(self, host, port: int, network_protocol):
        super().__init__(host, port, network_protocol)
        self.socket.settimeout(float(os.environ.get("CLIENT_TIMEOUT"))) 

    def send(self, packet: Packet) -> None:
        super().send(packet, (self.host, self.port))
