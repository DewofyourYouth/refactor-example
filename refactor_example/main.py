from prompt_toolkit import HTML

from refactor_example.inventory import BEEF, BREAD, CHEESE, LUCKY_CHARMS, MILK
from refactor_example.order import Order, OrderRow
from refactor_example.receipt_printer import HTMLReceipt, TerminalReceipt


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


def main():
    order0, order1 = sample_orders()
    print(TerminalReceipt.generate_receipt_str(order0))
    print(TerminalReceipt.generate_receipt_str(order1))
    print(HTMLReceipt.generate_receipt_str(order0))
    print(HTMLReceipt.generate_receipt_str(order1))


if __name__ == "__main__":
    main()
