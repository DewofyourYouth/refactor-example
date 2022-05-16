from pydoc import describe
from uuid import UUID

import pytest
from pytest import mark
from refactor_example.inventory import MILK
from refactor_example.main import sample_orders
from refactor_example.orders.order import Order, OrderRow
from refactor_example.orders.output.receipt_formatter import (
    HTMLReceipt,
    JSONAPIReceipt,
    TerminalReceipt,
    format_api_receipt,
    format_html_receipt,
    format_items_to_str,
    format_terminal_reciept,
)

joe, peter, glenn = sample_orders()


@mark.describe("Test the format_items_to_str function")
class TestFormatItemsToStr:
    @mark.it(
        "format_items_to_str returns a string with all the items formatted according to the input string"
    )
    def test_format_item_to_str(self):
        assert format_items_to_str(
            peter,
            "{name}:\n\t Price: ${price} * Quantity: {quantity} = ${total}\n\n",
        ).startswith(
            "Beef Choice Angus Ribeye Steak:\n\t Price: $22.70 * Quantity: 2 = $45.40\n\nLucky Charms"
        )

    @mark.it("Order.for_to_str with an invalid placeholder name returns a KeyError.")
    def test_invalid_str(self):
        with pytest.raises(KeyError, match="item_name"):
            format_items_to_str(
                peter,
                "{item_name}:\n\t Price: ${price} * Quantity: {quantity} = ${total}\n\n",
            )


@mark.describe("Test HTML Receipt class")
class TestHTMLReceipt:
    hr = HTMLReceipt()

    @mark.it("HTMLReceipt.generate_receipt_str returns the order formatted as HTML")
    def test_generate_html_receipt(self):
        assert (
            self.hr.generate_receipt_str(joe).strip()
            == "<div class='receipt'><h3>Receipt for <strong>Joe Swanson</strong></h3><hr><table><thead><tr><th>Item Name</th><th>Price</th><th>Quantity</th><th>Total</th></tr><thead><tbody><tr><td>Whole Milk</td><td>$4.16</td><td>2</td><td></td>$8.32</tr><tr><td>White Bread</td><td>$2.50</td><td>1</td><td></td>$2.50</tr><tr><td>American Processed Cheese</td><td>$3.89</td><td>1</td><td></td>$3.89</tr></tbody></table><h4>Total: $14.71</h4></div>"
        )

    @mark.it(
        "HTMLReceipt.generate_receipt_str on an empty order does not contain a table."
    )
    def test_empty_order_html_does_not_contain_table(self):
        html = self.hr.generate_receipt_str(glenn).strip()
        assert "<table" not in html

    @mark.it(
        "HTML Receipt.generate_receipt_str on an empty orderis formatted properly."
    )
    def test_empty_order_html_formatted_properly(self):
        html = self.hr.generate_receipt_str(glenn).strip()
        assert (
            html
            == "<div class='receipt'><h3>Receipt for <strong>Glenn Quagmire</strong></h3><hr><h4>Total: $0.00</h4></div>".strip()
        )


@mark.describe("Test the Terminal Receipt class")
class TestTerminalReceipt:
    tr = TerminalReceipt()
    glenn_str = tr.generate_receipt_str(order=glenn)
    peter_str = tr.generate_receipt_str(peter)

    @mark.it("The receipt title is properly formatted")
    def test_terminal_receipt_title(self):
        assert self.glenn_str.startswith(
            "\n\x1b[36mReceipt for \033[1mGlenn Quagmire\033[0m\n\x1b[33m===========================================================\n"
        )

    @mark.it("The item list is formatted correctly")
    def test_items_list(self):
        row_str = "Beef Choice Angus Ribeye Steak:\n\t Price: $22.70 * Quantity: 2 = $45.40\nLucky Charms:\n\t Price: $12.22 * Quantity: 1 = $12.22\n"
        assert row_str in self.peter_str


