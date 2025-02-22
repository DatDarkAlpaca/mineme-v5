from mineme_core.view import View
from mineme_core.localization import _tr
from mineme_core.constants import LOGO_FILE
from mineme_core.utils.file import read_file

from context import ClientContext
from commands import (
    quit_command, 
    clear_command,
    register_command,
    join_command,
    help_command
)


class WelcomeView(View):
    def __init__(self, context: ClientContext):
        super().__init__()
        
        self.context = context
        self.logo = ""

    def on_startup(self):
        self.logo = read_file(LOGO_FILE)

        self.command_handler.register_command("quit", quit_command)
        self.command_handler.register_command("clear", clear_command)
        self.command_handler.register_command("help", help_command)

        self.command_handler.register_command("register", register_command)
        self.command_handler.register_command("join", join_command)

    def on_view_startup(self):
        self.context.console.clear_terminal()
        self.display_header()
        print(_tr("Use the 'join' command to enter the game"))

        if not self.context.client_socket.connect():
            print("Failed to connect to server. Run any commands to retry.")

    def on_render(self):
        self.context.console.set_cursor_bottom()
        self.context.console.get_input()
        self.context.console.reset_cursor()

        self.context.console.clear_terminal()
        self.display_header()

        if self.command_handler.handle_command(
            self.context.console.main_command, self.context
        ):
            return
        else:
            print(_tr("Invalid command. Please try again."))

    def display_header(self):
        print(f"\n{self.logo}\n")
