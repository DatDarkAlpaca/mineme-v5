from context import ClientContext
from mineme_core.network.packet import *


def send_leave_packet(context: ClientContext):
    data = {
        'session_token': context.session_token
    }

    context.client_socket.send(Packet(PacketType.LEAVE_USER, data))
