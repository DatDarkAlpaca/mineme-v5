from dataclasses import dataclass


@dataclass
class User:
    uid: str = ""
    username: str = ""
    display_name: str = ""
    password: str = ""
