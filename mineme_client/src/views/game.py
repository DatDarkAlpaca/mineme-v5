from mineme_core.view import View
from mineme_core.constants import LOGO_FILE
from mineme_core.utils.file import read_file

from commands.quit import cmd_quit
from commands.clear import cmd_clear
from commands.join_user import cmd_leave

from commands.game_balance import cmd_check_balance
from commands.game_mine import cmd_mine

from context import ClientContext


class GameView(View):
    def __init__(self, context: ClientContext):
        super().__init__()

        self.context = context

        self.display_name = ''
        self.username = ''
        self.logo = ''
        
    def on_startup(self):
        self.logo = read_file(LOGO_FILE)

        self.register_command('quit', lambda _: cmd_quit(self.context))
        self.register_command('cls', lambda _: cmd_clear(self.context))
        self.register_command('clear', lambda _: cmd_clear(self.context))

        self.register_command('leave', lambda _: cmd_leave(self.context))

        self.register_command('balance', lambda _: cmd_check_balance(self.context))
        self.register_command('mine', lambda _: cmd_mine(self.context))

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

    def set_user(self, username: str, display_name: str, session_token: str):
        self.username = username
        self.display_name = display_name
        self.context.session_token = session_token
    
    def display_header(self):
        print(f"\n{self.logo}\n")
        print(f"* Logged in: {self.display_name}")
