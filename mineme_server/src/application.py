import os
from datetime import timedelta
from threading import Thread, Lock

from mineme_core.constants import * 
from mineme_core.network.network import *
from mineme_core.network.packet_handler import *
from mineme_core.database.database import create_database_connection

from mineme_server.src.session_data import *
from database_data import *
from callbacks.game import *
from callbacks.authentication import *
from mineme_server.src.application_context import ServerContext


class ServerApp:
    def __init__(self, server_address: str, server_port: int):
        self.context = ServerContext()
        
        self.context.server_socket = initialize_server_socket(server_address, server_port)
        self.server_lock = Lock()

        self.__initialize_tables()
        self.__initialize_server_data()

    def run(self):
        thread = Thread(target=lambda: self.__execute_server(), daemon=True)
        thread.start()

        thread = Thread(target=lambda: self.__cleanup_timeout_sessions(), daemon=True)
        thread.start()

        host = os.environ.get('SERVER_ADDRESS')
        port = int(os.environ.get('SERVER_PORT'))
        input(f"Initialized server at {host}:{port}. Press any key to shutdown...")

    def _user_authenticated(self, packet_result: RecvPacket) -> bool:
        session_token = packet_result.get_session_token()
        return self.context.session_data.get(session_token) and self.context.session_data[session_token].authenticated

    def __execute_server(self):
        while True:
            with self.server_lock:
                packet_result = self.context.server_socket.receive()
                self.context.packet_handler.execute_packet(packet_result)

    def __cleanup_timeout_sessions(self):
        while True:
            now = datetime.now()

            with self.server_lock:
                
                expired_tokens = []
                for session_token, session_data in self.context.session_data.items():
                    timed_out = now - session_data.last_activity > timedelta(minutes=SESSION_TIMEOUT)
                    if not timed_out:
                        continue

                    expired_tokens.append(session_token)

                for session_token in expired_tokens:
                    del self.context.session_data[session_token]
                        
    def __initialize_server_data(self):
        # Authentication:
        packet_handler = self.context.packet_handler

        packet_handler.register(PacketType.REGISTER_USER, lambda packet_result: 
            register_user_callback(self.context, packet_result)
        )

        packet_handler.register(PacketType.REGISTER_PASSWORD, lambda packet_result: 
            register_password_callback(self.context, packet_result)
        )

        packet_handler.register(PacketType.JOIN_USER, lambda packet_result: 
            join_user_callback(self.context, packet_result)
        )

        packet_handler.register(PacketType.LEAVE_USER, lambda packet_result: 
            leave_user_callback(self.context, packet_result)
        )

        # Game:
        packet_handler.register(PacketType.CHECK_BALANCE, lambda packet_result: self.__check_balance(packet_result))  
        packet_handler.register(PacketType.MINE, lambda packet_result: self.__mine(packet_result))

    def __initialize_tables(self):
        database_data = self.context.database_data

        self.context.db_connection = create_database_connection()
        self.context.db_cursor = self.context.db_connection.cursor()
        cursor = self.context.db_cursor

        database_data.user_table = UserTable(cursor)
        database_data.player_table = PlayerTable(cursor)

        ore_table = OreTable(cursor)
        ore_categories = OreCategoryTable(cursor)

        database_data.ores = ore_table.get_all_ores()
        database_data.ore_categories = ore_categories.get_all_ore_categories()

    def __check_balance(self, packet_result: RecvPacket):
        if not self._user_authenticated(packet_result):
            unauthenticated_callback(self.context, packet_result)

        check_balance_callback(self.context, packet_result)
    
    def __mine(self, packet_result: RecvPacket):
        if not self._user_authenticated(packet_result):
            unauthenticated_callback(self.context, packet_result)

        mine_callback(self.context, packet_result)
