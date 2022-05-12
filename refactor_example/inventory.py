#%%
from dataclasses import dataclass
import json

# Measurement
@dataclass
class Measurement:
    unit: str
    amount: int


@dataclass
class InventoryItem:
    name: str
    price: int
    category: str
    volume: Measurement

    @classmethod
    def from_json(cls, j_dict: dict):
        return InventoryItem(
            name=j_dict["name"],
            category=j_dict["category"],
            price=j_dict["price"],
            volume=Measurement(
                unit=j_dict["volume"]["unit"], amount=j_dict["volume"]["amount"]
            ),
        )


def load_inventory_items():
    with open("inventory_items.json") as f:
        data = json.load(f)
        return [InventoryItem.from_json(d) for d in data]


MILK, CHEESE, BREAD, LUCKY_CHARMS, BEEF = load_inventory_items()

# %%
