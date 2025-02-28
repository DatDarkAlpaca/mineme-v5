from context import ClientContext
from mineme_core.localization import _tr
from mineme_core.commands import Command
from mineme_core.constants import CURRENCY_SYMBOL
from mineme_core.network.packet import Packet, PacketType


def cmd_pay(context: ClientContext):
    args = context.console.arguments
    client_socket = context.client_socket

    if not client_socket.connected:
        client_socket.connect()
        return print("Attempting to reconnect to server. Please try again.")

    if len(args) < 2:
        return print("Usage: pay <username> <amount>")

    try:
        username = args[0].lower()
        amount = float(args[1].lower())
    except Exception:
        return print("Usage: pay <username> <amount>")

    data = {
        "session_token": context.session_token,
        "username": username,
        "amount": amount,
    }

    if not client_socket.send(Packet(PacketType.PAY, data)):
        return print("Connection timed out. Please try again later")

    packet_result = client_socket.receive()
    if not packet_result.is_valid():
        return print(f"Usage: pay <username> <amount> | {packet_result.get_reason()}")

    print(
        _tr("You have transferred {0}{1:.2f} to {2}", CURRENCY_SYMBOL, amount, username)
    )


pay_command = Command(
    "pay",
    "pays a certain amount of money to an user",
    "pay <username> <amount>",
    ["give"],
    cmd_pay
)
