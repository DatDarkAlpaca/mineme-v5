from mineme_core.network.network import *


def send_invalid_session_packet(server_socket: MineSocket, address):
    data = {
        'code': RESULT_FAILED,
        'reason': 'session not initialized'
    }

    server_socket.send(Packet(PacketType.CHECK_BALANCE, data), address)
