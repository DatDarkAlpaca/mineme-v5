from context import ServerContext

from mineme_core.network.packet import Packet
from mineme_core.network.mine_socket import MineSocket


def leave_callback(context: ServerContext, client_socket: MineSocket, packet_result: Packet):
    session_token = packet_result.get_session_token()

    if not context.session_handler.get(session_token):
        return

    del context.session_handler[session_token]
    client_socket.close()
