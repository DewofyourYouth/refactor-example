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
        self._update_row_price()

    def _update_row_price(self: OR):
        self.row_price = self.item.price * self.quantity

    def increment_quantity(self: OR, amount: int = 1) -> OR:
        self.quantity += amount
        self._update_row_price()
        return self

    def decrement_quantity(self: OR, amount: int = 1) -> OR:
        t = self.quantity - amount
        self.quantity = t if t >= 0 else self.quantity
        self._update_row_price()
        return self


@dataclass
class Order:
    customer_name: str
    order_items: List[OrderRow]
    balance: int = field(init=False)

    def __post_init__(self: O):
        self._update_balance()

    def _update_balance(self: O):
        self.balance = sum([row.row_price for row in self.order_items])
