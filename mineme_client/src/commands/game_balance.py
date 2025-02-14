from mineme_core.constants import *
from mineme_core.utils.string import get_number_with_separator
from mineme_core.network.network import MineSocket, PacketType


def view_balance(client_socket: MineSocket):
    client_socket.send_packet_default(PacketType.CHECK_BALANCE)

    packet, _ = client_socket.receive_packet()
    balance = float(packet.data)

    print(f"You currently have: {CURRENCY_SYMBOL}{get_number_with_separator(balance)}")
