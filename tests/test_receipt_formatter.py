from colorama import Fore
from pytest import mark
import pytest
from refactor_example.main import sample_orders
from refactor_example.receipt_formatter import (
    HTMLReceipt,
    TerminalReceipt,
    format_items_to_str,
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


@mark.describe("Test HTMLReceipt class")
class TestHTMLReceipt:
    @mark.it("HTMLReceipt.generate_receipt_str returns the order formatted as HTML")
    def test_generate_html_receipt(self):
        assert (
            HTMLReceipt.generate_receipt_str(joe).strip()
            == "<div class='receipt'><h3>Receipt for <strong>Joe Swanson</strong></h3><hr><table><thead><tr><th>Item Name</th><th>Price</th><th>Quantity</th><th>Total</th></tr><thead><tbody><tr><td>Whole Milk</td><td>$4.16</td><td>2</td><td></td>$8.32</tr><tr><td>White Bread</td><td>$2.50</td><td>1</td><td></td>$2.50</tr><tr><td>American Processed Cheese</td><td>$3.89</td><td>1</td><td></td>$3.89</tr></tbody></table><h4>Total: $14.71</h4></div>"
        )

    @mark.it(
        "HTMLReceipt.generate_receipt_str on an empty order does not contain a table."
    )
    def test_empty_order_html_does_not_contain_table(self):
        html = HTMLReceipt.generate_receipt_str(glenn).strip()
        assert "<table" not in html

    @mark.it("HTMLReceipt.generate_receipt_str on an empty orderis formatted properly.")
    def test_empty_order_html_formatted_properly(self):
        html = HTMLReceipt.generate_receipt_str(glenn).strip()
        assert (
            html
            == "<div class='receipt'><h3>Receipt for <strong>Glenn Quagmire</strong></h3><hr><h4>Total: $0.00</h4></div>".strip()
        )


@mark.describe("Test the TerminalReceipt class")
class TestTerminalReceipt:
    glenn_str = TerminalReceipt.generate_receipt_str(glenn)
    peter_str = TerminalReceipt.generate_receipt_str(peter)

    @mark.it("The receipt title is properly formatted")
    def test_terminal_receipt_title(self):
        assert self.glenn_str.startswith(
            "\n\x1b[36mReceipt for \033[1mGlenn Quagmire\033[0m\n\x1b[33m===========================================================\n"
        )

    @mark.it("The item list is formatted correctly")
    def test_items_list(self):
        row_str = "Beef Choice Angus Ribeye Steak:\n\t Price: $22.70 * Quantity: 2 = $45.40\nLucky Charms:\n\t Price: $12.22 * Quantity: 1 = $12.22\n"
        assert row_str in self.peter_str
