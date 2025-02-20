import time
from queue import Queue
from threading import Thread
from typing import Callable, Protocol


class View(Protocol):
    def __init__(self):
        self.on_execute_function_list: list = []
        self.command_list: dict = {}
        self.tasks = Queue()
        
        self.event_thread = Thread(target=lambda: self.__execute_tasks(), daemon=True)
        self.event_thread.start()

        self.handler = None

    def display_header(self): ...

    def on_startup(self): ...

    def on_view_startup(self): ...

    def on_view_shutdown(self): ...

    def register_on_execute(self, function: Callable):
        self.on_execute_function_list.append(function)

    def register_command(self, command_name: str, function: Callable):
        self.command_list[command_name] = function

    def register_task(self, function: Callable, cooldown: int):
        self.tasks.put((function, cooldown))

    def clear_tasks(self):
        self.tasks = Queue()

    def handle_command(self, command: str, args: list) -> bool:
        command_function = self.command_list.get(command)
        if not command_function:
            return False

        for function in self.on_execute_function_list:
            function(command, args)

        command_function(args)
        return True

    def _set_handler(self, handler):
        self.handler = handler

    def __execute_tasks(self):
        while True:
            function, cooldown = self.tasks.get(block=True)
            function()
            self.tasks.put((function, cooldown))
            time.sleep(cooldown)

class ViewHandler:
    def __init__(self):
        self.views: dict[str] = {}
        self.current_view: None | View = None

    def register_view(self, view: View, view_name: str):
        view._set_handler(self)
        view.on_startup()

        self.views[view_name] = view

        if not self.current_view:
            self.current_view = view

    def get_view(self, view_name: str) -> View | None:
        return self.views.get(view_name)

    def set_view(self, view_name: str):
        if self.current_view:
            self.current_view.on_view_shutdown()

        self.current_view = self.views[view_name]

        if self.current_view:
            self.current_view.on_view_startup()

    def on_render(self):
        self.current_view.on_render()
