from typing import Protocol
from mineme_core.network.packet import Packet, PacketType


class NetworkProtocol(Protocol):
    def encode_packet(self, packet: Packet) -> bytes: ...

    def decode_packet(self, data: bytes) -> Packet: ...


class DefaultProtocol:
    def encode_packet(self, packet: Packet) -> bytes:
        return str(packet).encode()

    def decode_packet(self, data: bytes) -> Packet:
        return Packet(type=PacketType.INVALID, data=data.decode())
