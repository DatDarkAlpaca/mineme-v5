from typing import Callable, Protocol


class View(Protocol):
    def __init__(self):
        self.command_list: dict = {}
        self.handler = None

    def on_startup(self):
        ...

    def on_view_startup(self):
        ...

    def on_render(self):
        ...

    def on_update(self):
        ...

    def on_view_shutdown(self):
        ...

    def register_command(self, command_name: str, function: Callable):
        self.command_list[command_name] = function

    def handle_command(self, command: str, args: list) -> bool:
        command_function = self.command_list.get(command)
        if not command_function:
            return False
        
        command_function(args)
        return True
    
    def _set_handler(self, handler):
        self.handler = handler


class ViewHandler:
    def __init__(self):
        self.views: list[View] = []
        self.current_view: None | View = None
    
    def register_view(self, view: View) -> int:
        view._set_handler(self)
        view.on_startup()
        
        self.views.append(view)
        return len(self.views) - 1

    def set_view(self, view_handle: int):
        if self.current_view:
            self.current_view.on_view_shutdown()
        
        self.current_view = self.views[view_handle]
        
        if self.current_view:
            self.current_view.on_view_startup()

    def on_render(self):
        self.current_view.on_render()

    def on_update(self):
        self.current_view.on_update()
