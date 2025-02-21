from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from context import ServerContext
from utils.packet_utils import send_invalid_session_packet


def notifications_callback(
    context: ServerContext, client_socket: MineSocket, packet_result: Packet
):
    session_token = packet_result.get_session_token()
    session = context.session_handler.get(session_token)

    if not session:
        return send_invalid_session_packet(client_socket)

    if len(session.notification_queue) == 0:
        data = {"reason": "no notifications"}
        return client_socket.send(Packet(PacketType.INVALID, data))

    data = {"messages": session.notification_queue}
    client_socket.send(Packet(PacketType.POLL_NOTIFICATION, data))

    session.notification_queue.clear()
