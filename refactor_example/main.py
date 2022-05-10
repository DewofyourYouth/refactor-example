from colorama import Fore  # type: ignore

from refactor_example.inventory import BEEF, BREAD, CHEESE, LUCKY_CHARMS, MILK
from refactor_example.order import Order, OrderRow
from refactor_example.receipt_formatter import (
    HTMLReceipt,
    ReceiptFormatter,
    TerminalReceipt,
)


def sample_orders():
    return Order(
        customer_name="Joe Swanson",
        order_items=[
            OrderRow(item=MILK, quantity=2),
            OrderRow(item=BREAD, quantity=1),
            OrderRow(item=CHEESE),
        ],
    ), Order(
        customer_name="Peter Griffin",
        order_items=[
            OrderRow(item=BEEF, quantity=2),
            OrderRow(item=LUCKY_CHARMS),
            OrderRow(item=CHEESE, quantity=5),
            OrderRow(item=MILK, quantity=3),
        ],
    )


def print_order(receipt_formatter: ReceiptFormatter, order: Order) -> None:
    print(receipt_formatter.generate_receipt_str(order))


def print_header(receipt_type: str):
    print(f"\n {Fore.BLUE} {receipt_type} RECEIPTS")
    print(
        f"================================================================================ {Fore.WHITE}"
    )


def main():
    order0, order1 = sample_orders()
    print_header("TERMINAL")
    print_order(TerminalReceipt, order0)
    print_order(TerminalReceipt, order1)
    print_header("HTML")
    print_order(HTMLReceipt, order0)
    print_order(HTMLReceipt, order1)


if __name__ == "__main__":
    main()
