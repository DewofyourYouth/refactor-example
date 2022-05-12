import copy
import json
from dataclasses import dataclass
from typing import Protocol

from refactor_example.orders.order import Order
from refactor_example.orders.output.utils import TERMINAL_COLORS as color
from refactor_example.orders.output.utils import TERMINAL_FORMAT as tf
from refactor_example.orders.output.utils import fmt_currency as fc

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
    def generate_receipt_str(self, order: Order) -> str:
        """Generates a receipts as a formatted string."""


@dataclass
class HTMLReceipt:
    """A ReceiptFormatter for HTML"""

    def generate_receipt_str(self, order: Order) -> str:
        """Returns a receipt in the form of an HTML string"""
        ROW_STR = "<tr><td>{name}</td><td>${price}</td><td>{quantity}</td><td></td>${total}</tr>"
        title_str = f"<div class='receipt'><h3>Receipt for <strong>{order.customer_name}</strong></h3><hr>"
        rows_str = format_items_to_str(order, ROW_STR)

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

    def generate_receipt_str(self, order: Order) -> str:
        """Returns a receipt formatted as a string for a terminal application"""
        print_str = [
            f"\n{color.CYAN}Receipt for {tf.S_BOLD}{order.customer_name}{tf.E_BOLD}"
        ]
        print_str.append(
            f"{color.YELLOW}===========================================================\n"
        )
        print_str.append(f"{color.WHITE}{tf.S_BOLD}Items:{tf.E_BOLD}")
        print_str.append(format_items_to_str(order, self.ROW_STRING))
        print_str.append(
            f"{color.YELLOW}---------------------------------------------------------"
        )
        print_str.append(
            f"{color.WHITE}TOTAL BALANCE: {color.RED} {tf.S_BOLD}${fc(order.balance)}{tf.E_BOLD}\n"
        )
        return "\n".join(print_str)


class JSONAPIReceipt:
    """A ReceiptFormatter for the receipt API"""

    @staticmethod
    def _serialize_order(order: Order) -> dict:
        f = lambda x: float(fc(x))
        json_order_items = [row.__dict__ for row in order.order_items]
        order_clone = copy.deepcopy(order)
        # Serialize all non serializable stuff
        for i, row in enumerate(json_order_items):
            o = order_clone.order_items[i]
            row["item"] = o.item.__dict__
            row["row_price"] = f(o.row_price)
            row["item"]["volume"] = o.item.volume.__dict__
            row["item"]["price"] = f(o.item.price)
        json_order = order.__dict__
        json_order["order_id"] = str(order.order_id)
        json_order["order_items"] = json_order_items
        json_order["balance"] = f(order.balance)
        return json_order

    def generate_receipt_str(self, order: Order) -> str:
        json_order = self._serialize_order(order)
        return json.dumps(json_order)
