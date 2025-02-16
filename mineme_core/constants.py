from termcolor import colored
from mineme_core.localization import _tr


RESOURCES_FOLDERS = 'res/'
LOGO_FILE = RESOURCES_FOLDERS + 'logo.txt'

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 38532
SESSION_TIMEOUT = 1
CLIENT_TIMEOUT = 3

DEFAULT_COMMAND_DELAY = 0.5

CURRENCY_SYMBOL = 'W$'
CURRENCY_NAME   = 'wonps'

SIZE_MODIFIERS = [
    colored('a tiny ', 'light_magenta'), 
    colored('a small ', 'light_blue'), 
    '', 
    colored('a big ', 'light_yellow'), 
    colored('a massive ', 'light_red'), 
    colored('a humongous ', 'red')
]
