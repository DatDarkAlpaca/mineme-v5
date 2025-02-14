import json

from mineme_core.game.ore import Ore
from mineme_core.network.network import *
from mineme_core.database.player_table import *

from mineme_core.game.mine import mine

from user import User


def handle_balance(user: User, address, server_socket: MineSocket, player_table: PlayerTable):
    uid = user.uid
    player = player_table.fetch_player(uid)

    if not player:
        return server_socket.send_packet(PacketType.CHECK_BALANCE, '12', address)   

    server_socket.send_packet(PacketType.CHECK_BALANCE, str(player.balance), address)


def handle_mine(user: User, address, server_socket: MineSocket, player_table: PlayerTable, ores: list[Ore]):
    uid = user.uid
    player = player_table.fetch_player(uid)

    if not player:
        return server_socket.send_packet(PacketType.MINE, '1,player_not_found', address)

    ore_data = mine(ores)
    price = ore_data.ore.price * ore_data.weight

    data = {
        'ore_name': ore_data.ore.name,
        'weight': ore_data.weight,
        'price': price
    }

    return server_socket.send_packet(PacketType.MINE, f"0,{json.dumps(data)}", address)
