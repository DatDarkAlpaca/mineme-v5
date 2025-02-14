from mineme_core.database.table import *


@dataclass
class PlayerEntry:
    uid: str
    balance: float


class PlayerTable(Table):
    def __init__(self, cursor: cursor):
        fields = [
            TableField('uid', 'PRIMARY KEY NOT NULL UNIQUE'),
            TableField('balance', 'REAL NOT NULL'),
        ]

        super().__init__(cursor, 'players', fields)