@mark.describe("Test API Receipt class")
class TestAPIReceipt:
    jr = JSONAPIReceipt()

    @mark.it("Serialize order takes an order and returns a JSON serializable dict")
    def test_serialize_order(self):
        order0 = Order(
            order_id=UUID("9f4c1013-a793-42ba-89a3-dacf2b52fdb0"),
            customer_name="Jerry Falwell",
            order_items=[OrderRow(MILK, 1)],
        )
        assert MILK.price == 416
        assert self.jr._serialize_order(order0) == {
            "order_id": "9f4c1013-a793-42ba-89a3-dacf2b52fdb0",
            "customer_name": "Jerry Falwell",
            "order_items": [
                {
                    "item": {
                        "item_id": "fe865a93-cdee-4d6d-9716-97d2afdf7b7c",
                        "name": "Whole Milk",
                        "price": 4.16,
                        "category": "Dairy",
                        "volume": {"unit": "Gallon", "amount": 1},
                    },
                    "quantity": 1,
                    "row_price": 4.16,
                }
            ],
            "balance": 4.16,
        }

    @mark.it("APIReceipt.generate_receipt_str returns a JSON serialized string")
    def test_api_receipt_returns_json(self):
        order0 = Order(
            order_id=UUID("9f4c1013-a793-42ba-89a3-dacf2b52fdb0"),
            customer_name="Jerry Falwell",
            order_items=[OrderRow(MILK, 1)],
        )
        assert (
            self.jr.generate_receipt_str(order0)
            == '{"order_id": "9f4c1013-a793-42ba-89a3-dacf2b52fdb0", "customer_name": "Jerry Falwell", "order_items": [{"item": {"item_id": "fe865a93-cdee-4d6d-9716-97d2afdf7b7c", "name": "Whole Milk", "price": 4.16, "category": "Dairy", "volume": {"unit": "Gallon", "amount": 1}}, "quantity": 1, "row_price": 4.16}], "balance": 4.16}'
        )


@mark.describe("Tests for callable receipt formatters")
class TestCallableReceiptFormatters:
    @mark.it("The callable API formatter works")
    def test_callable_api_formatter(self):
        order0 = Order(
            order_id="9f4c1013-a793-42ba-89a3-dacf2b52fdb0",
            customer_name="Jerry Falwell",
            order_items=[OrderRow(MILK, 1)],
        )
        assert format_api_receipt(order0) == {
            "order_id": "9f4c1013-a793-42ba-89a3-dacf2b52fdb0",
            "customer_name": "Jerry Falwell",
            "order_items": [
                {
                    "item": {
                        "item_id": "fe865a93-cdee-4d6d-9716-97d2afdf7b7c",
                        "name": "Whole Milk",
                        "price": 4.16,
                        "category": "Dairy",
                        "volume": {"unit": "Gallon", "amount": 1},
                    },
                    "quantity": 1,
                    "row_price": 4.16,
                }
            ],
            "balance": 4.16,
        }

    @mark.it("The callable HTML formatter works")
    def test_callable_html_formatter(self):
        assert (
            format_html_receipt(joe)
            == "<div class='receipt'><h3>Receipt for <strong>Joe Swanson</strong></h3><hr><table><thead><tr><th>Item Name</th><th>Price</th><th>Quantity</th><th>Total</th></tr><thead><tbody><tr><td>Whole Milk</td><td>$4.16</td><td>2</td><td></td>$8.32</tr><tr><td>White Bread</td><td>$2.50</td><td>1</td><td></td>$2.50</tr><tr><td>American Processed Cheese</td><td>$3.89</td><td>1</td><td></td>$3.89</tr></tbody></table><h4>Total: $14.71</h4></div>"
        )

    @mark.it("THe callable terminal formatter works")
    def test_callable_terminal_formatter(self):
        assert format_terminal_reciept(glenn).startswith(
            "\n\x1b[36mReceipt for \033[1mGlenn Quagmire\033[0m\n\x1b[33m===========================================================\n"
        )

    @mark.it("format_html_receipt on an empty order does not contain a table.")
    def test_empty_order_html_does_not_contain_table(self):
        html = format_html_receipt(glenn).strip()
        assert "<table" not in html

    @mark.it("format_html_receipt on an empty order is formatted properly.")
    def test_empty_order_html_formatted_properly(self):
        html = format_html_receipt(glenn).strip()
        assert (
            html
            == "<div class='receipt'><h3>Receipt for <strong>Glenn Quagmire</strong></h3><hr><h4>Total: $0.00</h4></div>".strip()
        )
