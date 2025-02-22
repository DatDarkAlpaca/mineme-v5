from context import ClientContext
from mineme_core.commands import Command


def cmd_quit(context: ClientContext):
    context.running = False


quit_command = Command(
    "quit", "exits the application", "quit", ["exit", "e", "q"], cmd_quit
)
