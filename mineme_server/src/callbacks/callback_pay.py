from mineme_core.constants import CURRENCY_SYMBOL
from mineme_core.network.packet import Packet, RecvPacket, PacketType

from context import ServerContext
from utils.packet_utils import send_invalid_session_packet


def pay_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    user_table = context.database_data.user_table
    player_table = context.database_data.player_table

    address = packet_result.address

    session_token = packet_result.get_session_token()
    session = context.session_data.get(session_token)

    if not session:
        return send_invalid_session_packet(server_socket, address)

    def send_invalid_args():
        data = {"reason": f"invalid arguments: username={username} | amount={amount}"}
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    try:
        username = packet_result.packet.data.get("username")
        amount = float(packet_result.packet.data.get("amount"))
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
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    # update sender's balance:
    player_table.update_player_balance(uid, balance - amount)

    # update receiver's balance:
    receiver_balance = player_table.fetch_player(receiver_uid).balance
    player_table.update_player_balance(receiver_uid, receiver_balance + amount)

    # send a notification to the receiver:
    for _, receiver_session in context.session_data.items():
        if receiver_session.user.username == username:
            receiver_session.notification_queue.append(f"{session.user.display_name} sent you {CURRENCY_SYMBOL}{amount:.2f}")

    server_socket.send(Packet(PacketType.PAY, {}), address)
