from pytest import mark
from refactor_example.inventory import MILK
from refactor_example.main import sample_orders
from refactor_example.orders.order import Order, OrderRow
from refactor_example.orders.output.receipt_formatter import (
    format_api_receipt,
    format_html_receipt,
    format_terminal_reciept,
)

joe, peter, glenn = sample_orders()


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

    @mark.it("The callable terminal formatter works")
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

    @mark.it("format_terminal_receipt on an empty order is formatted properly.")
    def test_format_terminal_receipt_on_empty_order(self):
        t = format_terminal_reciept(glenn)
        assert "Order bda60c77-3547-4d05-89b3-801f2eca2548 has no items." in t
        assert "Items" not in t
