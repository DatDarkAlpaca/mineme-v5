from mineme_core.game.player import Player
from mineme_core.database.table import *


class PlayerTable(Table):
    def __init__(self, cursor: cursor):
        fields = [
            TableField("id", "SERIAL PRIMARY KEY"),
            TableField("uid", "TEXT REFERENCES users (uid)"),
            TableField("balance", "REAL NOT NULL "),
        ]

        super().__init__(cursor, "players", fields)

    def insert_player(self, uid: str, balance: int = 0) -> bool:
        try:
            self.cursor.execute(
                "INSERT INTO players (uid, balance) VALUES (%s, %s)", (uid, balance)
            )
        except:
            return False
        return True

    def fetch_player(self, uid: str) -> Player | None:
        if not self.exists("uid", uid):
            return

        self.cursor.execute("SELECT uid, balance FROM players WHERE uid = %s", (uid,))
        uid, balance = self.cursor.fetchone()
        return Player(uid, balance)

    def fetch_player_by_username(self, username: str) -> Player | None:
        if not self.exists("username", username):
            return

        self.cursor.execute(
            "SELECT uid, balance FROM players WHERE username = %s", (username,)
        )
        uid, balance = self.cursor.fetchone()
        return Player(uid, balance)

    def update_player_balance(self, uid: str, balance: float):
        self.cursor.execute(
            "UPDATE players SET balance=%s WHERE uid = %s", (balance, uid)
        )
