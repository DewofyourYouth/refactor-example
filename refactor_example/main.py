from refactor_example.inventory import BEEF, BREAD, CHEESE, LUCKY_CHARMS, MILK
from refactor_example.order import Order, OrderRow


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
    print(order0.generate_terminal_receipt())
    print(order1.generate_terminal_receipt())
    print(order0.generate_html_receipt())


if __name__ == "__main__":
    main()
