from dataclasses import dataclass, field
from typing import List, TypeVar

from refactor_example import inventory
from refactor_example.utils import fmt_currency

OR = TypeVar("OR", bound="OrderRow")
O = TypeVar("O", bound="Order")


@dataclass
class OrderRow:
    item: inventory.InventoryItem
    quantity: int = 1
    row_price: int = field(init=False)

    def __post_init__(self):
        self.update_row_price()

    def update_row_price(self: OR):
        self.row_price = self.item.price * self.quantity

    def increment_quantity(self: OR, amount: int = 1) -> OR:
        self.quantity += amount
        self.update_row_price()
        return self

    def decrement_quantity(self: OR, amount: int = 1) -> OR:
        t = self.quantity - amount
        self.quantity = t if t >= 0 else self.quantity
        return self


@dataclass
class Order:
    customer_name: str
    order_items: List[OrderRow]
    balance: int = field(init=False)

    def __post_init__(self: O):
        self.update_balance()

    def update_balance(self: O):
        self.balance = sum([row.row_price for row in self.order_items])

    def format_items_to_str(self: O, row_str: str) -> str:
        row_data = lambda list_item: {
            "name": list_item.item.name,
            "price": fmt_currency(list_item.item.price),
            "quantity": list_item.quantity,
            "total": fmt_currency(list_item.row_price),
        }
        format_row = lambda list_item: row_str.format(**row_data(list_item))
        return "".join([format_row(list_item) for list_item in self.order_items])
