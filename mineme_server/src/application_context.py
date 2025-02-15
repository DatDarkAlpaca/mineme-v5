from dataclasses import dataclass, field
from psycopg2.extensions import cursor, connection 

from database_data import DatabaseData
from mineme_server.src.session_data import *
from mineme_core.network.packet_handler import *
from mineme_core.network.network import MineSocket

@dataclass
class ServerContext:
    server_socket: MineSocket | None = None
    session_data: dict[session_token, SessionData] = field(default_factory=dict)

    packet_handler: PacketHandler = field(default_factory=PacketHandler)
    
    db_connection: connection | None = None
    db_cursor: cursor | None = None

    database_data: DatabaseData = field(default_factory=DatabaseData)