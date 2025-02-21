from datetime import datetime


class CommandHistory:
    def __init__(self):
        self.history: list[str, datetime] = []

    def append(self, command: str, args: list):
        self.history.append((command + " ".join(args), datetime.now()))
