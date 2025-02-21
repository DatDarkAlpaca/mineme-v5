from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from session_data import SessionHandler


def is_user_authenticated(session_handler: SessionHandler, packet_result: Packet) -> bool:
    session_token = packet_result.get_session_token()
    return session_handler.get(session_token) and session_handler.get(session_token).authenticated
    

def send_invalid_session_packet(client_socket: MineSocket):
    data = {"reason": "invalid session | you were timed out | please log in again"}
    client_socket.send(Packet(PacketType.INVALID, data))


def send_delayed_command_packet(client_socket: MineSocket, delay: float):
    data = {"reason": f"you must wait {delay:.2f}s to use this command again"}
    client_socket.send(Packet(PacketType.INVALID, data))


def send_unauthenticated_packet(client_socket: MineSocket):
    data = {"reason": "user not authenticated"}
    return client_socket.send(Packet(PacketType.INVALID, data))
