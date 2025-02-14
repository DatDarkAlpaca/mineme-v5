import json
from mineme_core.network.network import MineSocket, PacketType


def view_mine(client_socket: MineSocket):
    client_socket.send_packet_default(PacketType.MINE)

    packet, _ = client_socket.receive_packet()
    response_code, data = packet.data.split(',', 1)

    if response_code == '1':
        return print('Failed to mine anything...')
    
    ore_data = json.loads(data)
    name = ore_data['ore_name']
    weight = ore_data['weight']    
    price = ore_data['price']

    print(name, weight, price)