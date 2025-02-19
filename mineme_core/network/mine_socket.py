import socket
from mineme_core.network.packet import Packet, PacketType, RecvPacket
from mineme_core.network.protocol import NetworkProtocol


class MineSocket:
    SOCKET_RECV_BUFFER_LEN = 1024

    def __init__(self, port: int, network_protocol: NetworkProtocol):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.network_protocol: NetworkProtocol = network_protocol
        self.port = port

    def send(self, packet: Packet, address) -> None:
        self.socket.sendto(self.network_protocol.encode_packet(packet), address)

    def receive(self) -> RecvPacket:
        try:
            data, address = self.socket.recvfrom(MineSocket.SOCKET_RECV_BUFFER_LEN)

        except socket.timeout:
            return RecvPacket(Packet(PacketType.INVALID), {"reason": "request timeout"})

        except Exception as e:
            return RecvPacket(Packet(PacketType.INVALID), {"reason": e})

        return RecvPacket(self.network_protocol.decode_packet(data), address)
