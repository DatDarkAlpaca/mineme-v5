from termcolor import colored
from context import ClientContext
from mineme_core.commands import Command
from mineme_core.constants import CURRENCY_SYMBOL
from mineme_core.network.packet import Packet, PacketType


def cmd_gamble(context: ClientContext):
    args: list = context.console.arguments
    client_socket = context.client_socket

    if not client_socket.connected:
        client_socket.connect()
        return print("Attempting to reconnect to server. Please try again.")

    if len(args) == 0:
        return print("usage: gamble <amount> <multiplier=2.0>")

    amount = args[0]
    multiplier = 2.0

    if len(args) >= 2:
        try:
            multiplier = float(args[1])
        except Exception:
            return print("usage: gamble <amount> <multiplier=2.0>")

    data = {
        "amount": amount,
        "multiplier": multiplier,
        "session_token": context.session_token,
    }
    if not client_socket.send(Packet(PacketType.GAMBLE, data)):
        return print("Connection timed out. Please try again later")

    packet_result = client_socket.receive()
    if not packet_result.is_valid():
        return print(
            f"usage: gamble <amount> <multiplier> | {packet_result.get_reason()}"
        )

    win = packet_result.data["win"]

    if win == 1:
        return print(
            colored("You won! ", "light_yellow")
            + f"You have received {CURRENCY_SYMBOL}{float(amount) * float(multiplier)}"
        )
    else:
        return print(
            colored("Oh no!", "red")
            + f" You lost... You have lost {CURRENCY_SYMBOL}{float(amount)}"
        )

gamble_command = Command(
    "gamble",
    "gambles a portion of your money",
    "gamble <amount> <multiplier: 1.5>",
    [],
    cmd_gamble
)
