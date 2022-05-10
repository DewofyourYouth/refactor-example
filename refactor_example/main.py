from dataclasses import dataclass, field
from functools import reduce
from locale import currency
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


row_data = lambda list_item: {
    "name": list_item.item.name,
    "price": utils.format_currency(list_item.item.price),
    "quantity": list_item.quantity,
    "total": utils.format_currency(list_item.price),
}


@dataclass
class Order:
    customer_name: str
    order_items: List[OrderRow]
    balance: int = field(init=False)

    def __post_init__(self):
        self.update_balance()

    def update_balance(self):
        self.balance = reduce(
            lambda a, b: a + b, [row.row_price for row in self.order_items]
        )

    def print_terminal_receipt(self):
        currency = utils.format_currency
        format_row = lambda list_item: "{name}:\n\t Price: ${price} * Quantity: {quantity} = ${total}\n".format(
            name=list_item.item.name,
            price=currency(list_item.item.price),
            quantity=list_item.quantity,
            total=list_item.row_price,
        )
        print(Fore.CYAN + f"Receipt for \033[1m{self.customer_name}\033[0m")
        print(
            Fore.YELLOW + "==========================================================="
        )
        print(Fore.WHITE + "\033[1mItems:\033[0m")
        print(
            "".join([format_row(list_item) for list_item in self.order_items])
        )  # Print rows
        print(Fore.YELLOW + "---------------------------------------------------------")
        print(
            Fore.WHITE
            + f"TOTAL BALANCE: {Fore.RED} \033[1m${utils.format_currency(self.balance)}\033[0m\n"
        )


def main():
    order0 = Order(
        customer_name="Joe Swanson",
        order_items=[
            OrderRow(item=inventory.MILK, quantity=2),
            OrderRow(item=inventory.BREAD, quantity=1),
            OrderRow(item=inventory.CHEESE),
        ],
    )
    order1 = Order(
        customer_name="Peter Griffin",
        order_items=[
            OrderRow(item=inventory.BEEF, quantity=2),
            OrderRow(item=inventory.LUCKY_CHARMS),
            OrderRow(item=inventory.CHEESE, quantity=5),
            OrderRow(item=inventory.MILK, quantity=3),
        ],
    )
    order0.print_terminal_receipt()
    order1.print_terminal_receipt()


if __name__ == "__main__":
    main()
