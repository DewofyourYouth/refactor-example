from dataclasses import dataclass, field
from functools import reduce
from typing import List

from colorama import Fore

from refactor_example import inventory
from refactor_example.utils import format_currency


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
        self.balance = reduce(
            lambda a, b: a + b,
            [row.row_price for row in self.order_items],
        )

    def format_items_to_str(self, row_str: str) -> str:
        row_data = lambda list_item: {
            "name": list_item.item.name,
            "price": format_currency(list_item.item.price),
            "quantity": list_item.quantity,
            "total": format_currency(list_item.row_price),
        }
        format_row = lambda list_item: row_str.format(**row_data(list_item))
        return "".join([format_row(list_item) for list_item in self.order_items])

    def generate_terminal_receipt(self) -> str:
        print_str = [
            "\n" + Fore.CYAN + f"Receipt for \033[1m{self.customer_name}\033[0m"
        ]
        row_str = "{name}:\n\t Price: ${price} * Quantity: {quantity} = ${total}\n"
        print_str.append(
            Fore.YELLOW
            + "===========================================================\n"
        )
        print_str.append(Fore.WHITE + "\033[1mItems:\033[0m")
        print_str.append(
            self.format_items_to_str(row_str)
        )  # Print_sprint_str.append rows
        print_str.append(
            Fore.YELLOW + "---------------------------------------------------------"
        )
        print_str.append(
            Fore.WHITE
            + f"TOTAL BALANCE: {Fore.RED} \033[1m${format_currency(self.balance)}\033[0m\n"
        )
        return "\n".join(print_str)

    def generate_html_receipt(self) -> str:
        title_str = f"<div class='receipt'><h3>Receipt for <strong>{self.customer_name}</strong></h3><hr>"
        rows_str = self.format_items_to_str(
            "<tr><td>{name}</td><td>${price}</td><td>{quantity}</td><td></td>${total}</tr>"
        )

        table_str = (
            f"<table><thead><tr><th>Item Name</th><th>Price</th><th>Quantity</th><th>Total</th></tr><thead><tbody>{rows_str}</tbody></table>"
            if self.order_items
            else ""
        )
        total_str = f"<h4>Total: ${format_currency(self.balance)}</h4></div>\n"

        return f"{title_str}{table_str}{total_str}"
