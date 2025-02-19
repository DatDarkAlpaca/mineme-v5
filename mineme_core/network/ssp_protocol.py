import json

from mineme_core.network.protocol import NetworkProtocol, Packet, PacketType


class SSP_Protocol(NetworkProtocol):
    """
    Super Simple Protocol
    """

    def encode_packet(self, packet: Packet) -> bytes:
        type = packet.type.value
        reason: str = packet.data.get("reason", "")

        packet_data = {
            "type": type,
        }

        if type == PacketType.INVALID and len(reason) == 0:
            packet_data["reason"] = "unknown reason"

        packet_data.update(packet.data)

        packet_string = json.dumps(packet_data)
        return packet_string.encode()

    def decode_packet(self, data: bytes) -> Packet:
        packet_object = json.loads(data.decode())
        type = PacketType(packet_object["type"])

        return Packet(type=type, data=packet_object)
