from dataclasses import dataclass, field

from mineme_core.database.user_table import UserTable
from mineme_core.database.ore_table import Ore, OreTable
from mineme_core.database.player_table import PlayerTable
from mineme_core.database.category_table import OreCategory, OreCategoryTable


@dataclass
class DatabaseData:
    user_table: None | UserTable = None
    player_table: None | PlayerTable = None
    ores: list[Ore] = field(default_factory=list)
    ore_categories: list[OreCategory] = field(default_factory=list)

    def initialize(self, cursor):
        self.user_table = UserTable(cursor)
        self.player_table = PlayerTable(cursor)

        ore_table = OreTable(cursor)
        ore_categories = OreCategoryTable(cursor)

        self.ores = ore_table.get_all_ores()
        self.ore_categories = ore_categories.get_all_ore_categories()
