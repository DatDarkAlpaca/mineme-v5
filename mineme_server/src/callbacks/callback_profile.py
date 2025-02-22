from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from context import ServerContext
from utils.packet_utils import (
    send_invalid_session_packet,
    send_unauthenticated_packet,
    is_user_authenticated,
)


def profile_callback(
    context: ServerContext, client_socket: MineSocket, packet_result: Packet
):
    session_handler = context.session_handler
    player_table = context.database_data.player_table
    context.database_data.user_table
    
    session_token = packet_result.get_session_token()
    session = session_handler.get(session_token)

    if not session:
        return send_invalid_session_packet(client_socket)

    if not is_user_authenticated(session_handler, packet_result):
        return send_unauthenticated_packet(client_socket)

    username = packet_result.data.get("username")
    
    profile_session = session_handler.get_from_username(username)
    if not profile_session:
        data = {
            "reason": f"user {username} does not exist"
        }
        return client_socket.send(Packet(PacketType.INVALID, data))

    player = player_table.fetch_player(profile_session.user.uid)
    if not player:
        data = {
            "reason": f"user {username} does not exist"
        }
        return client_socket.send(Packet(PacketType.INVALID, data))

    data = {
        "username": username,
        "display_name": profile_session.user.display_name,
        "balance": player.balance
    }
    client_socket.send(Packet(PacketType.USERS, data))
