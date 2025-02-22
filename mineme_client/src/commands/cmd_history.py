from context import ClientContext
from mineme_core.commands import Command


def cmd_history(context: ClientContext):
    history = context.command_history.history
    args = context.console.arguments

    if len(args) >= 1:
        subcommand = args[0].lower()
        if subcommand == "clear":
            history.clear()
            return print("Cleared command history")

    print("\nCommands List:")
    for command, time in context.command_history.history:
        formatted_time = time.strftime("%H:%M:%S")
        print(f"* [{formatted_time}] {command}")


history_command = Command(
    "history",
    "display a commands history",
    "history",
    [],
    cmd_history
)
