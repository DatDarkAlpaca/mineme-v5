import os
from threading import Thread

from mineme_core.network.network import *
from mineme_core.network.packet_handler import *
from mineme_core.database.database import create_database_connection

from client_data import *
from database_data import *
from callbacks.game import *
from callbacks.authentication import *
from application_data import ServerAppData


class ServerApp:
    def __init__(self, server_address: str, server_port: int):
        self.data = ServerAppData()
        self.data.server_socket = initialize_server_socket(server_address, server_port)

        self.__initialize_tables()
        self.__initialize_server_data()

    def run(self):
        thread = Thread(target=lambda: self.__execute_server(), daemon=True)
        thread.start()

        host = os.environ.get('SERVER_ADDRESS')
        port = int(os.environ.get('SERVER_PORT'))
        input(f"Initialized server at {host}:{port}. Press any key to shutdown...")

    def _user_authenticated(self, address) -> bool:
        return self.data.client_data.get(address) and self.data.client_data[address].authenticated

    def __execute_server(self):
        while True:
            packet_result = self.data.server_socket.receive()
            self.data.packet_handler.execute_packet(packet_result)

    def __initialize_server_data(self):
        # Authentication:
        packet_handler = self.data.packet_handler

        packet_handler.register(PacketType.REGISTER_USER, lambda packet_result: 
            register_user_callback(self.data, packet_result)
        )

        packet_handler.register(PacketType.REGISTER_PASSWORD, lambda packet_result: 
            register_password_callback(self.data, packet_result)
        )

        packet_handler.register(PacketType.JOIN_USER, lambda packet_result: 
            join_user_callback(self.data, packet_result)
        )

        packet_handler.register(PacketType.LEAVE_USER, lambda packet_result: 
            leave_user_callback(self.data, packet_result)
        )

        # Game:
        packet_handler.register(PacketType.CHECK_BALANCE, lambda packet_result: self.__check_balance(packet_result))  
        packet_handler.register(PacketType.MINE, lambda packet_result: self.__mine(packet_result))

    def __initialize_tables(self):
        database_data = self.data.database_data

        self.data.db_connection = create_database_connection()
        self.data.db_cursor = self.data.db_connection.cursor()
        cursor = self.data.db_cursor

        database_data.user_table = UserTable(cursor)
        database_data.player_table = PlayerTable(cursor)

        ore_table = OreTable(cursor)
        ore_categories = OreCategoryTable(cursor)

        database_data.ores = ore_table.get_all_ores()
        database_data.ore_categories = ore_categories.get_all_ore_categories()

    def __check_balance(self, packet_result: RecvPacket):
        if not self._user_authenticated(packet_result.address):
            unauthenticated_callback(self, packet_result)

        check_balance_callback(self.data, packet_result)
    
    def __mine(self, packet_result: RecvPacket):
        if not self._user_authenticated(packet_result.address):
            unauthenticated_callback(self, packet_result)

        mine_callback(self.data, packet_result)
