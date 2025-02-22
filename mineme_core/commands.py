from typing import Callable
from dataclasses import dataclass, field


@dataclass
class Command:
    name: str
    description: str = ''
    usage: str = ''
    aliases: list = field(default_factory=list)
    function: Callable = field(default_factory=Callable)


class CommandHandler:
    def __init__(self):
        self.on_command_start_list: list[Callable] = []
        self.command_list: dict[str, Command] = {}

    def register_on_command_start(self, function: Callable):
        self.on_command_start_list.append(function)

    def register_command(self, command_name: str, command: Command):
        self.command_list[command_name] = command
        
        if command.aliases and len(command.aliases) > 0:
            for command_alias in command.aliases:
                self.command_list[command_alias] = command

    def handle_command(self, command_name: str, context) -> bool:
        command = self.command_list.get(command_name)
        if not command:
            return False

        for function in self.on_command_start_list:
            function(context)

        command.function(context)
        return True
