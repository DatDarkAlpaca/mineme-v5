from context import ClientContext

from mineme_core.localization import _tr
from mineme_core.constants import CURRENCY_SYMBOL
from mineme_core.network.packet import Packet, PacketType
from mineme_core.utils.string import get_number_with_separator


def cmd_balance(context: ClientContext):
    client_socket = context.client_socket

    if not client_socket.connected:
        client_socket.connect()
        return print("Attempting to reconnect to server. Please try again.")

    data = {"session_token": context.session_token}
    if not client_socket.send(Packet(PacketType.CHECK_BALANCE, data)):
        return print("Connection timed out. Please try again later")

    packet_result = client_socket.receive()

    if not packet_result.is_valid():
        return print(f"usage: balance | {packet_result.get_reason()}")

    balance = packet_result.data["balance"]

    print(
        _tr(
            "You currently have {0}{1}",
            CURRENCY_SYMBOL,
            get_number_with_separator(float(balance)),
        )
    )
