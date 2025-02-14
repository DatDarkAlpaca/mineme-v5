import socket
from mineme_core.network.packet import Packet, PacketType


class MineSocket:
    def __init__(self, address: str, port: int):
        self.address: str = address
        self.port: int = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def encode_packet(self, packet_type: PacketType, data: str):
        packet_data = str(packet_type.value) + ',' + data
        return packet_data.encode()

    def decode_packet(self, data: bytes) -> Packet:
        packet_type, data = data.decode().split(',', 1)
        return Packet(type=PacketType(int(packet_type)), data=data)

    def send_packet_default(self, packet_type: PacketType, data: str):
        self.socket.sendto(self.encode_packet(packet_type, data), (self.address, self.port))

    def send_packet(self, packet_type: PacketType, data: str, address):
        self.socket.sendto(self.encode_packet(packet_type, data), address)

    def receive_packet(self) -> tuple[Packet, str]:
        data, address = self.socket.recvfrom(1024)
        return (self.decode_packet(data), address)


def initialize_server_socket(host: str, port: int) -> MineSocket:
    server_socket = MineSocket(host, port)
    server_socket.socket.bind((host, port))
    return server_socket