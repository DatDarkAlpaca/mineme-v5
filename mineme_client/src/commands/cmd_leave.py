from mineme_core.commands import Command
from mineme_core.network.packet import Packet, PacketType

from context import ClientContext


def cmd_leave(context: ClientContext):
    client_socket = context.client_socket
    view_handler = context.view_handler

    data = {"session_token": context.session_token}

    client_socket.send(Packet(PacketType.LEAVE_USER, data))
    view_handler.set_view("welcome")


leave_command = Command(
    "leave",
    "attempts to leave the game",
    "leave",
    [],
    cmd_leave
)
