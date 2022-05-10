from refactor_example.order import Order, OrderRow, inventory


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


def test_generate_html_receipt():
    assert (
        order1.generate_html_receipt()
        == "<div class='receipt'><h3>Receipt for <strong>Joe Swanson</strong></h3><hr><table><thead><tr><th>Item Name</th><th>Price</th><th>Quantity</th><th>Total</th></tr><thead><tbody><tr><td>Whole Milk</td><td>$4.16</td><td>2</td><td></td>$8.32</tr><tr><td>White Bread</td><td>$2.50</td><td>1</td><td></td>$2.50</tr><tr><td>American Processed Cheese</td><td>$3.89</td><td>1</td><td></td>$3.89</tr></tbody></table><h4>Total: $14.71</h4></div>"
    )
