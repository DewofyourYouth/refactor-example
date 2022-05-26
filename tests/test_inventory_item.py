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
            item_id="fe865a93-cdee-4d6d-9716-97d2afdf7b7c",
            name="Whole Milk",
            price=416,
            category="Dairy",
            volume=Measurement(unit="Gallon", amount=1),
        )


@mark.it("load_inventory_items_from_file can load InventoryItems from a json file.")
def test_load_inventory_items_from_file():
    assert load_inventory_items_from_file("inventory_items.json") == [
        InventoryItem(
            item_id="fe865a93-cdee-4d6d-9716-97d2afdf7b7c",
            name="Whole Milk",
            price=416,
            category="Dairy",
            volume=Measurement(unit="Gallon", amount=1),
        ),
        InventoryItem(
            item_id="8efdbf5e-40cb-42f8-899a-22f7cfa32679",
            name="American Processed Cheese",
            price=389,
            category="Dairy",
            volume=Measurement(unit="Pound", amount=1),
        ),
        InventoryItem(
            item_id="3a291734-3320-406e-84f9-b230f135f636",
            name="White Bread",
            price=250,
            category="Bread",
            volume=Measurement(unit="Loaf", amount=1),
        ),
        InventoryItem(
            item_id="b286e9d7-6e24-452d-9608-1de4422d6ee3",
            name="Lucky Charms",
            price=1222,
            category="Breakfast Cereal",
            volume=Measurement(unit="Gallon", amount=1),
        ),
        InventoryItem(
            item_id="660e0b0e-546f-4392-8943-2d7e73942100",
            name="Beef Choice Angus Ribeye Steak",
            price=2270,
            category="Meat & Seafood",
            volume=Measurement(unit="Ounces", amount=32),
        ),
    ]
