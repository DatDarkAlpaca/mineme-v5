from mineme_core.constants import *
from mineme_core.network.network import *
from mineme_core.utils.string import get_number_with_separator


def cmd_check_balance(client_socket: MineSocket):
    client_socket.send(Packet(PacketType.CHECK_BALANCE))

    packet_result = client_socket.receive()

    if not packet_result.valid:
        return print(packet_result.get_reason())
        
    balance = float(packet_result.packet.data['balance'])
    print(f"You currently have: {CURRENCY_SYMBOL}{get_number_with_separator(balance)}")
