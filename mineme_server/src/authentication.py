import bcrypt
import uuid
from mineme_core.database.user_table import *
from mineme_core.network.network import Packet, PacketType, MineSocket
from mineme_core.database.user_table import UserTable

from user import User


def handle_user_registration_username(user_table: UserTable, server_socket: MineSocket, packet: Packet, address: str, clients):
    username = packet.data

    if len(username) < 3:
        return server_socket.send_packet(PacketType.REGISTER_USER, '1,short', address)

    if user_table.exists_user(username):
        return server_socket.send_packet(PacketType.REGISTER_USER, '1,taken', address)

    salt = bcrypt.gensalt().decode()
    server_socket.send_packet(PacketType.REGISTER_USER, '0,' + salt, address)

    clients[address] = User(username=username)


def handle_user_registration_password(user_table: UserTable, server_socket: MineSocket, packet: Packet, address: str, client: User):
    salted_password = packet.data

    entry = UserEntry(str(uuid.uuid4()), client.username, client.username, salted_password)
    if not user_table.insert_user(entry):
        return server_socket.send_packet(PacketType.REGISTER_PASSWORD, '1,database', address)

    server_socket.send_packet(PacketType.REGISTER_PASSWORD, '0,success', address)


def handle_user_join(user_table: UserTable, server_socket: MineSocket, packet: Packet, address: str, clients: dict[User]):
    if address not in clients:
        clients[address] = User()

    client = clients[address]

    username, password = packet.data.split(',')
    if not user_table.verify_user(username, password):
        return server_socket.send_packet(PacketType.JOIN_USER, '1,invalid', address)
    
    user_entry = user_table.fetch_user(username)

    client.authenticated = True
    client.uid = user_entry.uid
    client.username = user_entry.username
    client.display_name = user_entry.display_name

    server_socket.send_packet(PacketType.JOIN_USER, '0,success', address)


def handle_user_not_authenticated(server_socket: MineSocket, address: str):
    return server_socket.send_packet(PacketType.NOT_AUTH, '', address)


def handle_user_left(address: str, clients: dict[User]):
    del clients[address]
