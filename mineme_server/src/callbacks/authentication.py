import uuid
import bcrypt
from mineme_core.network.network import *
from mineme_core.database.user_table import *

from application_data import ServerAppData
from client_data import ClientData


def register_user_callback(server_app: ServerAppData, packet_result: RecvPacket):
    user_table = server_app.database_data.user_table
    server_socket = server_app.server_socket
    clients = server_app.client_data

    address = packet_result.address
    username = packet_result.packet.data['username']

    if len(username) < 3:
        data = {
            'code': RESULT_FAILED,
            'reason': 'username must be at least 3x characters long'
        }
        return server_socket.send(Packet(PacketType.REGISTER_USER, data), address)

    elif len(username) > 20:
        data = {
            'code': RESULT_FAILED,
            'reason': 'username must be at less than 20x characters long'
        }
        return server_socket.send(Packet(PacketType.REGISTER_USER, data), address)

    if user_table.exists_user(username):
        data = {
            'code': RESULT_FAILED,
            'reason': f"username {user_table} is taken"
        }
        return server_socket.send(Packet(PacketType.REGISTER_USER, data), address)

    data = {
        'salt': bcrypt.gensalt().decode()
    }
    server_socket.send(Packet(PacketType.REGISTER_USER, data), address)

    clients[address] = ClientData()
    clients[address].user.username = username


def register_password_callback(server_app: ServerAppData, packet_result: RecvPacket):
    server_socket = server_app.server_socket
    user_table = server_app.database_data.user_table
    player_table = server_app.database_data.player_table
    
    address = packet_result.address
    client = server_app.client_data[address]
    
    salted_password = packet_result.packet.data['hash_pass']

    entry = User(str(uuid.uuid4()), client.user.username, client.user.username, salted_password)
    if not user_table.insert_user(entry):
        data = {
            'code': RESULT_FAILED,
            'reason': 'failed to insert user inside database. please contact the admins.'
        }
        return server_socket.send(PacketType.REGISTER_PASSWORD, data, address)

    if not player_table.insert_player(entry.uid):
        data = {
            'code': RESULT_FAILED,
            'reason': 'failed to insert player inside database. please contact the admins.'
        }
        return server_socket.send(PacketType.REGISTER_PASSWORD, data, address)

    server_socket.send(Packet(PacketType.REGISTER_PASSWORD), address)


def join_user_callback(server_app: ServerAppData, packet_result: RecvPacket):
    server_socket = server_app.server_socket
    user_table = server_app.database_data.user_table

    address = packet_result.address
    clients = server_app.client_data
    
    if address not in clients:
        server_app.client_data[address] = ClientData()

    client = server_app.client_data[address]

    username = packet_result.packet.data['username']
    password = packet_result.packet.data['password']

    if not user_table.verify_user(username, password):
        data = {
            'code': RESULT_FAILED,
            'reason': 'invalid credentials'
        }
        return server_socket.send(Packet(PacketType.JOIN_USER, data), address)
    
    user_entry = user_table.fetch_user(username)

    client.authenticated = True
    client.user.uid = user_entry.uid
    client.user.username = user_entry.username
    client.user.display_name = user_entry.display_name

    data = {
        'code': RESULT_PASSED,
        'username': client.user.username,
        'display_name': client.user.display_name
    }
    server_socket.send(Packet(PacketType.JOIN_USER, data), address)


def unauthenticated_callback(server_app: ServerAppData, packet_result: RecvPacket):
    server_socket = server_app.server_socket
    
    data = {
        'code': RESULT_FAILED,
        'reason': 'user not authenticated'
    }
    return server_socket.send(Packet(PacketType.NOT_AUTH, data), packet_result.address)


def leave_user_callback(server_app: ServerAppData, packet_result: RecvPacket):
    del server_app.client_data[packet_result.address]
