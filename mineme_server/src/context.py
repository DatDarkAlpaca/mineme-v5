import os

from dataclasses import dataclass, field
from psycopg2.extensions import cursor, connection

from database_data import DatabaseData
from mineme_core.network.ssp_protocol import SSP_Protocol
from mineme_core.network.packet_handler import PacketHandler
from mineme_core.database.database import create_database_connection
from mineme_core.network.command_cooldown import CommandCooldownTable

from session_data import SessionHandler
from server_socket import ServerSocket


@dataclass
class ServerContext:
    server_socket: ServerSocket | None = None
    packet_handler: PacketHandler = field(default_factory=PacketHandler)
    session_handler: SessionHandler = field(default_factory=SessionHandler)

    cooldown_table: CommandCooldownTable = field(default_factory=CommandCooldownTable)

    database_data: DatabaseData = field(default_factory=DatabaseData)
    db_connection: connection | None = None
    db_cursor: cursor | None = None

    def __post_init__(self):
        ssp_protocol = SSP_Protocol()
        self.server_socket = ServerSocket(
            os.environ.get("SERVER_ADDRESS"),
            int(os.environ.get("SERVER_PORT")),
            ssp_protocol,
            self.packet_handler,
            self.session_handler,
        )

        self.db_connection = create_database_connection()
        self.db_cursor = self.db_connection.cursor()

        self.database_data.initialize(self.db_cursor)
