import random
from math import sqrt

from mineme_core.network.packet import Packet, RecvPacket, PacketType

from utils.packet_utils import send_invalid_session_packet
from mineme_core.constants import *
from context import ServerContext


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
            "reason": f"invalid arguments: amount={amount} | multiplier={multiplier}"
        }
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    try:
        amount = float(packet_result.packet.data.get("amount"))
        multiplier = float(packet_result.packet.data.get("multiplier"))
    except:
        return send_invalid_args()

    if not amount or not multiplier:
        return send_invalid_args()

    if multiplier <= 1.0 or multiplier > 10.0:
        data = {"reason": "multipler must be greater than 1.0, and smaller than 10.0"}
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    uid = session.user.uid
    balance = player_table.fetch_player(uid).balance

    if balance < amount:
        data = {
            "reason": f"you do not have the required funds to gamble. your current balance is: {CURRENCY_SYMBOL}{balance}"
        }
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    odds = (sqrt(1 / 5) ** multiplier) * 100
    random_number = random.uniform(0, 100)
    win = random_number <= odds

    # update balance:
    balance = player_table.fetch_player(session.user.uid).balance

    if win:
        new_balance = balance + amount * multiplier
    else:
        new_balance = balance - amount

    player_table.update_player_balance(session.user.uid, new_balance)

    # packet:
    data = {"win": 1 if win else 0}
    server_socket.send(Packet(PacketType.GAMBLE, data), address)
