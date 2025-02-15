from mineme_core.network.packet import *
from typing import Callable


class PacketHandler:
    def __init__(self):
        self.packet_map: dict[PacketType, Callable] = {}
    
    def execute_packet(self, packet_result: RecvPacket):
        if not packet_result.valid:
            return

        packet_map_result = self.packet_map.get(packet_result.packet.type)
        if not packet_map_result:
            return
        
        packet_map_result(packet_result)

    def register(self, packet_type: PacketType, function: Callable):
        self.packet_map[packet_type] = function
    
    