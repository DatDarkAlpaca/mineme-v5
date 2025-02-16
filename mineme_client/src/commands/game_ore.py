from context import ClientContext
from mineme_core.localization import _tr
from mineme_core.network.network import *


def cmd_ore(context: ClientContext):
    args = context.console.arguments
    client_socket = context.client_socket
    
    if len(args) < 1:
        return print(f"Usage: ore <ore_name>")

    ore_name = args[0].lower()

    data = {
        'session_token': context.session_token,
        'ore_name': ore_name
    }
    client_socket.send(Packet(PacketType.ORE, data))

    packet_result = client_socket.receive()
    if not packet_result.valid:
        return print(f"Usage: ore <ore_name> | {packet_result.get_reason()}")
    
    data = packet_result.packet.data
    ore_name = data['ore_name']
    category = data['category']
    price = data['price']
    min_weight = data['min_weight']
    max_weight = data['max_weight']
    
    information = f"{ore_name} information:\n * category: {category}\n * price: W${price}\n * minimum weight: {min_weight}kg\n * maximum weight: {max_weight}kg"
    print(information)