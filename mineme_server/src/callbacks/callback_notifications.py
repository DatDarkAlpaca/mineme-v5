from context import ServerContext
from utils.packet_utils import send_invalid_session_packet
from mineme_core.network.packet import Packet, PacketType, RecvPacket


def notifications_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    address = packet_result.address

    session_token = packet_result.get_session_token()
    session = context.session_data.get(session_token)

    if not session:
        return send_invalid_session_packet(server_socket, address)

    if len(session.notification_queue) == 0:
        data = {
            'reason': 'no notifications'
        }
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    data = {
        "messages": session.notification_queue
    }
    server_socket.send(Packet(PacketType.POLL_NOTIFICATION, data), address)
    
    session.notification_queue.clear()
