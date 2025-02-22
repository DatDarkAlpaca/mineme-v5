from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from context import ServerContext
from utils.packet_utils import (
    send_invalid_session_packet,
    send_unauthenticated_packet,
    is_user_authenticated,
)


def users_callback(
    context: ServerContext, client_socket: MineSocket, packet_result: Packet
):
    session_handler = context.session_handler
    
    session_token = packet_result.get_session_token()
    session = context.session_handler.get(session_token)

    if not session:
        return send_invalid_session_packet(client_socket)

    if not is_user_authenticated(context.session_handler, packet_result):
        return send_unauthenticated_packet(client_socket)

    connected_users = []
    username = session.user.username
    for _, session_data in session_handler.items():
        if session_data.user.username == username:
            continue
        connected_users.append(session_data.user.username)

    data = {"users": connected_users}
    client_socket.send(Packet(PacketType.USERS, data))
