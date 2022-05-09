from dataclasses import dataclass, field
from functools import reduce
from typing import List

from colorama import Fore

from refactor_example import inventory, utils


@dataclass
class OrderRow:
    item: inventory.InventoryItem
    quantity: int = 1
    row_price: int = field(init=False)

    def __post_init__(self):
        self.row_price = self.item.price * self.quantity


@dataclass
class Order:
    customer_name: str
    order_items: List[OrderRow]
    balance: int = field(init=False)

    def __post_init__(self):
        self.balance = reduce(
            lambda a, b: a + b, [row.row_price for row in self.order_items]
        )


def print_receipt(customer_name: str, item_list=List[OrderRow]) -> None:
    # Extract functions
    get_price = lambda order_item: order_item.item.price * order_item.quantity
    format_row = (
        lambda list_item: f"{list_item.item.name}:\n\t Price: ${utils.format_currency(list_item.item.price)} * Quantity: {list_item.quantity} = ${utils.format_currency(get_price(list_item))}\n"
    )
    get_balance = lambda l: reduce(lambda a, b: a + b, map(get_price, l))

    # Printing
    print(Fore.CYAN + f"Receipt for \033[1m{customer_name}\033[0m")
    print(Fore.YELLOW + "===========================================================")
    print(Fore.WHITE + "\033[1mItems:\033[0m")
    print("".join([format_row(list_item) for list_item in item_list]))  # Print rows
    print(Fore.YELLOW + "---------------------------------------------------------")
    print(
        Fore.WHITE
        + f"TOTAL BALANCE: {Fore.RED} \033[1m${utils.format_currency(get_balance(item_list))}\033[0m\n"
    )


def main():
    print_receipt(
        customer_name="Joe Swanson",
        item_list=[
            OrderRow(item=inventory.MILK, quantity=2),
            OrderRow(item=inventory.BREAD, quantity=1),
            OrderRow(item=inventory.CHEESE),
        ],
    )
    print_receipt(
        customer_name="Peter Griffin",
        item_list=[
            OrderRow(item=inventory.BEEF, quantity=2),
            OrderRow(item=inventory.LUCKY_CHARMS),
            OrderRow(item=inventory.CHEESE, quantity=5),
            OrderRow(item=inventory.MILK, quantity=3),
        ],
    )


if __name__ == "__main__":
    main()
