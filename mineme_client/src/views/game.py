from mineme_core.view import View
from mineme_core.constants import LOGO_FILE
from mineme_core.utils.file import read_file

from commands import (
    quit_command,
    clear_command,
    leave_command,
    balance_command,
    mine_command,
    gamble_command,
    history_command,
    ore_command,
    pay_command,
    help_command,
    users_command
)

from tasks import handle_notifications
from context import ClientContext


class GameView(View):
    def __init__(self, context: ClientContext):
        super().__init__()

        self.context = context
        self.logo = ""

    def on_startup(self):
        self.logo = read_file(LOGO_FILE)

        self.command_handler.register_on_command_start(
            lambda context: self.context.command_history.append(
                context.console.main_command, context.console.arguments
            )
        )

        self.command_handler.register_command("quit", quit_command)
        self.command_handler.register_command("cls", clear_command)
        self.command_handler.register_command("history", history_command)
        self.command_handler.register_command("help", help_command)

        self.command_handler.register_command("leave", leave_command)

        self.command_handler.register_command("balance", balance_command)
        self.command_handler.register_command("mine", mine_command)
        self.command_handler.register_command("gamble", gamble_command)
        self.command_handler.register_command("ore", ore_command)
        self.command_handler.register_command("pay", pay_command)

        self.command_handler.register_command("users", users_command)

    def on_view_startup(self):
        self.context.console.clear_terminal()
        self.display_header()

        self.register_task(lambda: handle_notifications(self.context), 1)

    def on_view_shutdown(self):
        self.context.username = ""
        self.context.display_name = ""
        self.context.session_token = ""

        self.clear_tasks()

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
            print("Invalid command. Please try again.")

    def display_header(self):
        print(f"{self.logo}\n")
        print(f"* Logged in: {self.context.display_name}")

        lines_used = self.logo.count("\n") + 2
        self.context.console.set_last_line(lines_used)
