import json
import socket
from mineme_core.network.packet import *


RESULT_PASSED = 0
RESULT_FAILED = 1


class MineSocket:
    def __init__(self, address: str = '', port: int = 0):
        self.address: str = address
        self.port: int = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send(self, packet: Packet, address=None):
        if not address:
            address = (self.address, self.port)

        self.socket.sendto(self._encode_packet(packet), address)

    def receive(self) -> RecvPacket:
        try:
            data, address = self.socket.recvfrom(1024)
            recv_packet = RecvPacket(packet=self._decode_packet(data), address=address, valid=True)

            if recv_packet.packet.data['code'] == RESULT_FAILED:
                recv_packet.valid = False

            return recv_packet          

        except socket.timeout:
            return RecvPacket(packet=Packet(), address='', valid=False)
        
        except Exception as e:
            return RecvPacket(packet=Packet(), address='', valid=False)

    def set_timeout(self, timeout: float):
        self.socket.settimeout(timeout)

    def _encode_packet(self, packet: Packet):
        packet_data = {
            'type': packet.type.value,
        }

        if not packet_data.get('code'):
            packet_data['code'] = RESULT_PASSED

        if packet_data['code'] == RESULT_FAILED and not packet_data.get('reason'):
            packet_data['reason'] = 'unknown reason'

        packet_data.update(packet.data)

        packet_string = json.dumps(packet_data)
        return packet_string.encode()

    def _decode_packet(self, data: bytes) -> Packet:
        packet_data = data.decode()
        packet_obj = json.loads(packet_data)

        type = PacketType(packet_obj['type'])

        return Packet(type=type, data=packet_obj)


def initialize_server_socket(host: str, port: int) -> MineSocket:
    server_socket = MineSocket(host, port)
    server_socket.socket.bind((host, port))
    return server_socket
