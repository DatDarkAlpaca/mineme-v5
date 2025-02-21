from mineme_core.game.mine import mine
from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from context import ServerContext
from utils.packet_utils import (
    send_invalid_session_packet,
    send_unauthenticated_packet,
    is_user_authenticated,
)


def mine_callback(
    context: ServerContext, client_socket: MineSocket, packet_result: Packet
):
    player_table = context.database_data.player_table
    ores = context.database_data.ores

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

    ore_data = mine(ores)
    ore_price = ore_data.ore.price * ore_data.weight

    data = {
        "ore_name": ore_data.ore.name,
        "weight": ore_data.weight,
        "price": ore_price,
        "min_weight": ore_data.ore.min_weight,
        "max_weight": ore_data.ore.max_weight,
    }

    balance = player.balance
    player_table.update_player_balance(uid, balance + ore_price)

    return client_socket.send(Packet(PacketType.MINE, data))
