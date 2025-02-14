import bcrypt

from mineme_core.network.network import MineSocket
from mineme_core.network.packet import *


def view_register_user(args: list[str], client_socket: MineSocket):
    if len(args) < 2:
        return print('Usage: register <username> <password>')
        
    username = args[0]
    password = args[1]

    # username:
    client_socket.send_packet_default(packet_type=PacketType.REGISTER_USER, data=username)

    packet, _ = client_socket.receive_packet()
    response_code, response = packet.data.split(',', 1)

    if response_code == '1':
        if response == 'short':
            return print('Usage: register <username> <password> | username must be at least 3x characters long')
        
        elif response == 'taken':
            return print(f"Usage: register <username> <password> | username '{username}' has already been taken")

    # password:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt=response.encode('utf-8')).decode()
    client_socket.send_packet_default(packet_type=PacketType.REGISTER_PASSWORD, data=hashed_password)

    packet, _ = client_socket.receive_packet()
    response_code, response = packet.data.split(',', 1)

    if response_code == '1':
        return print(f"Usage: register <username> <password> | could not register username {username}. please contact the admins")
    
    return print(f"Successfully registered user: {username}. Use the command 'join <username> <password>' to join")
