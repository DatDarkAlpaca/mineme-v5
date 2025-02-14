import bcrypt

from mineme_core.network.network import MineSocket
from mineme_core.network.packet import *


def view_join_user(args: list[str], client_socket: MineSocket):
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
    
    print(response_code, data)
    print('Successfully logged in!')
