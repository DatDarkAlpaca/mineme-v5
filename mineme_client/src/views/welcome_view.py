from mineme_core.view import View
from mineme_core.localization import _tr
from mineme_core.constants import LOGO_FILE
from mineme_core.utils.file import read_file

from mineme_client.src.commands.cmd_quit import cmd_quit
from mineme_client.src.commands.cmd_clear import cmd_clear
from mineme_client.src.commands.cmd_register import cmd_register
from mineme_client.src.commands.cmd_join import cmd_join

from context import ClientContext


class WelcomeView(View):
    def __init__(self, context: ClientContext):
        super().__init__()

        self.context = context
        self.logo = ""

    def on_startup(self):
        self.logo = read_file(LOGO_FILE)

        self.register_command("quit", lambda _: cmd_quit(self.context))
        self.register_command("cls", lambda _: cmd_clear(self.context))
        self.register_command("clear", lambda _: cmd_clear(self.context))

        self.register_command("register", lambda _: cmd_register(self.context))
        self.register_command("join", lambda _: cmd_join(self.context))

    def on_view_startup(self):
        self.context.console.clear_terminal()
        self.display_header()
        print(_tr("Use the 'join' command to enter the game"))

    def on_render(self):
        self.context.console.get_input()
        self.context.console.clear_terminal()
        self.display_header()

        if self.handle_command(
            self.context.console.main_command, self.context.console.arguments
        ):
            return
        else:
            print(_tr("Invalid command. Please try again."))

    def display_header(self):
        print(f"\n{self.logo}\n")
