from mineme_core.database.table import *


@dataclass
class OreCategory:
    id: int
    name: str


class OreCategoryTable(Table):
    def __init__(self, cursor: cursor):
        fields = [
            TableField('id', 'SERIAL PRIMARY KEY'),
            TableField('name', 'TEXT NOT NULL'),
        ]

        super().__init__(cursor, 'ore_categories', fields)

    def get_all_ore_categories(self) -> list[OreCategory]:
        self.cursor.execute("SELECT id, name FROM ore_categories")
        
        ore_categories: list[OreCategory] = []
        for id, name in self.cursor.fetchall():
            ore_categories.append(OreCategory(id, name))

        return ore_categories
