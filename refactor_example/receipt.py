from dataclasses import dataclass
from operator import inv
from pprint import pprint
from typing import List

import inventory


@dataclass
class OrderRow:
    item: inventory.InventoryItem
    quantity: int = 1


@dataclass
class Receipt:
    customer_name: str
    item_list: List[OrderRow]


RECIEPT_ONE = Receipt(
    customer_name="Joe Swanson",
    item_list=[
        OrderRow(item=inventory.MILK, quantity=2),
        OrderRow(item=inventory.BREAD, quantity=1),
        OrderRow(item=inventory.CHEESE),
    ],
)

RECIEPT_TWO = Receipt(
    customer_name="Peter Griffin",
    item_list=[
        OrderRow(item=inventory.BEEF, quantity=2),
        OrderRow(item=inventory.LUCKY_CHARMS),
        OrderRow(item=inventory.CHEESE, quantity=5),
        OrderRow(item=inventory.MILK, quantity=3),
    ],
)
