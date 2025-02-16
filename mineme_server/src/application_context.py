from dataclasses import dataclass, field
from psycopg2.extensions import cursor, connection 

from database_data import DatabaseData
from mineme_server.src.session_data import *
from mineme_core.network.packet_handler import *
from mineme_core.network.network import MineSocket
from mineme_core.database.database import create_database_connection
from mineme_core.network.command_cooldown import CommandCooldownTable

@dataclass
class ServerContext:
    server_socket: MineSocket | None = None
    packet_handler: PacketHandler = field(default_factory=PacketHandler)
    session_data: dict[session_token, SessionData] = field(default_factory=dict)

    cooldown_table: CommandCooldownTable = field(default_factory=CommandCooldownTable)
    
    database_data: DatabaseData = field(default_factory=DatabaseData)
    db_connection: connection | None = None
    db_cursor: cursor | None = None

    def initialize(self, address, port):
        self.server_socket = initialize_server_socket(address, port)

        self.db_connection = create_database_connection()
        self.db_cursor = self.db_connection.cursor()

        self.database_data.initialize(self.db_cursor)