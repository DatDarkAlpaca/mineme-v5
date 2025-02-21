from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from context import ServerContext
from utils.packet_utils import (
    send_invalid_session_packet,
    send_unauthenticated_packet,
    is_user_authenticated,
)


def balance_callback(
    context: ServerContext, client_socket: MineSocket, packet_result: Packet
):
    player_table = context.database_data.player_table

    session_token = packet_result.get_session_token()
    session = context.session_handler.get(session_token)

    if not session:
        return send_invalid_session_packet(client_socket)

    if not is_user_authenticated(context.session_handler, packet_result):
        return send_unauthenticated_packet(client_socket)

    uid = session.user.uid
    player = player_table.fetch_player(uid)

    if not player:
        data = {"reason": f"player {uid} not found"}
        return client_socket.send(Packet(PacketType.INVALID, data))

    data = {"balance": player.balance}
    client_socket.send(Packet(PacketType.CHECK_BALANCE, data))
