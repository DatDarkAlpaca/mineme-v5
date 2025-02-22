from mineme_core.commands import Command
from mineme_core.network.packet import Packet, PacketType

from context import ClientContext


def cmd_join(context: ClientContext):
    args = context.console.arguments
    client_socket = context.client_socket
    view_handler = context.view_handler

    if not client_socket.connected:
        client_socket.connect()
        return print("Attempting to reconnect to server. Please try again.")

    if len(args) < 2:
        return print("Usage: join <username> <password>")

    username = args[0]
    password = args[1]

    # username:
    data = {"username": username, "password": password}

    if not client_socket.send(Packet(PacketType.JOIN_USER, data)):
        return print("A connection error has occurred. Please try again later")

    packet_result = client_socket.receive()
    if not packet_result.is_valid():
        return print(
            f"Usage: join <username> <password> | {packet_result.get_reason()}"
        )

    username = packet_result.data["username"]
    display_name = packet_result.data["display_name"]
    session_token = packet_result.get_session_token()

    view_handler.get_view("game").set_user(username, display_name, session_token)
    view_handler.set_view("game")


join_command = Command(
    "join",
    "attempts to join the game",
    "join <username> <password>",
    [],
    cmd_join
)
