from mineme_core.game.player import Player
from mineme_core.database.table import *


class PlayerTable(Table):
    def __init__(self, cursor: cursor):
        fields = [
            TableField('uid', 'TEXT PRIMARY KEY'),
            TableField('balance', 'REAL NOT NULL'),
        ]

        super().__init__(cursor, 'players', fields)

    def fetch_player(self, uid: str) -> Player:
        if not self.exists('uid', uid):
            return
        
        self.cursor.execute("SELECT uid, balance FROM players WHERE uid = %s", (uid,))
        uid, balance = self.cursor.fetchone()
        return Player(uid, balance)
