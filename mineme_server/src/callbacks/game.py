import json

from mineme_core.game.ore import Ore
from mineme_core.network.network import *
from mineme_core.database.player_table import *

from mineme_core.game.user import User
from mineme_core.game.mine import mine

from application_data import ServerAppData


def check_balance_callback(server_app: ServerAppData, packet: RecvPacket):
    server_socket = server_app.server_socket
    player_table = server_app.database_data.player_table

    address = packet.address
    client = server_app.client_data[packet.address]

    uid = client.user.uid
    player = player_table.fetch_player(uid)

    if not player:
        data = {
            'code': RESULT_FAILED,
            'reason': f"player {uid} not found"
        }

        return server_socket.send(Packet(PacketType.CHECK_BALANCE, data), address)

    data = {
        'code': RESULT_PASSED,
        'balance': player.balance
    }
    server_socket.send(Packet(PacketType.CHECK_BALANCE, data), address)


def mine_callback(server_app: ServerAppData, packet: RecvPacket):
    server_socket = server_app.server_socket
    player_table = server_app.database_data.player_table
    ores = server_app.database_data.ores

    address = packet.address
    client = server_app.client_data[address]

    uid = client.user.uid
    player = player_table.fetch_player(uid)
    
    if not player:
        data = {
            'code': RESULT_FAILED,
            'reason': f"player {player.uid} not found"
        }
        return server_socket.send(Packet(PacketType.MINE, data), address)

    ore_data = mine(ores)
    ore_price = ore_data.ore.price * ore_data.weight

    data = {
        'code': RESULT_PASSED,
        'ore_name': ore_data.ore.name,
        'weight': ore_data.weight,
        'price': ore_price
    }

    balance = player.balance
    player_table.update_player_balance(uid, balance + ore_price)

    return server_socket.send(Packet(PacketType.MINE, data), address)

