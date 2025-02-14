from mineme_core.network.network import MineSocket
from mineme_core.network.packet import *


def view_join_user(args: list[str], client_socket: MineSocket, view_handler):
    if len(args) < 2:
        return print('Usage: join <username> <password>')
        
    username = args[0]
    password = args[1]

    # username:
    client_socket.send_packet_default(packet_type=PacketType.JOIN_USER, data=f"{username},{password}")

    packet, _ = client_socket.receive_packet()
    response_code, data = packet.data.split(',', 1)

    if response_code == '1':
        return print('Usage: join <username> <password> | invalid credentials')
    
    view_handler.set_view('game')


def view_leave_user(client_socket: MineSocket, view_handler):
    client_socket.send_packet_default(packet_type=PacketType.LEAVE_USER, data='')
    view_handler.set_view('welcome')
