import os
import uuid

from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from session_data import SessionData
from context import ServerContext


def create_session_token() -> str:
    return str(uuid.uuid4())


def join_callback(context: ServerContext, client_socket: MineSocket, packet_result: Packet):
    user_table = context.database_data.user_table
    session_handler = context.session_handler

    username = packet_result.data["username"]
    password = packet_result.data["password"]

    if len(context.session_handler) >= int(os.environ.get("SERVER_CAPACITY")):
        data = {"reason": "server currently full. please try again later."}
        return client_socket.send(Packet(PacketType.INVALID, data))

    if not user_table.verify_user(username, password):
        data = {"reason": "invalid credentials"}
        return client_socket.send(Packet(PacketType.INVALID, data))

    for session_token, session_info in session_handler.items():
        if session_info.user.username == username:
            data = {"reason": "user already connected"}
            return client_socket.send(Packet(PacketType.INVALID, data))

    user_entry = user_table.fetch_user(username)

    # session:
    session_token = create_session_token()
    session_handler.add(session_token, SessionData())

    session = session_handler.get(session_token)
    session.authenticated = True
    session.address = client_socket.socket.getpeername()

    session.user.uid = user_entry.uid
    session.user.username = user_entry.username
    session.user.display_name = user_entry.display_name

    data = {
        "session_token": session_token,
        "username": session.user.username,
        "display_name": session.user.display_name,
    }

    client_socket.send(Packet(PacketType.JOIN_USER, data))
