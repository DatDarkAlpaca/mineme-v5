import os

from mineme_core.localization import initialize_localization
from mineme_core.utils.environment import initialize_environment

from views.game import GameView
from views.welcome_view import WelcomeView

from application import Application


def main():
    os.chdir("./mineme_client")

    initialize_environment("./.env")
    initialize_localization("./languages.json")

    app = Application()
    app.context.view_handler.register_view(WelcomeView(app.context), "welcome")
    app.context.view_handler.register_view(GameView(app.context), "game")

    app.context.view_handler.set_view("welcome")

    app.run()


if __name__ == "__main__":
    main()
