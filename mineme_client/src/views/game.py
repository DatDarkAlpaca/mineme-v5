from mineme_core.view import View
from mineme_core.constants import LOGO_FILE
from mineme_core.utils.file import read_file

from mineme_client.src.commands.cmd_quit import cmd_quit
from mineme_client.src.commands.cmd_clear import cmd_clear
from mineme_client.src.commands.cmd_join import cmd_leave

from mineme_client.src.commands.cmd_balance import cmd_balance
from mineme_client.src.commands.cmd_mine import cmd_mine
from mineme_client.src.commands.cmd_gamble import cmd_gamble
from mineme_client.src.commands.cmd_ore import cmd_ore
from mineme_client.src.commands.cmd_pay import cmd_pay

from tasks import handle_notifications
from context import ClientContext


class GameView(View):
    def __init__(self, context: ClientContext):
        super().__init__()

        self.context = context

        self.display_name = ""
        self.username = ""
        self.logo = ""

    def on_startup(self):
        self.logo = read_file(LOGO_FILE)

        self.register_command("quit", lambda _: cmd_quit(self.context))
        self.register_command("cls", lambda _: cmd_clear(self.context))
        self.register_command("clear", lambda _: cmd_clear(self.context))

        self.register_command("leave", lambda _: cmd_leave(self.context))

        self.register_command("balance", lambda _: cmd_balance(self.context))
        self.register_command("mine", lambda _: cmd_mine(self.context))
        self.register_command("gamble", lambda _: cmd_gamble(self.context))
        self.register_command("ore", lambda _: cmd_ore(self.context))
        self.register_command("pay", lambda _: cmd_pay(self.context))

    def on_view_startup(self):
        self.context.console.clear_terminal()
        self.display_header()

        self.register_task(lambda: handle_notifications(self.context), 1)

    def on_view_shutdown(self):
        self.username = ""
        self.display_name = ""
        self.context.session_token = ""

        self.clear_tasks()

    def on_render(self):
        self.context.console.set_cursor_bottom()
        self.context.console.get_input()
        self.context.console.reset_cursor()

        self.context.console.clear_terminal()
        self.display_header()

        if self.handle_command(
            self.context.console.main_command, self.context.console.arguments
        ):
            return
        else:
            print("Invalid command. Please try again.")

    def set_user(self, username: str, display_name: str, session_token: str):
        self.username = username
        self.display_name = display_name
        self.context.session_token = session_token

    def display_header(self):
        print(f"{self.logo}\n")
        print(f"* Logged in: {self.display_name}")

        lines_used = self.logo.count('\n') + 2
        self.context.console.set_last_line(lines_used)
