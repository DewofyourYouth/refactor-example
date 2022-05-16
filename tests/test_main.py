import io
from unittest.mock import patch

from pytest import mark
from refactor_example import main
from refactor_example.main import print_header


@patch("sys.stdout", new_callable=io.StringIO)
@mark.it("print header prints a header")
def test_print_header(mock_stdout):
    print_header("SPIDER")
    assert mock_stdout.getvalue().startswith(
        "\n \x1b[34m SPIDER RECEIPTS\n==============="
    )
