import bcrypt

from mineme_core.network.network import MineSocket
from mineme_core.network.packet import *


def view_register_user(args: list[str], client_socket: MineSocket):
    if len(args) < 2:
        return print('Usage: register <username> <password>')
        
    username = args[0]
    password = args[1]

    # username:
    data = {
        'username': username
    }
    client_socket.send(Packet(PacketType.REGISTER_USER, data=data))

    packet_result = client_socket.receive()

    if not packet_result.valid:
        return print(f"Usage: register <username> <password> | {packet_result.get_reason()}")

    salt = packet_result.packet.data['salt']

    # password:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt=salt.encode('utf-8')).decode()

    data = {
        'hash_pass': hashed_password
    }
    client_socket.send(Packet(PacketType.REGISTER_PASSWORD, data=data))

    packet_result = client_socket.receive()
    if not packet_result.valid:
        return print(f"Usage: register <username> <password> | {packet_result.get_reason()}")

    return print(f"Successfully registered user: {username}. Use the command 'join <username> <password>' to join")
