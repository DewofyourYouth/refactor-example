from refactor_example.inventory import BEEF, BREAD, CHEESE, LUCKY_CHARMS, MILK
from refactor_example.orders.order import Order, OrderRow
from refactor_example.orders.output.receipt_formatter import (
    ReceiptFormatter,
    format_html_receipt,
    format_terminal_reciept,
)
from refactor_example.orders.output.utils import TERMINAL_COLORS as color


def sample_orders():  # pragma: no cover
    return (
        Order(
            order_id="682c52a0-110a-4fc9-9bed-2392c5cab72a",
            customer_name="Joe Swanson",
            order_items=[
                OrderRow(item=MILK, quantity=2),
                OrderRow(item=BREAD, quantity=1),
                OrderRow(item=CHEESE),
            ],
        ),
        Order(
            order_id="09d37df9-48a1-4746-91fb-1bcd125a4ed5",
            customer_name="Peter Griffin",
            order_items=[
                OrderRow(item=BEEF, quantity=2),
                OrderRow(item=LUCKY_CHARMS),
                OrderRow(item=CHEESE, quantity=5),
                OrderRow(item=MILK, quantity=3),
            ],
        ),
        Order(
            order_id="bda60c77-3547-4d05-89b3-801f2eca2548",
            customer_name="Glenn Quagmire",
            order_items=[],
        ),
    )


def print_header(receipt_type: str) -> None:
    print(f"\n {color.BLUE} {receipt_type} RECEIPTS")
    print(
        f"================================================================================ {color.WHITE}"
    )


def main() -> None:  # pragma: no cover
    print_header("TERMINAL")
    for order in sample_orders():
        print(format_terminal_reciept(order))

    print_header("HTML")
    for order in sample_orders():
        print(format_html_receipt(order) + "\n")


if __name__ == "__main__":
    main()
