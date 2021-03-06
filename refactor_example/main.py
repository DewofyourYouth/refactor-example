from refactor_example.inventory import BEEF, BREAD, CHEESE, LUCKY_CHARMS, MILK
from refactor_example.orders.order import Order, OrderRow
from refactor_example.orders.output.receipt_formatter import (
    HTMLReceipt,
    ReceiptFormatter,
    TerminalReceipt,
)
from refactor_example.orders.output.utils import TERMINAL_COLORS as color


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


def print_formatted_order(rf: ReceiptFormatter, order: Order) -> None:
    print(rf.generate_receipt_str(order))


def print_header(receipt_type: str) -> None:
    print(f"\n {color.BLUE} {receipt_type} RECEIPTS")
    print(
        f"================================================================================ {color.WHITE}"
    )


def main() -> None:
    print_header("TERMINAL")
    for order in sample_orders():
        print_formatted_order(TerminalReceipt(), order)

    print_header("HTML")
    for order in sample_orders():
        print_formatted_order(HTMLReceipt(), order)


if __name__ == "__main__":
    main()
