from context import ClientContext


def cmd_clear(context: ClientContext):
    context.console.clear_terminal()
    context.view_handler.current_view.display_header()
