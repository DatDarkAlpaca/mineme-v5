from mineme_core.network.network import MineSocket
from mineme_core.network.packet import *


def view_join_user(args: list[str], client_socket: MineSocket, view_handler):
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

    view_handler.get_view('game').set_user(username, display_name)
    view_handler.set_view('game')


def view_leave_user(client_socket: MineSocket, view_handler):
    client_socket.send(Packet(PacketType.LEAVE_USER))
    view_handler.set_view('welcome')
