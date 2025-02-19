from mineme_core.network.packet import Packet, PacketType, RecvPacket
from context import ServerContext


def ore_callback(context: ServerContext, packet_result: RecvPacket):
    server_socket = context.server_socket
    ores = context.database_data.ores
    categories = context.database_data.ore_categories

    address = packet_result.address

    ore_name = packet_result.packet.data.get("ore_name")
    if not ore_name:
        data = {"reason": "invalid ore name"}
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    try:
        for ore_data in ores:
            if ore_name == ore_data.name:
                ore = ore_data

        for category_data in categories:
            if ore.category_id == category_data.id:
                category_name = category_data.name

    except Exception:
        data = {"reason": "invalid ore name"}
        return server_socket.send(Packet(PacketType.INVALID, data), address)

    data = {
        "ore_name": ore.name,
        "category": category_name,
        "price": ore.price,
        "min_weight": ore.min_weight,
        "max_weight": ore.max_weight,
    }

    return server_socket.send(Packet(PacketType.ORE, data), address)
