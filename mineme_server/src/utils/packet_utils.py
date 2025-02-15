from mineme_core.network.network import *


def send_invalid_session_packet(server_socket: MineSocket, address):
    data = {
        'code': RESULT_FAILED,
        'reason': 'session not initialized'
    }

    server_socket.send(Packet(PacketType.INVALID, data), address)

def send_delayed_command_packet(server_socket: MineSocket, delay: float, address):
    data = {
        'code': RESULT_FAILED,
        'reason': f"you must wait {delay}s to use this command again"
    }

    server_socket.send(Packet(PacketType.INVALID, data), address)
