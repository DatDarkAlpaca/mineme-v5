import bcrypt
import uuid
from mineme_core.database.user_database import *
from mineme_core.network.network import Packet, PacketType, MineSocket

from user import User


def handle_user_registration_username(cursor, server_socket: MineSocket, packet: Packet, address: str, clients):
    username = packet.data

    if len(username) < 3:
        return server_socket.send_packet(PacketType.REGISTER_USER_RESPONSE, '1,short', address)

    if exists_username_entry(cursor, username):
        return server_socket.send_packet(PacketType.REGISTER_USER_RESPONSE, '1,taken', address)

    salt = bcrypt.gensalt().decode()
    server_socket.send_packet(PacketType.REGISTER_USER_RESPONSE, '0,' + salt, address)

    clients[address] = User(username=username)


def handle_user_registration_password(cursor, server_socket: MineSocket, packet: Packet, address: str, client: User):
    salted_password = packet.data

    entry = UserEntry(str(uuid.uuid4()), client.username, client.username, salted_password)
    if not create_user_entry(cursor, entry):
        return server_socket.send_packet(PacketType.REGISTER_PASSWORD_RESPONSE, '1,database', address)

    server_socket.send_packet(PacketType.REGISTER_PASSWORD_RESPONSE, '0,success', address)


def handle_user_join(cursor, server_socket: MineSocket, packet: Packet, address: str, clients: dict[User]):
    if address not in clients:
        clients[address] = User('', '', '')

    client = clients[address]

    username, password = packet.data.split(',')
    if not verify_user_entry(cursor, username, password):
        return server_socket.send_packet(PacketType.JOIN_USER_RESPONSE, '1,invalid', address)
    
    user_entry = fetch_user_entry(cursor, username)

    client.username = user_entry.username
    client.display_name = user_entry.display_name
    client.uid = user_entry.uid

    server_socket.send_packet(PacketType.JOIN_USER_RESPONSE, '0,success', address)
