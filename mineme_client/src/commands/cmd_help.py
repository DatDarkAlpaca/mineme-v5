from context import ClientContext
from mineme_core.commands import Command


def display_command_help(command: Command):
    print(f"Usage: { command.usage}")
    if not command.aliases:
        print(f"    {command.description}")
    else:
        print(f"    {command.description}. Aliases: \"{', '.join(command.aliases)}\"")


def cmd_help(context: ClientContext):
    command_handler = context.view_handler.current_view.command_handler
    arguments = context.console.arguments
    
    selected_command = ''
    if len(arguments) > 0:
        selected_command = arguments[0]
    
    # Selected:
    if selected_command:
        command = command_handler.command_list.get(selected_command)
        if not command:
            return print("This command does not exist. For a list of commands, type 'help'")
        
        return display_command_help(command)

    # All:
    show_commands = []
    for _, command in command_handler.command_list.items():
        if command.name in show_commands:
            continue
        display_command_help(command)
        print()

        show_commands.append(command.name)


help_command = Command(
    "help",
    "displays the help menu",
    "help (command_name)",
    None,
    cmd_help
)
