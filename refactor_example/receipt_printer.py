from abc import ABC
from dataclasses import dataclass
from typing import Protocol

from colorama import Fore

from refactor_example.order import Order
from refactor_example.utils import fmt_currency


def format_items_to_str(order: Order, row_str: str) -> str:
    row_data = lambda list_item: {
        "name": list_item.item.name,
        "price": fmt_currency(list_item.item.price),
        "quantity": list_item.quantity,
        "total": fmt_currency(list_item.row_price),
    }
    format_row = lambda list_item: row_str.format(**row_data(list_item))
    return "".join([format_row(list_item) for list_item in order.order_items])


class ReceiptFormatter(Protocol):
    @classmethod
    def generate_receipt_str(cls, order: Order) -> str:
        """Outputs a receipt as a formatted string"""


@dataclass
class HTMLReceipt:
    ROW_STR = (
        "<tr><td>{name}</td><td>${price}</td><td>{quantity}</td><td></td>${total}</tr>"
    )

    @classmethod
    def generate_receipt_str(cls, order: Order) -> str:
        title_str = f"<div class='receipt'><h3>Receipt for <strong>{order.customer_name}</strong></h3><hr>"
        rows_str = format_items_to_str(order, cls.ROW_STR)

        table_str = (
            f"<table><thead><tr><th>Item Name</th><th>Price</th><th>Quantity</th><th>Total</th></tr><thead><tbody>{rows_str}</tbody></table>"
            if order.order_items
            else ""
        )
        total_str = f"<h4>Total: ${fmt_currency(order.balance)}</h4></div>\n"
        return f"{title_str}{table_str}{total_str}"


@dataclass
class TerminalReceipt:
    ROW_STRING = "{name}:\n\t Price: ${price} * Quantity: {quantity} = ${total}\n"

    @classmethod
    def generate_receipt_str(cls, order: Order) -> str:
        print_str = [
            "\n" + Fore.CYAN + f"Receipt for \033[1m{order.customer_name}\033[0m"
        ]
        print_str.append(
            Fore.YELLOW
            + "===========================================================\n"
        )
        print_str.append(Fore.WHITE + "\033[1mItems:\033[0m")
        print_str.append(
            format_items_to_str(order, cls.ROW_STRING)
        )  # Print_sprint_str.append rows
        print_str.append(
            Fore.YELLOW + "---------------------------------------------------------"
        )
        print_str.append(
            Fore.WHITE
            + f"TOTAL BALANCE: {Fore.RED} \033[1m${fmt_currency(order.balance)}\033[0m\n"
        )
        return "\n".join(print_str)
