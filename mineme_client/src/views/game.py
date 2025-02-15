from mineme_core.view import View
from mineme_core.constants import LOGO_FILE
from mineme_core.utils.file import read_file

from commands.quit import view_quit_commmand
from commands.clear import view_clear_commmand
from commands.join_user import view_leave_user

from commands.game_balance import cmd_check_balance
from commands.game_mine import cmd_mine


class GameView(View):
    def __init__(self, application):
        super().__init__()
        self.logo = ''

        self.application = application
        self.console = self.application.console
        self.view_handler = self.application.view_handler
        self.client_socket = self.application.client_socket
        
        self.username = ''
        self.display_name = ''
    
    def on_startup(self):
        self.logo = read_file(LOGO_FILE)

        self.register_command('quit', lambda _: view_quit_commmand(self.application))
        self.register_command('cls', lambda _: view_clear_commmand(self.console, self))
        self.register_command('clear', lambda _: view_clear_commmand(self.console, self))

        self.register_command('leave', lambda _: view_leave_user(self.client_socket, self.view_handler))

        self.register_command('balance', lambda _: cmd_check_balance(self.client_socket))
        self.register_command('mine', lambda _: cmd_mine(self.client_socket))

    def on_view_startup(self):
        self.console.clear_terminal()
        self.display_header()

    def on_render(self):
        self.console.get_input()

        self.console.clear_terminal()
        self.display_header()

        if self.handle_command(self.console.main_command, self.console.arguments):
            return
        else:
            print('Invalid command. Please try again.')

    def set_user(self, username: str, display_name: str):
        self.username = username
        self.display_name = display_name

    def display_header(self):
        print(f"\n{self.logo}\n")
        print(f"* Logged in: {self.display_name}")
