from context import ServerContext
from mineme_core.network.packet import RecvPacket


def leave_callback(context: ServerContext, packet_result: RecvPacket):
    session_token = packet_result.get_session_token()

    if not context.session_data.get(session_token):
        return

    del context.session_data[session_token]
