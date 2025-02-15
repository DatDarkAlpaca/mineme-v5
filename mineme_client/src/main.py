import os
from views.welcome_view import WelcomeView
from views.game import GameView
from mineme_client.src.application import Application
from mineme_core.utils.environment import initialize_environment


def main():
    os.chdir('./mineme_client')
    initialize_environment('./.env')

    app = Application()
    app.context.view_handler.register_view(WelcomeView(app.context), 'welcome')
    app.context.view_handler.register_view(GameView(app.context), 'game')

    app.context.view_handler.set_view('welcome')

    app.run()


if __name__ == '__main__':
    main()
