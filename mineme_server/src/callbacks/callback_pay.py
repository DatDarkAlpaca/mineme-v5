from mineme_core.constants import CURRENCY_SYMBOL
from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from context import ServerContext
from utils.packet_utils import (
    send_invalid_session_packet, 
    send_unauthenticated_packet,
    is_user_authenticated
)


def pay_callback(context: ServerContext, client_socket: MineSocket, packet_result: Packet):
    user_table = context.database_data.user_table
    player_table = context.database_data.player_table

    session_token = packet_result.get_session_token()
    session = context.session_handler.get(session_token)

    if not session:
        return send_invalid_session_packet(client_socket)

    if not is_user_authenticated(context.session_handler, packet_result):
        return send_unauthenticated_packet(client_socket)

    def send_invalid_args():
        data = {"reason": f"invalid arguments: username={username} | amount={amount}"}
        return client_socket.send(Packet(PacketType.INVALID, data))

    try:
        username = packet_result.data.get("username")
        amount = float(packet_result.data.get("amount"))
    except Exception:
        return send_invalid_args()

    if not amount or not username:
        return send_invalid_args()

    # TOOD: check if username exists:
    receiver_user = user_table.fetch_user(username)
    receiver_uid = receiver_user.uid

    uid = session.user.uid
    balance = player_table.fetch_player(uid).balance

    if balance < amount:
        data = {
            "reason": f"you do not have the required funds to pay {username}. Your current balance is: {CURRENCY_SYMBOL}{balance}"
        }
        return client_socket.send(Packet(PacketType.INVALID, data))

    # update sender's balance:
    player_table.update_player_balance(uid, balance - amount)

    # update receiver's balance:
    receiver_balance = player_table.fetch_player(receiver_uid).balance
    player_table.update_player_balance(receiver_uid, receiver_balance + amount)

    # send a notification to the receiver:
    for _, receiver_session in context.session_handler.items():
        if receiver_session.user.username == username:
            receiver_session.notification_queue.append(f"{session.user.display_name} sent you {CURRENCY_SYMBOL}{amount:.2f}")

    client_socket.send(Packet(PacketType.PAY, {}))
