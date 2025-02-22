from datetime import datetime, timedelta

from mineme_core.network.mine_socket import MineSocket
from mineme_core.network.packet import Packet, PacketType

from context import ServerContext
from utils.packet_utils import send_invalid_session_packet, send_delayed_command_packet


def handle_command_cooldown(
        context: ServerContext, client_socket: MineSocket, packet_result: Packet
    ) -> bool:
        type = packet_result.type

        if type in [
            PacketType.REGISTER_USER,
            PacketType.JOIN_USER,
            PacketType.LEAVE_USER,
            PacketType.POLL_NOTIFICATION,
        ]:
            return True

        session_token = packet_result.get_session_token()
        session = context.session_handler.get(session_token)
        if not session_token or not session:
            send_invalid_session_packet(client_socket)
            return False

        last_executed = session.command_cooldowns.get_cooldown(type)

        now = datetime.now()
        time_passed = now - last_executed
        cooldown_time = timedelta(seconds=context.cooldown_table.get_delay(type))

        if time_passed < cooldown_time:
            remaining = cooldown_time.total_seconds() - time_passed.total_seconds()
            send_delayed_command_packet(client_socket, remaining)
            return False

        session.command_cooldowns.use_command(type)
        return True
