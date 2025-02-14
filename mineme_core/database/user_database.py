import bcrypt
from dataclasses import dataclass
from psycopg2.extensions import cursor


@dataclass
class UserEntry:
    uid: str
    username: str
    display_name: str
    password: str


def initialize_user_table(cursor: cursor) -> None:
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                   id SERIAL PRIMARY KEY,
                   uid TEXT NOT NULL UNIQUE,
                   username TEXT NOT NULL UNIQUE,
                   display_name TEXT NOT NULL,
                   password TEXT NOT NULL)
                   """)


def exists_username_entry(cursor: cursor, username: str) -> bool:
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    return cursor.fetchone()


def fetch_user_entry(cursor: cursor, username: str) -> UserEntry:
    if not exists_username_entry(cursor, username):
        return

    cursor.execute("SELECT uid, username, display_name, password FROM users WHERE username=%s", (username,))
    uid, username, display_name, password = cursor.fetchone()

    return UserEntry(uid, username, display_name, password)


def create_user_entry(cursor: cursor, entry: UserEntry) -> bool:
    try:
        cursor.execute("""INSERT INTO users (uid, username, display_name, password) VALUES(%s, %s, %s, %s)""", 
                       (entry.uid, entry.username, entry.display_name, entry.password))
    except:
        return False
    
    return True


def verify_user_entry(cursor: cursor, username: str, password: UserEntry) -> bool:
    if not exists_username_entry(cursor, username):
        return False

    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    if not result:
        return False
    
    hashed_password = result[0]
    result_password = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    return result_password
