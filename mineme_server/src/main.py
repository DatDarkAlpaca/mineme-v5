import os
from threading import Thread

from mineme_core.network.network import *
from mineme_core.database.user_database import *
from mineme_core.utils.environment import initialize_environment
from mineme_core.database.database import create_database_connection

from user import *
from authentication import *


def initialize_database():
    connection = create_database_connection()
    cursor = connection.cursor()

    initialize_user_table(cursor=cursor)
    return connection, cursor


def run():
    connection, cursor = initialize_database()
    server_socket = initialize_server_socket(host=os.environ.get('SERVER_ADDRESS'), port=int(os.environ.get('SERVER_PORT')))
    clients: dict[User] = {}

    while True:
        packet, address = server_socket.receive_packet()
                
        if packet.type == PacketType.REGISTER_USER:
            handle_user_registration_username(cursor, server_socket, packet, address, clients)
    
        elif packet.type == PacketType.REGISTER_PASSWORD:
            handle_user_registration_password(cursor, server_socket, packet, address, clients[address])

        elif packet.type == PacketType.JOIN_USER:
            handle_user_join(cursor, server_socket, packet, address, clients)


def main():
    initialize_environment('./mineme_server/.env')
    
    thread = Thread(target=run, daemon=True)
    thread.start()

    host = os.environ.get('SERVER_ADDRESS')
    port = int(os.environ.get('SERVER_PORT'))
    input(f"Initialized server at {host}:{port}. Press any key to shutdown...")


if __name__ == '__main__':
    main()
