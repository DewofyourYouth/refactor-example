from enum import Enum
from refactor_example.inventory import BEEF, BREAD, CHEESE, LUCKY_CHARMS, MILK
from refactor_example.order import Order, OrderRow


class ReceiptType(Enum):
    HTML = 1
    TERMINAL = 2


def sample_orders():
    return (
        Order(
            customer_name="Joe Swanson",
            order_items=[
                OrderRow(item=MILK, quantity=2),
                OrderRow(item=BREAD, quantity=1),
                OrderRow(item=CHEESE),
            ],
        ),
        Order(
            customer_name="Peter Griffin",
            order_items=[
                OrderRow(item=BEEF, quantity=2),
                OrderRow(item=LUCKY_CHARMS),
                OrderRow(item=CHEESE, quantity=5),
                OrderRow(item=MILK, quantity=3),
            ],
        ),
        Order(customer_name="Glenn Quagmire", order_items=[]),
    )


def print_receipt(order: Order, receipt_type: ReceiptType) -> None:
    if receipt_type == ReceiptType.HTML:
        print(order.generate_html_receipt())
    elif receipt_type == ReceiptType.TERMINAL:
        print(order.generate_terminal_receipt())


def main():
    for order in sample_orders():
        print_receipt(order, ReceiptType.TERMINAL)
    for order in sample_orders():
        print_receipt(order, ReceiptType.HTML)


if __name__ == "__main__":
    main()
