from mineme_core.network.packet import Packet, PacketType
from context import ClientContext


def handle_notifications(context: ClientContext):
    context.client_socket.send(Packet(PacketType.POLL_NOTIFICATION))
    packet_result = context.client_socket.receive()

    print(packet_result.packet.data['message'])

