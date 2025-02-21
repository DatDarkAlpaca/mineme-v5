from mineme_core.network.packet import Packet, PacketType, RecvPacket

from context import ServerContext
from utils.packet_utils import (
    send_invalid_session_packet, 
    send_unauthenticated_packet,
    is_user_authenticated
)

def balance_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    player_table = context.database_data.player_table

    address = packet_result.address

    session_token = packet_result.get_session_token()
    session = context.session_data.get(session_token)

    if not session:
        return send_invalid_session_packet(server_socket, address)

    if not is_user_authenticated(context.session_data, packet_result):
        return send_unauthenticated_packet(server_socket, address)


    uid = session.user.uid
    player = player_table.fetch_player(uid)

    if not player:
        data = {"reason": f"player {uid} not found"}
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    data = {"balance": player.balance}
    server_socket.send(Packet(PacketType.CHECK_BALANCE, data), address)
