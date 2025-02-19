from context import ClientContext


def cmd_quit(context: ClientContext):
    context.running = False
