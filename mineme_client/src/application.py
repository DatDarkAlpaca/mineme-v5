from context import ClientContext


class Application:
    def __init__(self):
        self.context = ClientContext()

    def run(self):
        while self.context.running:
            self.context.view_handler.on_render()
