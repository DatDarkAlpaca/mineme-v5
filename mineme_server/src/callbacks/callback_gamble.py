import random
from math import sqrt

from mineme_core.constants import CURRENCY_SYMBOL
from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from context import ServerContext
from utils.packet_utils import (
    send_invalid_session_packet,
    send_unauthenticated_packet,
    is_user_authenticated,
)


def gamble_callback(
    context: ServerContext, client_socket: MineSocket, packet_result: Packet
):
    player_table = context.database_data.player_table

    session_token = packet_result.get_session_token()
    session = context.session_handler.get(session_token)

    if not session:
        return send_invalid_session_packet(client_socket)

    if not is_user_authenticated(context.session_handler, packet_result):
        return send_unauthenticated_packet(client_socket)

    def send_invalid_args():
        data = {
            "reason": f"invalid arguments: amount={amount} | multiplier={multiplier}"
        }
        return client_socket.send(Packet(PacketType.INVALID, data))

    try:
        amount = float(packet_result.data.get("amount"))
        multiplier = float(packet_result.data.get("multiplier"))
    except Exception:
        return send_invalid_args()

    if not amount or not multiplier:
        return send_invalid_args()

    if multiplier <= 1.0 or multiplier > 10.0:
        data = {"reason": "multipler must be greater than 1.0, and smaller than 10.0"}
        return client_socket.send(Packet(PacketType.INVALID, data))

    uid = session.user.uid
    balance = player_table.fetch_player(uid).balance

    if balance < amount:
        data = {
            "reason": f"you do not have the required funds to gamble. your current balance is: {CURRENCY_SYMBOL}{balance}"
        }
        return client_socket.send(Packet(PacketType.INVALID, data))

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
    client_socket.send(Packet(PacketType.GAMBLE, data))
