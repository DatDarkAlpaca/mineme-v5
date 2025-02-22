from context import ClientContext
from mineme_core.commands import Command


def cmd_clear(context: ClientContext):
    context.console.clear_terminal()
    context.view_handler.current_view.display_header()


clear_command = Command(
    "clear",
    "clears the console screen",
    "clear",
    ["cls"],
    cmd_clear
)
