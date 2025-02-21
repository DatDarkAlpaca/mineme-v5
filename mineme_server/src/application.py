from threading import Thread
from datetime import timedelta, datetime

from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from context import ServerContext

from callbacks import (
    register_callback,
    join_callback,
    leave_callback,
    balance_callback,
    gamble_callback,
    mine_callback,
    ore_callback,
    pay_callback,
    notifications_callback
)
from utils.packet_utils import (
    send_invalid_session_packet,
    send_delayed_command_packet
)


class ServerApp:
    def __init__(self):
        self.context = ServerContext()
        self.initialize()

    def initialize(self):
        self.initialize_packet_handler()

        thread = Thread(target=lambda: self.context.server_socket.execute(), daemon=True)
        thread.start()
    
    def run(self):
        print(f"Initialized server at {self.context.server_socket.host}:{self.context.server_socket.port}.")
        while True:
            command = input("> ").lower()

            if command in ["quit", "exit", "q", "e"]:
                return
            
            if command.startswith('kick'):
                session_token = command.split(' ')[1]

                session = self.context.session_handler.get(session_token)
                if not session:
                    continue
                
                self.context.session_handler.remove(session_token)

            elif command.startswith('notify'):
                session_token = command.split(' ')[1]
                message = ''.join(command.split(' ')[2:])
            
                if session_token == '*':
                    for _, session in self.context.session_handler.items():
                        session.notification_queue.append(message)
                    continue

                session = self.context.session_handler.get(session_token)
                if not session:
                    continue
                
                session.notification_queue.append(message)
            
            elif command.startswith("list"):
                print("Session list:")
                for session_token, session in self.context.session_handler.items():
                    uid = session.user.uid
                    username = session.user.username
                    display = session.user.display_name

                    print(f"* [[{session_token}]: {username} ({display}) [{uid}]")

    def initialize_packet_handler(self):
        packet_handler = self.context.packet_handler
        
        packet_handler.register(
            PacketType.POLL_NOTIFICATION,
            lambda client_socket, packet_result: notifications_callback(self.context, client_socket, packet_result),
        )
        packet_handler.register_on_execute(
            lambda client_socket, packet_result: self.__handle_command_cooldown(client_socket, packet_result)
        )

        # Authentication:
        packet_handler.register(
            PacketType.REGISTER_USER,
            lambda client_socket, packet_result: register_callback(self.context, client_socket, packet_result),
        )
        packet_handler.register(
            PacketType.JOIN_USER,
            lambda client_socket, packet_result: join_callback(self.context, client_socket, packet_result),
        )
        packet_handler.register(
            PacketType.LEAVE_USER,
            lambda client_socket, packet_result: leave_callback(self.context, client_socket, packet_result),
        )

        # Game:
        packet_handler.register(
            PacketType.CHECK_BALANCE,
            lambda client_socket, packet_result: balance_callback(self.context, client_socket, packet_result),
        )
        packet_handler.register(
            PacketType.MINE, lambda client_socket, packet_result: mine_callback(self.context, client_socket, packet_result)
        )
        packet_handler.register(
            PacketType.GAMBLE, lambda client_socket, packet_result: gamble_callback(self.context, client_socket, packet_result)
        )
        packet_handler.register(
            PacketType.ORE,
            lambda client_socket, packet_result: ore_callback(self.context, client_socket, packet_result),
        )
        packet_handler.register(
            PacketType.PAY, lambda client_socket, packet_result: pay_callback(self.context, client_socket, packet_result)
        )

    def __handle_command_cooldown(self, client_socket: MineSocket, packet_result: Packet) -> bool:
        type = packet_result.type

        if type in [
            PacketType.REGISTER_USER,
            PacketType.JOIN_USER,
            PacketType.LEAVE_USER,
            PacketType.POLL_NOTIFICATION,
        ]:
            return True

        session_token = packet_result.get_session_token()
        session = self.context.session_handler.get(session_token)
        if not session_token or not session:
            send_invalid_session_packet(client_socket)
            return False

        last_executed = session.command_cooldowns.get_cooldown(type)

        now = datetime.now()
        time_passed = now - last_executed
        cooldown_time = timedelta(seconds=self.context.cooldown_table.get_delay(type))

        if time_passed < cooldown_time:
            remaining = cooldown_time.total_seconds() - time_passed.total_seconds()
            send_delayed_command_packet(client_socket, remaining)
            return False

        session.command_cooldowns.use_command(type)
        return True
