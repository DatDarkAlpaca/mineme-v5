from mineme_core.game.mine import mine
from mineme_core.network.packet import Packet, RecvPacket, PacketType

from utils.packet_utils import send_invalid_session_packet
from context import ServerContext


def mine_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    player_table = context.database_data.player_table
    ores = context.database_data.ores

    address = packet_result.address

    session_token = packet_result.get_session_token()
    session = context.session_data.get(session_token)

    if not session:
        return send_invalid_session_packet(server_socket, address)

    uid = session.user.uid
    player = player_table.fetch_player(uid)

    if not player:
        data = {"reason": f"player {uid} not found"}
        return server_socket.send(Packet(PacketType.INVALID, data), address)

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

    return server_socket.send(Packet(PacketType.MINE, data), address)
