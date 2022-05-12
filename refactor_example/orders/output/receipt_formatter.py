from dataclasses import dataclass
from typing import Protocol

from refactor_example.orders.output.utils import (
    TERMINAL_COLORS as color,
    TERMINAL_FORMAT as tf,
    fmt_currency as fc,
)

from refactor_example.orders.order import Order


# This pattern is overkill here, but is useful for more complex branching logic


def format_items_to_str(order: Order, row_str: str) -> str:
    row_data = lambda list_item: {
        "name": list_item.item.name,
        "price": fc(list_item.item.price),
        "quantity": list_item.quantity,
        "total": fc(list_item.row_price),
    }
    format_row = lambda list_item: row_str.format(**row_data(list_item))
    return "".join([format_row(list_item) for list_item in order.order_items])


class ReceiptFormatter(Protocol):
    @classmethod
    def generate_receipt_str(cls, order: Order) -> str:
        """Outputs a receipt as a formatted string"""


@dataclass
class HTMLReceipt:
    """A ReceiptFormatter for HTML"""

    ROW_STR = (
        "<tr><td>{name}</td><td>${price}</td><td>{quantity}</td><td></td>${total}</tr>"
    )

    @classmethod
    def generate_receipt_str(cls, order: Order) -> str:
        """Returns a receipt in the form of an HTML string"""
        title_str = f"<div class='receipt'><h3>Receipt for <strong>{order.customer_name}</strong></h3><hr>"
        rows_str = format_items_to_str(order, cls.ROW_STR)

        table_str = (
            f"<table><thead><tr><th>Item Name</th><th>Price</th><th>Quantity</th><th>Total</th></tr><thead><tbody>{rows_str}</tbody></table>"
            if order.order_items
            else ""
        )
        total_str = f"<h4>Total: ${fc(order.balance)}</h4></div>\n"
        return f"{title_str}{table_str}{total_str}"


@dataclass
class TerminalReceipt:
    """A ReceiptFormatter for a command line interface"""

    ROW_STRING = "{name}:\n\t Price: ${price} * Quantity: {quantity} = ${total}\n"

    @classmethod
    def generate_receipt_str(cls, order: Order) -> str:
        """Returns a receipt formatted as a string for a terminal application"""
        print_str = [
            f"\n{color.CYAN}Receipt for {tf.S_BOLD}{order.customer_name}{tf.E_BOLD}"
        ]
        print_str.append(
            f"{color.YELLOW}===========================================================\n"
        )
        print_str.append(f"{color.WHITE}{tf.S_BOLD}Items:{tf.E_BOLD}")
        print_str.append(format_items_to_str(order, cls.ROW_STRING))
        print_str.append(
            f"{color.YELLOW}---------------------------------------------------------"
        )
        print_str.append(
            f"{color.WHITE}TOTAL BALANCE: {color.RED} {tf.S_BOLD}${fc(order.balance)}{tf.E_BOLD}\n"
        )
        return "\n".join(print_str)
