from mineme_core.network.network import *
from mineme_core.database.player_table import *

from user import User


def handle_balance(user: User, address, server_socket: MineSocket, player_table: PlayerTable):
    uid = user.uid
    player = player_table.fetch_player(uid)

    if not player:
        return server_socket.send_packet(PacketType.CHECK_BALANCE, '0', address)   

    server_socket.send_packet(PacketType.CHECK_BALANCE, player.balance, address)
