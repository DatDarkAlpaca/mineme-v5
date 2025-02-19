import os


class Console:
    def __init__(self):
        self.main_command = ""
        self.arguments = []
        self.last_line = 0

    # Line saving:
    def set_last_line(self, value: int):
        self.last_line = value
    
    def get_last_line(self):
        return self.last_line

    # Cursor:
    def get_terminal_lines(self):
        return os.get_terminal_size().lines

    def set_cursor_bottom(self):
        self.set_cursor(self.get_terminal_lines())

    def set_cursor(self, line: int = 0, column: int = 0):
        print(f"\x1B[{line};{column}H")

    def reset_cursor(self):
        self.set_cursor()

    def save_cursor(self):
        print("\0337", flush=True, end='')
    
    def restore_cursor(self):
        print("\0338", flush=True, end='')
    
    # Input:
    def get_input(self):
        command_args = input("> ").lower().split()
        try:
            self.main_command = command_args[0]
            self.arguments = command_args[1:]
        except:
            return

    # Clear:
    def erase_at_cursor(self):
        print("\033[2K", flush=True, end='')

    def clear_terminal(self):
        print("\033[H\033[J")
