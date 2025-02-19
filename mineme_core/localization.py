import os
import json


localization_table = {}


def initialize_localization(filepath: str):
    global localization_table
    with open(filepath, mode="r", encoding="utf-8") as file:
        localization_table = json.load(file)


def _tr(english_string: str, *args) -> str:
    # TODO: error handling
    # TODO: settings manager -> language
    global localization_table, language
    return localization_table[os.environ.get("LANGUAGE")][english_string].format(*args)
