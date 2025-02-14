import bcrypt

from mineme_core.database.table import *
from mineme_core.game.user import *


class UserTable(Table):
    def __init__(self, cursor: cursor):
        fields = [
            TableField('id', 'SERIAL PRIMARY KEY'),
            TableField('uid', 'TEXT NOT NULL UNIQUE'),
            TableField('username', 'TEXT NOT NULL UNIQUE'),
            TableField('display_name', 'TEXT NOT NULL'),
            TableField('password', 'TEXT NOT NULL UNIQUE'),
        ]

        super().__init__(cursor, 'users', fields)

    def exists_user(self, username: str) -> bool:
        return self.exists('username', username)
    
    def fetch_user(self, username: str) -> User | None:
        if not self.exists_user(username):
            return

        self.cursor.execute("SELECT uid, username, display_name, password FROM users WHERE username=%s", (username,))
        uid, username, display_name, password = self.cursor.fetchone()
        
        return User(uid, username, display_name, password)

    def insert_user(self, entry: User):
        try:
            self.insert_entry(entry.uid, entry.username, entry.display_name, entry.password)
        except:
            return False
        return True

    def verify_user(self, username: str, input_password: str) -> bool:
        if not self.exists_user(username):
            return False

        entry = self.fetch_user(username)
        if not entry:
            return False
    
        hashed_password = entry.password
        return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))
