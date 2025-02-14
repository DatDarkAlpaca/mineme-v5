import json
from dataclasses import dataclass, asdict


@dataclass
class Ore:
    id: int
    name: str
    rarity: str
    category_id: int
    price: float
    min_weight: float
    max_weight: float
