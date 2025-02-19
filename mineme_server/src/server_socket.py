from mineme_core.network.mine_socket import MineSocket


class ServerSocket(MineSocket):
    def __init__(self, host: str, port: int, network_protocol):
        super().__init__(port, network_protocol)

        self.socket.bind((host, port))

    def send(self, packet, address) -> None:
        super().send(packet, address)
