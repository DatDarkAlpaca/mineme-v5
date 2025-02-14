import os
from threading import Thread

from mineme_core.network.network import *
from mineme_core.database.user_table import *
from mineme_core.database.player_table import *
from mineme_core.utils.environment import initialize_environment
from mineme_core.database.database import create_database_connection

from user import *
from authentication import *


def initialize_database():
    connection = create_database_connection()
    cursor = connection.cursor()

    user_table = UserTable(cursor)
    player_table = PlayerTable(cursor)

    return user_table, player_table


def run():
    user_table, player_table = initialize_database()

    server_socket = initialize_server_socket(host=os.environ.get('SERVER_ADDRESS'), port=int(os.environ.get('SERVER_PORT')))
    clients: dict[User] = {}

    while True:
        packet, address = server_socket.receive_packet()
                
        if packet.type == PacketType.REGISTER_USER:
            handle_user_registration_username(user_table, server_socket, packet, address, clients)
    
        elif packet.type == PacketType.REGISTER_PASSWORD:
            handle_user_registration_password(user_table, server_socket, packet, address, clients[address])

        elif packet.type == PacketType.JOIN_USER:
            handle_user_join(user_table, server_socket, packet, address, clients)

        # Authenticated only packets:
        else:
            if not clients.get(address) or not clients[address].authenticated:
                return handle_user_not_authenticated(server_socket, address)


def main():
    initialize_environment('./mineme_server/.env')
    
    thread = Thread(target=run, daemon=True)
    thread.start()

    host = os.environ.get('SERVER_ADDRESS')
    port = int(os.environ.get('SERVER_PORT'))
    input(f"Initialized server at {host}:{port}. Press any key to shutdown...")


if __name__ == '__main__':
    main()
