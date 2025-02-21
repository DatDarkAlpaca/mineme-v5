import socket
from typing import Optional
from mineme_core.network.packet import Packet, PacketType
from mineme_core.network.protocol import NetworkProtocol, DefaultProtocol


class MineSocket:
    SOCKET_RECV_BUFFER_LEN = 1024

    def __init__(
        self,
        host: Optional[str] = "",
        port: Optional[int] = 0,
        network_protocol: NetworkProtocol = DefaultProtocol(),
    ):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.network_protocol: NetworkProtocol = network_protocol
        self.host = host
        self.port = port

    def set_socket(self, socket):
        self.socket = socket

    def close(self):
        self.socket.close()

    def send(self, packet: Packet) -> bool:
        try:
            self.socket.sendall(self.network_protocol.encode_packet(packet))
            return True

        except ConnectionResetError:
            return False

        except socket.timeout:
            return False

    def receive(self) -> Packet:
        try:
            data = self.socket.recv(MineSocket.SOCKET_RECV_BUFFER_LEN)

        except socket.timeout:
            return Packet(type=PacketType.INVALID, data={"reason": "request timeout"})

        except Exception as e:
            return Packet(type=PacketType.INVALID, data={"reason": e})

        return self.network_protocol.decode_packet(data)
