from server_socket import ServerSocket
from mineme_core.network.packet import Packet, PacketType


def send_invalid_session_packet(server_socket: ServerSocket, address):
    data = {"reason": "invalid session | you were timed out | please log in again"}
    server_socket.send(Packet(PacketType.INVALID, data), address)


def send_delayed_command_packet(server_socket: ServerSocket, delay: float, address):
    data = {"reason": f"you must wait {delay:.2f}s to use this command again"}

    server_socket.send(Packet(PacketType.INVALID, data), address)


def send_unauthenticated_packet(server_socket: ServerSocket, address):
    data = {"reason": "user not authenticated"}
    return server_socket.send(Packet(PacketType.INVALID, data), address)
