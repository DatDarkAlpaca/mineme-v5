from mineme_core.network.network import MineSocket
from mineme_core.network.packet import *

from context import ClientContext


def cmd_join(context: ClientContext):
    args = context.console.arguments
    client_socket = context.client_socket
    view_handler = context.view_handler
    
    if len(args) < 2:
        return print('Usage: join <username> <password>')
        
    username = args[0]
    password = args[1]

    # username:
    data = {
        'username': username,
        'password': password
    }

    client_socket.send(Packet(PacketType.JOIN_USER, data))
    packet_result = client_socket.receive()

    if not packet_result.valid:
        return print(f"Usage: join <usaname> <paswword> | {packet_result.get_reason()}")

    username = packet_result.packet.data['username']
    display_name = packet_result.packet.data['display_name']
    session_token = packet_result.get_session_token()

    view_handler.get_view('game').set_user(username, display_name, session_token)
    view_handler.set_view('game')


def cmd_leave(context: ClientContext):
    client_socket = context.client_socket
    view_handler = context.view_handler
    
    data = {
        'session_token': context.session_token
    }

    client_socket.send(Packet(PacketType.LEAVE_USER, data))
    view_handler.set_view('welcome')
