import random
from dataclasses import dataclass
from mineme_core.game.ore import Ore


@dataclass
class MineResult:
    ore: Ore
    weight: float


def mine(ores: list[Ore]) -> MineResult:
    ore_ids = [ore.id for ore in ores]
    ore_rarities = [ore.rarity for ore in ores]

    chosen_ore_id = random.choices(ore_ids, ore_rarities)
    chosen_ore: Ore | None = None
    for ore in ores:
        if ore.id == chosen_ore_id:
            chosen_ore = ore

    weight = random.uniform(chosen_ore.min_weight, chosen_ore.max_weight)
    return MineResult(ore, weight)
