from refactor_example.inventory import *
from pytest import mark

milk = {
    "itemId": "fe865a93-cdee-4d6d-9716-97d2afdf7b7c",
    "name": "Whole Milk",
    "category": "Dairy",
    "volume": {"unit": "Gallon", "amount": 1},
    "price": 416,
}


@mark.describe("InventoryItem is a class for storing items available in the inventory.")
class TestInventoryItem:
    @mark.it("InventoryItem.from_json takes a dict and returns an inventory item")
    def test_load_inventory_item(self):
        assert InventoryItem.from_json(milk) == InventoryItem(
            name="Whole Milk",
            price=416,
            category="Dairy",
            volume=Measurement(unit="Gallon", amount=1),
        )


@mark.it(
    "load_inventory_items_from_file can load InventoryItems from 'inventory_items.json'."
)
def test_load_inventory_items_from_file():
    assert load_inventory_items() == [
        InventoryItem(
            name="Whole Milk",
            price=416,
            category="Dairy",
            volume=Measurement(unit="Gallon", amount=1),
        ),
        InventoryItem(
            name="American Processed Cheese",
            price=389,
            category="Dairy",
            volume=Measurement(unit="Pound", amount=1),
        ),
        InventoryItem(
            name="White Bread",
            price=250,
            category="Bread",
            volume=Measurement(unit="Loaf", amount=1),
        ),
        InventoryItem(
            name="Lucky Charms",
            price=1222,
            category="Breakfast Cereal",
            volume=Measurement(unit="Gallon", amount=1),
        ),
        InventoryItem(
            name="Beef Choice Angus Ribeye Steak",
            price=2270,
            category="Meat & Seafood",
            volume=Measurement(unit="Ounces", amount=32),
        ),
    ]
