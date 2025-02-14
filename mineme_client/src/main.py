import os
from views.welcome_view import WelcomeView
from views.game import GameView
from mineme_client.src.application import Application
from mineme_core.utils.environment import initialize_environment


def main():
    os.chdir('./mineme_client')
    initialize_environment('./.env')

    app = Application()
    app.view_handler.register_view(WelcomeView(app), 'welcome')
    app.view_handler.register_view(GameView(app), 'game')

    app.view_handler.set_view('welcome')

    app.run()


if __name__ == '__main__':
    main()
