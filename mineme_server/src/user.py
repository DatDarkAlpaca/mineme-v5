from dataclasses import dataclass


@dataclass
class User:
    username: str = ''
    display_name: str = ''
    uid: str = ''