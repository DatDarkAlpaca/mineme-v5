from mineme_core.network.packet import Packet, PacketType
from mineme_core.localization import _tr

from context import ClientContext


def cmd_register(context: ClientContext):
    args = context.console.arguments
    client_socket = context.client_socket

    if not client_socket.connected:
        client_socket.connect()
        return print("Attempting to reconnect to server. Please try again.")

    if len(args) < 2:
        return print("Usage: register <username> <password>")

    username = args[0]
    password = args[1]

    # username:
    data = {"username": username, "password": password}

    if not client_socket.send(Packet(PacketType.REGISTER_USER, data)):
        return print("Connection timed out. Please try again later")

    packet_result = client_socket.receive()

    if not packet_result.is_valid():
        return print(
            f"Usage: register <username> <password> | {packet_result.get_reason()}"
        )

    print(
        _tr(
            "Successfully registered user: {}. Use the command 'join' to join", username
        )
    )
