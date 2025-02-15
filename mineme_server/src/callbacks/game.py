import random
from math import sqrt

from mineme_core.game.mine import mine
from mineme_core.network.network import *
from mineme_core.database.player_table import *
from mineme_core.constants import CURRENCY_SYMBOL
from mineme_server.src.application_context import ServerContext

from utils.packet_utils import *


def check_balance_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    player_table = context.database_data.player_table

    address = packet_result.address

    session_token = packet_result.get_session_token()
    session = context.session_data.get(session_token)

    if not session:
        return send_invalid_session_packet(server_socket, address)

    uid = session.user.uid
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
        data = {
            'code': RESULT_FAILED,
            'reason': f"player {uid} not found"
        }
        return server_socket.send(Packet(PacketType.MINE, data), address)

    ore_data = mine(ores)
    ore_price = ore_data.ore.price * ore_data.weight

    data = {
        'code': RESULT_PASSED,
        'ore_name': ore_data.ore.name,
        'weight': ore_data.weight,
        'price': ore_price,
        'min_weight': ore_data.ore.min_weight,
        'max_weight': ore_data.ore.max_weight
    }

    balance = player.balance
    player_table.update_player_balance(uid, balance + ore_price)

    return server_socket.send(Packet(PacketType.MINE, data), address)


def gamble_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    player_table = context.database_data.player_table

    address = packet_result.address

    session_token = packet_result.get_session_token()
    session = context.session_data.get(session_token)

    if not session:
        return send_invalid_session_packet(server_socket, address)

    def send_invalid_args():
        data = {
            'code': RESULT_FAILED,
            'reason': f"invalid arguments: amount={amount} | multiplier={multiplier}"
        }
        return server_socket.send(Packet(PacketType.GAMBLE, data), address)

    try:
        amount = float(packet_result.packet.data.get('amount'))
        multiplier = float(packet_result.packet.data.get('multiplier'))
    except:
        return send_invalid_args()
    
    if not amount or not multiplier:
        return send_invalid_args()
    
    uid = session.user.uid
    balance = player_table.fetch_player(uid).balance
    
    if multiplier <= 1.0 or multiplier > 10.0:
        data = {
            'code': RESULT_FAILED,
            'reason': f"multipler must be greater than 1.0, and smaller than 10.0"
        }
        return server_socket.send(Packet(PacketType.GAMBLE, data), address)

    if balance < amount:
        data = {
            'code': RESULT_FAILED,
            'reason': f"you do not have the required funds to gamble. your current balance is: {CURRENCY_SYMBOL}{balance}"
        }
        return server_socket.send(Packet(PacketType.GAMBLE, data), address)

    odds = (sqrt(1/5) ** multiplier) * 100
    random_number = random.uniform(0, 100)
    win = random_number <= odds

    data = {
        'win': 1 if win else 0
    }
    server_socket.send(Packet(PacketType.GAMBLE, data), address)

    balance = player_table.fetch_player(session.user.uid).balance

    if win:
        new_balance = balance + amount * multiplier 
    else:
        new_balance = balance - amount

    player_table.update_player_balance(session.user.uid, new_balance)
