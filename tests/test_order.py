import pytest
from refactor_example.order import Order, OrderRow, inventory
from refactor_example.main import sample_orders
from pytest import mark

joe, peter, glenn = sample_orders()


@mark.describe("Test OrderRow class methods")
class TestOrderRow:
    @mark.it("OrderRow.row_price is the price of the row.")
    def test_order_row_price(self):
        row0 = OrderRow(item=inventory.MILK, quantity=1)
        row1 = OrderRow(item=inventory.MILK, quantity=3)
        assert row0.row_price == 416
        assert row1.row_price == 1248


@mark.describe("Test Order class methods")
class TestOrder:
    @mark.it("Order.balance is the sum of price of all the rows in the order")
    def test_order_balace(self):
        assert peter.balance == 8955
        assert joe.balance == 1471

    @mark.it(
        "Order.format_items_to_str returns a string with all the items formatted according to the input string"
    )
    def test_format_items_to_str(self):
        assert peter.format_items_to_str(
            "{name}:\n\t Price: ${price} * Quantity: {quantity} = ${total}\n\n"
        ).startswith(
            "Beef Choice Angus Ribeye Steak:\n\t Price: $22.70 * Quantity: 2 = $45.40\n\nLucky Charms"
        )

    @mark.it("Order.for_to_str with an invalid placeholder name returns a KeyError.")
    def test_invalid_str(self):
        with pytest.raises(KeyError, match="item_name"):
            peter.format_items_to_str(
                "{item_name}:\n\t Price: ${price} * Quantity: {quantity} = ${total}\n\n"
            )

    @mark.it("Order.generate_html_receipt return the order formatted as HTML")
    def test_generate_html_receipt(self):
        assert (
            joe.generate_html_receipt().strip()
            == "<div class='receipt'><h3>Receipt for <strong>Joe Swanson</strong></h3><hr><table><thead><tr><th>Item Name</th><th>Price</th><th>Quantity</th><th>Total</th></tr><thead><tbody><tr><td>Whole Milk</td><td>$4.16</td><td>2</td><td></td>$8.32</tr><tr><td>White Bread</td><td>$2.50</td><td>1</td><td></td>$2.50</tr><tr><td>American Processed Cheese</td><td>$3.89</td><td>1</td><td></td>$3.89</tr></tbody></table><h4>Total: $14.71</h4></div>"
        )

    @mark.it("Order.generate_html_receipt on an empty order does not contain a table.")
    def test_empty_order_html_does_not_contain_table(self):
        html = glenn.generate_html_receipt().strip()
        assert "<table" not in html

    @mark.it("Order.generate_html_receipt on an empty orderis formatted properly.")
    def test_empty_order_html_formatted_properly(self):
        html = glenn.generate_html_receipt().strip()
        assert (
            html
            == "<div class='receipt'><h3>Receipt for <strong>Glenn Quagmire</strong></h3><hr><h4>Total: $0.00</h4></div>".strip()
        )
