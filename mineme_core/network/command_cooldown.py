import os
from datetime import datetime
from mineme_core.network.packet import PacketType


class CommandCooldown:
    def __init__(self):
        self.cooldown_table: dict[PacketType, datetime] = {}

        now = datetime.now()
        for type in PacketType:
            self.cooldown_table[type] = now

    def use_command(self, type: PacketType) -> datetime:
        self.cooldown_table[type] = datetime.now()

    def get_cooldown(self, type: PacketType) -> datetime:
        try:
            return self.cooldown_table[type]
        except Exception:
            print(f"Error: unregistered packet type cooldown: {type}")


class CommandCooldownTable:
    command_delays: dict[PacketType, int] = {}

    @classmethod
    def initialize(cls):
        cls.command_delays[PacketType.MINE] = 1
        cls.command_delays[PacketType.GAMBLE] = 1

    @classmethod
    def get_delay(cls, type: PacketType):
        return cls.command_delays.get(
            type, float(os.environ.get("DEFAULT_COMMAND_DELAY"))
        )
