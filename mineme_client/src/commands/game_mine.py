from mineme_core.constants import CURRENCY_SYMBOL, SIZE_MODIFIERS
from mineme_core.network.network import *
from context import ClientContext

from termcolor import colored

def get_size_modifier(weight: float, min_weight: float, max_weight: float):
    modifiers_amount = len(SIZE_MODIFIERS)

    weight_sum = min_weight + max_weight
    portion = weight_sum / (modifiers_amount + 1)

    for i in range(0, modifiers_amount):
        if weight >= min_weight + portion * i and weight < min_weight + portion * (i + 1):
            return SIZE_MODIFIERS[i]

    return ''


def cmd_mine(context: ClientContext):
    client_socket = context.client_socket

    data = {
        'session_token': context.session_token
    }
    client_socket.send(Packet(PacketType.MINE, data))

    packet_result = client_socket.receive()
    if not packet_result.valid:
        return print(f"Usage: mine | {packet_result.get_reason()}")

    ore_name = packet_result.packet.data['ore_name']
    weight = packet_result.packet.data['weight']
    price = packet_result.packet.data['price']
    min_weight = packet_result.packet.data['min_weight']
    max_weight = packet_result.packet.data['max_weight']

    size_modifier = colored(get_size_modifier(weight, min_weight, max_weight), 'red')
    print(f"You struck {size_modifier}{ore_name}! It weighs {weight:.2f}kg, and it's worth {CURRENCY_SYMBOL}{price:.2f}!")
