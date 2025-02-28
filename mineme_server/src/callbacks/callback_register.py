import uuid
import bcrypt

from mineme_core.database.user_table import User
from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from context import ServerContext


def register_callback(
    context: ServerContext, client_socket: MineSocket, packet_result: Packet
):
    user_table = context.database_data.user_table
    player_table = context.database_data.player_table

    username = packet_result.data["username"]
    password = packet_result.data["password"]

    # input validation:
    if len(username) < 3:
        data = {"reason": "username must be at least 3x characters long"}
        return client_socket.send(Packet(PacketType.INVALID, data))

    elif len(username) > 20:
        data = {"reason": "username must be at less than 20x characters long"}
        return client_socket.send(Packet(PacketType.INVALID, data))

    if len(password) < 8:
        data = {"reason": "password must be at least 8x characters long"}
        return client_socket.send(Packet(PacketType.INVALID, data))

    elif len(password) > 40:
        data = {"reason": "password must be at less than 40x characters long"}
        return client_socket.send(Packet(PacketType.INVALID, data))

    if user_table.exists_user(username):
        data = {"reason": f"username {user_table} is taken"}
        return client_socket.send(Packet(PacketType.INVALID, data))

    # password:
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"), salt=bcrypt.gensalt()
    ).decode()

    entry = User(str(uuid.uuid4()), username, username, hashed_password)
    if not user_table.insert_user(entry):
        data = {
            "reason": "failed to insert user inside database. please contact the admins."
        }
        return client_socket.send(PacketType.INVALID, data)

    if not player_table.insert_player(entry.uid):
        data = {
            "reason": "failed to insert player inside database. please contact the admins."
        }
        return client_socket.send(PacketType.INVALID, data)

    client_socket.send(Packet(PacketType.REGISTER_USER, {}))
