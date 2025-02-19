from application import ServerApp
from mineme_core.utils.environment import initialize_environment


def main():
    initialize_environment("./mineme_server/.env")

    server_app = ServerApp()
    server_app.run()


if __name__ == "__main__":
    main()
