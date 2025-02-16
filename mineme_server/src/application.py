import os
import time
from threading import Thread, Lock
from datetime import timedelta, datetime

from mineme_core.constants import * 
from mineme_server.src.application_context import ServerContext

from callbacks.game import *
from callbacks.authentication import *


class ServerApp:
    def __init__(self, server_address: str, server_port: int):
        self.context = ServerContext()
        self.context.initialize(server_address, server_port)
                
        self.server_lock = Lock()

        self.__initialize_server_data()

    def run(self):
        thread = Thread(target=lambda: self.__execute_server(), daemon=True)
        thread.start()

        thread = Thread(target=lambda: self.__cleanup_timeout_sessions(), daemon=True)
        thread.start()

        host = os.environ.get('SERVER_ADDRESS')
        port = int(os.environ.get('SERVER_PORT'))
        
        print(f"Initialized server at {host}:{port}.")
        while True:
            command = input('> ').lower()

            if command in ['quit', 'exit', 'q', 'e']:
                return
            
            elif command == 'list':
                print('Session list:')
                for session_token, session_data in self.context.session_data.items():
                    uid = session_data.user.uid
                    username = session_data.user.username
                    display = session_data.user.display_name

                    print(f"* [{session_token}]: {username} ({display}) [{uid}]")
        
    def _user_authenticated(self, packet_result: RecvPacket) -> bool:
        session_token = packet_result.get_session_token()
        return self.context.session_data.get(session_token) and self.context.session_data[session_token].authenticated

    def __execute_server(self):
        while True:
            packet_result = self.context.server_socket.receive()
            with self.server_lock:
                self.context.packet_handler.execute_packet(packet_result)

    def __cleanup_timeout_sessions(self):
        while True:
            now = datetime.now()

            with self.server_lock:
                expired_tokens = []
                for session_token, session_data in self.context.session_data.items():
                    last_active = session_data.last_activity
                    idle_duration = now - last_active
                    
                    timed_out = idle_duration > timedelta(minutes=float(os.environ.get('SESSION_TIMEOUT')))
                    if not timed_out:
                        continue

                    expired_tokens.append(session_token)

                for session_token in expired_tokens:
                    del self.context.session_data[session_token]
        
            time.sleep(1.0)

    def __initialize_server_data(self):
        # Authentication:
        packet_handler = self.context.packet_handler
        packet_handler.register_on_execute(lambda packet_result: self.__handle_command_cooldown(packet_result))

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
        packet_handler.register(PacketType.GAMBLE, lambda packet_result: self.__gamble(packet_result))
        packet_handler.register(PacketType.ORE, lambda packet_result: ore_callback(self.context, packet_result))
        packet_handler.register(PacketType.PAY, lambda packet_result: self.__pay(packet_result)) 

    def __handle_command_cooldown(self, packet_result: RecvPacket) -> bool:
        type = packet_result.packet.type

        if type in [PacketType.REGISTER_USER, PacketType.REGISTER_PASSWORD, PacketType.JOIN_USER, PacketType.LEAVE_USER]:
            return True

        session_token = packet_result.get_session_token()
        session = self.context.session_data.get(session_token)
        if not session_token or not session:
            send_invalid_session_packet(self.context.server_socket, packet_result.address)
            return False
        
        last_executed = session.command_cooldowns.get_cooldown(type)
        
        now = datetime.now()
        time_passed = now - last_executed
        cooldown_time = timedelta(seconds=self.context.cooldown_table.get_delay(type))

        if time_passed < cooldown_time:
            remaining = cooldown_time.total_seconds() - time_passed.total_seconds()
            send_delayed_command_packet(self.context.server_socket, remaining, packet_result.address)
            return False

        session.command_cooldowns.use_command(type)
        session.last_activity = now
        return True
            
    def __check_balance(self, packet_result: RecvPacket):
        if not self._user_authenticated(packet_result):
            return unauthenticated_callback(self.context, packet_result)

        check_balance_callback(self.context, packet_result)
    
    def __mine(self, packet_result: RecvPacket):
        if not self._user_authenticated(packet_result):
            return unauthenticated_callback(self.context, packet_result)

        mine_callback(self.context, packet_result)

    def __gamble(self, packet_result: RecvPacket):
        if not self._user_authenticated(packet_result):
            return unauthenticated_callback(self.context, packet_result)

        gamble_callback(self.context, packet_result)

    def __pay(self, packet_result: RecvPacket):
        if not self._user_authenticated(packet_result):
            return unauthenticated_callback(self.context, packet_result)

        pay_callback(self.context, packet_result)
