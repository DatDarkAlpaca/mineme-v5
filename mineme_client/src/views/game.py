from mineme_core.view import View
from mineme_core.constants import LOGO_FILE
from mineme_core.utils.file import read_file

from commands.quit import view_quit_commmand
from commands.clear import view_clear_commmand
from commands.join_user import view_leave_user


class GameView(View):
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
        self.register_command('cls', lambda _: view_clear_commmand(self.console))
        self.register_command('clear', lambda _: view_clear_commmand(self.console))

        self.register_command('leave', lambda _: view_leave_user(self.client_socket, self.view_handler))

    def on_render(self):
        print()
        print(self.logo)
        print('Logged in')
        print()

    def on_update(self):
        self.console.get_input()
        if self.handle_command(self.console.main_command, self.console.arguments):
            return

        self.console.clear_terminal()
        print('Invalid command. Please try again.')
        print()