from context import ClientContext

from mineme_core.commands import Command
from mineme_core.network.packet import Packet, PacketType


def cmd_ore(context: ClientContext):
    args = context.console.arguments
    client_socket = context.client_socket

    if not client_socket.connected:
        client_socket.connect()
        return print("Attempting to reconnect to server. Please try again.")

    if len(args) < 1:
        return print("Usage: ore <ore_name>")

    ore_name = args[0].lower()

    data = {"session_token": context.session_token, "ore_name": ore_name}

    if not client_socket.send(Packet(PacketType.ORE, data)):
        return print("Connection timed out. Please try again later")

    packet_result = client_socket.receive()
    if not packet_result.is_valid():
        return print(f"Usage: ore <ore_name> | {packet_result.get_reason()}")

    data = packet_result.data
    ore_name = data["ore_name"]
    category = data["category"]
    price = data["price"]
    min_weight = data["min_weight"]
    max_weight = data["max_weight"]

    information = f"{ore_name} information:\n * category: {category}\n * price: W${price}\n * minimum weight: {min_weight}kg\n * maximum weight: {max_weight}kg"
    print(information)


ore_command = Command(
    "ore_info",
    "displays information about a specific ore",
    "ore_info",
    ["ore"],
    cmd_ore
)