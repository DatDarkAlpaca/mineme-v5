from mineme_core.view import View
from mineme_core.constants import LOGO_FILE
from mineme_core.utils.file import read_file

from commands.quit import cmd_quit
from commands.clear import cmd_clear
from commands.register_user import cmd_register
from commands.join_user import cmd_join

from context import ClientContext


class WelcomeView(View):
    def __init__(self, context: ClientContext):
        super().__init__()

        self.context = context
        self.logo = ''

    def on_startup(self):
        self.logo = read_file(LOGO_FILE)

        self.register_command('quit', lambda _: cmd_quit(self.context))
        self.register_command('cls', lambda _: cmd_clear(self.context))
        self.register_command('clear', lambda _: cmd_clear(self.context))
        
        self.register_command('register', lambda _: cmd_register(self.context))
        self.register_command('join', lambda _: cmd_join(self.context))

    def on_view_startup(self):
        self.context.console.clear_terminal()
        self.display_header()

    def on_render(self):
        self.context.console.get_input()
        self.context.console.clear_terminal()
        self.display_header()

        if self.handle_command(self.context.console.main_command, self.context.console.arguments):
            return
        else:
            print('Invalid command. Please try again.')
        
    def display_header(self):
        print(f"\n{self.logo}\n")
