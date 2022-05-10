import json
from dataclasses import dataclass


@dataclass
class Measurement:
    unit: str
    amount: int


@dataclass
class InventoryItem:
    item_id: str
    name: str
    price: int
    category: str
    volume: Measurement

    @classmethod
    def from_json(cls, j_dict: dict):
        return InventoryItem(
            item_id=j_dict["itemId"],
            name=j_dict["name"],
            category=j_dict["category"],
            price=j_dict["price"],
            volume=Measurement(
                unit=j_dict["volume"]["unit"], amount=j_dict["volume"]["amount"]
            ),
        )


def load_inventory_items_from_file(json_file: str):
    with open(json_file) as f:
        data = json.load(f)
        return [InventoryItem.from_json(d) for d in data]


MILK, CHEESE, BREAD, LUCKY_CHARMS, BEEF = load_inventory_items_from_file(
    "inventory_items.json"
)
