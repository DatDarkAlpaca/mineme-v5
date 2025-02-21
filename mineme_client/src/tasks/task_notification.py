from mineme_core.network.packet import Packet, PacketType
from context import ClientContext
from termcolor import colored


def handle_notifications(context: ClientContext):
    data = {
        "session_token": context.session_token
    }
    context.client_socket.send(Packet(PacketType.POLL_NOTIFICATION, data))
    packet_result = context.client_socket.receive()

    if not packet_result.is_valid():
        return
    
    messages = packet_result.data['messages']
    if len(messages) == 0:
        return
    
    context.console.save_cursor()

    after_logo_line = context.console.get_last_line()
    context.console.set_cursor(after_logo_line)
    
    for message in messages:
        context.console.erase_at_cursor()
        print(f"[ {colored("!", "light_yellow")} ]: {message}")
        
    context.console.restore_cursor()
