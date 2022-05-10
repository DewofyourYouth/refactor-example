from refactor_example.main import Order, OrderRow, inventory


def test_order_row_price():
    row0 = OrderRow(item=inventory.MILK, quantity=1)
    row1 = OrderRow(item=inventory.MILK, quantity=3)
    assert row0.row_price == 416
    assert row1.row_price == 1248


order0 = Order(
    customer_name="Peter Griffin",
    order_items=[
        OrderRow(item=inventory.BEEF, quantity=2),
        OrderRow(item=inventory.LUCKY_CHARMS),
        OrderRow(item=inventory.CHEESE, quantity=5),
        OrderRow(item=inventory.MILK, quantity=3),
    ],
)
order1 = Order(
    customer_name="Joe Swanson",
    order_items=[
        OrderRow(item=inventory.MILK, quantity=2),
        OrderRow(item=inventory.BREAD, quantity=1),
        OrderRow(item=inventory.CHEESE),
    ],
)


def test_order_balace():

    assert order0.balance == 8955
    assert order1.balance == 1471


def test_format_item_to_str():
    assert order0.format_items_to_str(
        "{name}:\n\t Price: ${price} * Quantity: {quantity} = ${total}\n"
    ).startswith(
        "Beef Choice Angus Ribeye Steak:\n\t Price: $22.70 * Quantity: 2 = $45.40\n"
    )
