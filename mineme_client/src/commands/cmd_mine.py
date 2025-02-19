from context import ClientContext
from mineme_core.localization import _tr
from mineme_core.network.packet import Packet, PacketType
from mineme_core.constants import CURRENCY_SYMBOL, SIZE_MODIFIERS


def get_size_modifier(weight: float, min_weight: float, max_weight: float):
    modifiers_amount = len(SIZE_MODIFIERS)

    weight_sum = min_weight + max_weight
    portion = weight_sum / (modifiers_amount + 1)

    for i in range(0, modifiers_amount):
        if weight >= min_weight + portion * i and weight < min_weight + portion * (
            i + 1
        ):
            return SIZE_MODIFIERS[i]

    return ""


def cmd_mine(context: ClientContext):
    client_socket = context.client_socket

    data = {"session_token": context.session_token}
    client_socket.send(Packet(PacketType.MINE, data))

    packet_result = client_socket.receive()
    if not packet_result.is_valid():
        return print(f"Usage: mine | {packet_result.get_reason()}")

    data = packet_result.packet.data

    ore_name = data["ore_name"]
    weight = data["weight"]
    price = data["price"]
    min_weight = data["min_weight"]
    max_weight = data["max_weight"]

    size_modifier = get_size_modifier(weight, min_weight, max_weight)

    print(
        _tr(
            "You struck {0}{1}! It weighs {2:.2f}kg, and it's worth {3}{4:.2f}!",
            size_modifier,
            ore_name,
            weight,
            CURRENCY_SYMBOL,
            price,
        )
    )
