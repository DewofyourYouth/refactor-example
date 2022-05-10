from dataclasses import dataclass, field
from typing import List

from refactor_example import inventory
from refactor_example.utils import fmt_currency


@dataclass
class OrderRow:
    item: inventory.InventoryItem
    quantity: int = 1
    row_price: int = field(init=False)

    def __post_init__(self):
        self.update_row_price()

    def update_row_price(self):
        self.row_price = self.item.price * self.quantity

    def increment_quantity(self, amount=1):
        self.quantity += amount
        self.update_row_price()

    def decrement_quantity(self, amount=1):
        t = self.quantity - amount
        self.quantity = t if t >= 0 else self.quantity


@dataclass
class Order:
    customer_name: str
    order_items: List[OrderRow]
    balance: int = field(init=False)

    def __post_init__(self):
        self.update_balance()

    def update_balance(self):
        self.balance = sum([row.row_price for row in self.order_items])

    def format_items_to_str(self, row_str: str) -> str:
        row_data = lambda list_item: {
            "name": list_item.item.name,
            "price": fmt_currency(list_item.item.price),
            "quantity": list_item.quantity,
            "total": fmt_currency(list_item.row_price),
        }
        format_row = lambda list_item: row_str.format(**row_data(list_item))
        return "".join([format_row(list_item) for list_item in self.order_items])
