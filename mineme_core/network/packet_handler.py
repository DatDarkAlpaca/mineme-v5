from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType
from typing import Callable


class PacketHandler:
    def __init__(self):
        self.packet_map: dict[PacketType, Callable] = {}
        self.on_execute_callbacks: list[Callable] = []

    def register_on_execute(self, callback: Callable):
        self.on_execute_callbacks.append(callback)

    def execute_packet(self, client_socket: MineSocket, packet_result: Packet):
        if not packet_result.is_valid():
            return

        for on_execute in self.on_execute_callbacks:
            if not on_execute(client_socket, packet_result):
                return

        packet_map_result = self.packet_map.get(packet_result.type)
        if not packet_map_result:
            return

        packet_map_result(client_socket, packet_result)

    def register(self, packet_type: PacketType, function: Callable):
        self.packet_map[packet_type] = function
