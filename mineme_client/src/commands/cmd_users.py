from mineme_core.commands import Command
from mineme_core.network.packet import Packet, PacketType

from context import ClientContext


def cmd_users(context: ClientContext):
    client_socket = context.client_socket

    if not client_socket.connected:
        client_socket.connect()
        return print("Attempting to reconnect to server. Please try again.")
    
    data = {
        "session_token": context.session_token
    }
    if not client_socket.send(Packet(PacketType.USERS, data)):
        return print("A connection error has occurred. Please try again later")

    packet_result = client_socket.receive()
    if not packet_result.is_valid():
        return print(
            f"Usage: users | {packet_result.get_reason()}"
        )
    
    users = packet_result.data["users"]

    print("Connected users:")
    print(f"* {context.username} [you]")
    for user in users:
        print(f"* {user}")


users_command = Command(
    "users",
    "shows a list of the connected users",
    "users",
    None,
    cmd_users
)
