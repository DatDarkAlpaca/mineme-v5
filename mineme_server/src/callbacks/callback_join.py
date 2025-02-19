import os
import uuid

from mineme_core.network.packet import Packet, PacketType, RecvPacket

from session_data import SessionData
from context import ServerContext


def create_session_token() -> str:
    return str(uuid.uuid4())


def join_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    user_table = context.database_data.user_table
    session_data = context.session_data

    address = packet_result.address

    username = packet_result.packet.data["username"]
    password = packet_result.packet.data["password"]

    if len(context.session_data) >= int(os.environ.get("SERVER_CAPACITY")):
        data = {"reason": "server currently full. please try again later."}
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    if not user_table.verify_user(username, password):
        data = {"reason": "invalid credentials"}
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    for session_token, session_info in session_data.items():
        if session_info.user.username == username:
            data = {"reason": "user already connected"}
            return server_socket.send(Packet(PacketType.INVALID, data), address)

    user_entry = user_table.fetch_user(username)

    # session:
    session_token = create_session_token()
    session_data[session_token] = SessionData()

    session = session_data[session_token]
    session.authenticated = True

    session.address = address
    session.user.uid = user_entry.uid
    session.user.username = user_entry.username
    session.user.display_name = user_entry.display_name

    data = {
        "session_token": session_token,
        "username": session.user.username,
        "display_name": session.user.display_name,
    }

    server_socket.send(Packet(PacketType.JOIN_USER, data), address)
