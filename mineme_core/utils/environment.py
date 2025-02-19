from dotenv import load_dotenv, find_dotenv


def initialize_environment(filepath: str = None):
    if not filepath:
        filepath = find_dotenv()

    if not load_dotenv(filepath):
        print("Failed to load .env file")
