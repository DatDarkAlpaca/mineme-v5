from dataclasses import dataclass, field
from psycopg2.extensions import cursor, connection 

from client_data import ClientData
from database_data import DatabaseData
from mineme_core.network.network import MineSocket
from mineme_core.network.packet_handler import PacketHandler


@dataclass
class ServerAppData:
    server_socket: MineSocket | None = None
    client_data: dict[str, ClientData] = field(default_factory=dict)
    packet_handler: PacketHandler = field(default_factory=PacketHandler)
    
    db_connection: connection | None = None
    db_cursor: cursor | None = None

    database_data: DatabaseData = field(default_factory=DatabaseData)