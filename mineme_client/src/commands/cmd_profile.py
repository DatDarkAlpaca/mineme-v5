from mineme_core.commands import Command
from mineme_core.constants import CURRENCY_SYMBOL
from mineme_core.network.packet import Packet, PacketType

from context import ClientContext


def cmd_profile(context: ClientContext):
    client_socket = context.client_socket
    arguments = context.console.arguments

    if not client_socket.connected:
        client_socket.connect()
        return print("Attempting to reconnect to server. Please try again.")
    
    if not len(arguments) > 0:
        return print("Usage: profile <username>")

    data = {
        "session_token": context.session_token,
        "username": arguments[0]
    }
    if not client_socket.send(Packet(PacketType.PROFILE, data)):
        return print("A connection error has occurred. Please try again later")

    packet_result = client_socket.receive()
    if not packet_result.is_valid():
        return print(
            f"Usage: profile <username> | {packet_result.get_reason()}"
        )
    
    username = packet_result.data["username"]
    display_name = packet_result.data["display_name"]
    balance = packet_result.data["balance"]

    print(f"{username}'s profile")
    print(f"  display name: {display_name}")
    print(f"  balance: {CURRENCY_SYMBOL}{float(balance):.2f}")


profile_command = Command(
    "profile",
    "displays the <username>'s user profile",
    "profile <username>",
    None,
    cmd_profile
)
