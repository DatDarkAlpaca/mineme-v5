from mineme_core.database.table import *
from mineme_core.game.ore import Ore


class OreTable(Table):
    def __init__(self, cursor: cursor):
        fields = [
            TableField('id', 'SERIAL PRIMARY KEY'),
            TableField('name', 'TEXT NOT NULL'),
            TableField('rarity', 'REAL NOT NULL'),
            TableField('category_id', 'SERIAL NOT NULL REFERENCES ore_categories (id)'),
            TableField('price', 'REAL NOT NULL'),
            TableField('min_weight', 'REAL NOT NULL'),
            TableField('max_weight', 'REAL NOT NULL'),
        ]

        super().__init__(cursor, 'ores', fields)

    def get_all_ores(self) -> list[Ore]:
        self.cursor.execute("SELECT id, name, rarity, category_id, price, min_weight, max_weight FROM ores")
        
        ores: list[Ore] = []
        for id, name, rarity, category_id, price, min_weight, max_weight in self.cursor.fetchall():
            ores.append(Ore(id, name, rarity, category_id, price, min_weight, max_weight))

        return ores
