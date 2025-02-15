from mineme_core.constants import CURRENCY_SYMBOL
from mineme_core.network.network import *


def cmd_mine(client_socket: MineSocket):
    client_socket.send(Packet(PacketType.MINE))

    packet_result = client_socket.receive()
    if not packet_result.valid:
        return print(f"Usage: mine | {packet_result.get_reason()}")

    ore_name = packet_result.packet.data['ore_name']
    weight = packet_result.packet.data['weight']
    price = packet_result.packet.data['price']

    print(f"You struck {ore_name}! It weighs {weight:.2f}kg, and it's worth {CURRENCY_SYMBOL}{price:.2f}!")
