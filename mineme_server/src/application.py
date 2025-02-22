from threading import Thread
from mineme_core.network.packet import PacketType

from callbacks import (
    register_callback,
    join_callback,
    leave_callback,
    balance_callback,
    gamble_callback,
    mine_callback,
    ore_callback,
    pay_callback,
    notifications_callback,
    users_callback,
    profile_callback
)
from context import ServerContext
from utils.cooldown import handle_command_cooldown


class ServerApp:
    def __init__(self):
        self.context = ServerContext()
        self.initialize()

    def initialize(self):
        self.initialize_packet_handler()
        self.initialize_cooldown_table()

        thread = Thread(
            target=lambda: self.context.server_socket.execute(), daemon=True
        )
        thread.start()

    def run(self):
        print(
            f"Initialized server at {self.context.server_socket.host}:{self.context.server_socket.port}."
        )
        while True:
            command = input("> ").lower()

            if command in ["quit", "exit", "q", "e"]:
                return

            if command.startswith("kick"):
                session_token = command.split(" ")[1]

                session = self.context.session_handler.get(session_token)
                if not session:
                    continue

                session.notification_queue.append("You have been kicked out. Please join in again")
                self.context.session_handler.remove(session_token)

            elif command.startswith("notify"):
                session_token = command.split(" ")[1]
                message = "".join(command.split(" ")[2:])

                if session_token == "*":
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
            lambda client_socket, packet_result: notifications_callback(
                self.context, client_socket, packet_result
            ),
        )
        packet_handler.register_on_execute(
            lambda client_socket, packet_result: handle_command_cooldown(
                self.context, client_socket, packet_result
            )
        )

        # Authentication:
        packet_handler.register(
            PacketType.REGISTER_USER,
            lambda client_socket, packet_result: register_callback(
                self.context, client_socket, packet_result
            ),
        )
        packet_handler.register(
            PacketType.JOIN_USER,
            lambda client_socket, packet_result: join_callback(
                self.context, client_socket, packet_result
            ),
        )
        packet_handler.register(
            PacketType.LEAVE_USER,
            lambda client_socket, packet_result: leave_callback(
                self.context, client_socket, packet_result
            ),
        )

        # Game:
        packet_handler.register(
            PacketType.CHECK_BALANCE,
            lambda client_socket, packet_result: balance_callback(
                self.context, client_socket, packet_result
            ),
        )
        packet_handler.register(
            PacketType.MINE,
            lambda client_socket, packet_result: mine_callback(
                self.context, client_socket, packet_result
            ),
        )
        packet_handler.register(
            PacketType.GAMBLE,
            lambda client_socket, packet_result: gamble_callback(
                self.context, client_socket, packet_result
            ),
        )
        packet_handler.register(
            PacketType.ORE,
            lambda client_socket, packet_result: ore_callback(
                self.context, client_socket, packet_result
            ),
        )
        packet_handler.register(
            PacketType.PAY,
            lambda client_socket, packet_result: pay_callback(
                self.context, client_socket, packet_result
            ),
        )
        
        # Session:
        packet_handler.register(
            PacketType.USERS,
            lambda client_socket, packet_result: users_callback(
                self.context, client_socket, packet_result
            ),
        )
        packet_handler.register(
            PacketType.PROFILE,
            lambda client_socket, packet_result: profile_callback(
                self.context, client_socket, packet_result
            ),
        )

    def initialize_cooldown_table(self):
        self.context.cooldown_table.set_delay(PacketType.MINE, 3)
        self.context.cooldown_table.set_delay(PacketType.GAMBLE, 10)