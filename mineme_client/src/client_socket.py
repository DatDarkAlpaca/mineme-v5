import os
from mineme_core.network.mine_socket import MineSocket


class ClientSocket(MineSocket):
    def __init__(self, host, port: int, network_protocol):
        super().__init__(host, port, network_protocol)
        self.socket.settimeout(float(os.environ.get("CLIENT_TIMEOUT")))
        self.connected = False

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True

            return True
        except Exception:
            return
