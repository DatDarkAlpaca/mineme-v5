from dataclasses import dataclass, field

from mineme_core.database.ore_table import *
from mineme_core.database.user_table import *
from mineme_core.database.player_table import *
from mineme_core.database.category_table import *


@dataclass
class DatabaseData:
    user_table: None | UserTable = None
    player_table: None | PlayerTable = None
    ores: list[Ore] = field(default_factory=list)
    ore_categories: list[OreCategory] = field(default_factory=list)
