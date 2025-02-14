from mineme_core.view import View
from mineme_core.constants import LOGO_FILE
from mineme_core.utils.file import read_file

from commands.quit import view_quit_commmand
from commands.clear import view_clear_commmand
from commands.register_user import view_register_user
from commands.join_user import view_join_user


class WelcomeView(View):
    def __init__(self, application):
        super().__init__()

        self.application = application
        self.console = self.application.console
        self.view_handler = self.application.view_handler
        self.client_socket = self.application.client_socket

        self.logo = ''

    def on_startup(self):
        self.logo = read_file(LOGO_FILE)

        self.register_command('quit', lambda _: view_quit_commmand(self.application))
        self.register_command('cls', lambda _: view_clear_commmand(self.console, self))
        self.register_command('clear', lambda _: view_clear_commmand(self.console, self))
        
        self.register_command('register', lambda _: view_register_user(self.console.arguments, self.client_socket))
        self.register_command('join', lambda _: view_join_user(self.console.arguments, self.client_socket, self.view_handler))

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
        
    def display_header(self):
        print(f"\n{self.logo}\n")
