import uuid
import bcrypt
from mineme_core.network.network import *
from mineme_core.database.user_table import *

from mineme_server.src.application_context import ServerContext
from mineme_server.src.session_data import SessionData


def create_session_token() -> str:
    return str(uuid.uuid4())


def register_user_callback(context: ServerContext, packet_result: RecvPacket):
    user_table = context.database_data.user_table
    server_socket = context.server_socket
    session_data = context.session_data

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

    session_token = create_session_token()

    data = {
        'salt': bcrypt.gensalt().decode(),
        'session_token': session_token
    }
    server_socket.send(Packet(PacketType.REGISTER_USER, data), address)

    session_data[session_token] = SessionData()
    session_data[session_token].user.username = username


def register_password_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    user_table = context.database_data.user_table
    player_table = context.database_data.player_table
    
    address = packet_result.address

    session_token = packet_result.get_session_token()
    session = context.session_data[session_token]
    
    salted_password = packet_result.packet.data['hash_pass']

    entry = User(str(uuid.uuid4()), session.user.username, session.user.username, salted_password)
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

    del context.session_data[session_token]


def join_user_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    user_table = context.database_data.user_table

    address = packet_result.address

    username = packet_result.packet.data['username']
    password = packet_result.packet.data['password']

    if not user_table.verify_user(username, password):
        data = {
            'code': RESULT_FAILED,
            'reason': 'invalid credentials'
        }
        return server_socket.send(Packet(PacketType.JOIN_USER, data), address)

    user_entry = user_table.fetch_user(username)

    # session:
    session_token = create_session_token()
    context.session_data[session_token] = SessionData()

    session = context.session_data[session_token]
    session.authenticated = True

    session.user.uid = user_entry.uid
    session.user.username = user_entry.username
    session.user.display_name = user_entry.display_name
    
    data = {
        'code': RESULT_PASSED,
        'session_token': session_token,
        'username': session.user.username,
        'display_name': session.user.display_name
    }
    server_socket.send(Packet(PacketType.JOIN_USER, data), address)


def unauthenticated_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    
    data = {
        'code': RESULT_FAILED,
        'reason': 'user not authenticated'
    }
    return server_socket.send(Packet(PacketType.NOT_AUTH, data), packet_result.address)


def leave_user_callback(context: ServerContext, packet_result: RecvPacket):
    session_token = packet_result.get_session_token()
    
    if not context.session_data.get(session_token):
        return

    del context.session_data[session_token]
