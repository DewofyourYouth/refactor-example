import copy
from typing import Protocol

from refactor_example.orders.order import Order
from refactor_example.orders.output.utils import TERMINAL_COLORS as color
from refactor_example.orders.output.utils import TERMINAL_FORMAT as tf
from refactor_example.orders.output.utils import fmt_currency as fc


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
    def __call__(self, order: Order) -> str | dict:
        """Outputs a receipt as a formatted string"""


def format_api_receipt(order: Order) -> dict:
    format_to_float = lambda x: float(fc(x))
    json_order_items = [row.__dict__ for row in order.order_items]
    order_clone = copy.deepcopy(order)
    # Serialize all non serializable stuff
    for i, row in enumerate(json_order_items):
        o = order_clone.order_items[i]
        row["item"] = o.item.__dict__
        row["row_price"] = format_to_float(o.row_price)
        row["item"]["volume"] = o.item.volume.__dict__
        row["item"]["price"] = format_to_float(o.item.price)
    json_order = order.__dict__
    json_order["order_id"] = str(order.order_id)  # this is not needed
    json_order["order_items"] = json_order_items
    json_order["balance"] = format_to_float(order.balance)
    return json_order


def format_html_receipt(order: Order) -> str:
    row_str = (
        "<tr><td>{name}</td><td>${price}</td><td>{quantity}</td><td></td>${total}</tr>"
    )
    title_str = f"<div class='receipt'><h3>Receipt for <strong>{order.customer_name}</strong></h3><hr>"
    rows_str = format_items_to_str(order, row_str)

    table_str = (
        f"<table><thead><tr><th>Item Name</th><th>Price</th><th>Quantity</th><th>Total</th></tr><thead><tbody>{rows_str}</tbody></table>"
        if order.order_items
        else ""
    )
    total_str = f"<h4>Total: ${fc(order.balance)}</h4></div>"
    return f"{title_str}{table_str}{total_str}"


def format_terminal_reciept(order: Order) -> str:
    row_str = "{name}:\n\t Price: ${price} * Quantity: {quantity} = ${total}\n"

    table = (
        f"{color.WHITE}{tf.S_BOLD}Items:{tf.E_BOLD} {format_items_to_str(order, row_str)}"
        if len(order.order_items) > 0
        else f"Order {order.order_id} has no items.\n"
    )
    return (
        f"\n{color.CYAN}Receipt for {tf.S_BOLD}{order.customer_name}{tf.E_BOLD}\n"
        + f"{color.YELLOW}===========================================================\n"
        + table
        + f"{color.YELLOW}---------------------------------------------------------\n"
        + f"{color.WHITE}TOTAL BALANCE: {color.RED} {tf.S_BOLD}${fc(order.balance)}{tf.E_BOLD}\n"
    )
