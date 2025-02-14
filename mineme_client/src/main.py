import os
from views.welcome_view import WelcomeView
from mineme_client.src.application import Application
from mineme_core.utils.environment import initialize_environment


def main():
    os.chdir('./mineme_client')
    initialize_environment('./.env')

    app = Application()
    welcome_view = app.view_handler.register_view(WelcomeView(app))
    app.view_handler.set_view(welcome_view)

    app.run()


if __name__ == '__main__':
    main()
