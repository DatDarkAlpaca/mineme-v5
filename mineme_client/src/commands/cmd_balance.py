from context import ClientContext

from mineme_core.constants import *
from mineme_core.localization import _tr
from mineme_core.network.packet import Packet, PacketType
from mineme_core.utils.string import get_number_with_separator


def cmd_check_balance(context: ClientContext):
    client_socket = context.client_socket

    data = {"session_token": context.session_token}
    client_socket.send(Packet(PacketType.CHECK_BALANCE, data))
    packet_result = client_socket.receive()

    if not packet_result.is_valid():
        return print(f"usage: balance | {packet_result.get_reason()}")

    balance = packet_result.packet.data["balance"]

    print(
        _tr(
            "You currently have {0}{1}",
            CURRENCY_SYMBOL,
            get_number_with_separator(float(balance)),
        )
    )
