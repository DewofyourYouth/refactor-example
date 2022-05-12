from pytest import mark
from refactor_example import __version__


@mark.it("Check that the version is correct.")
def test_version():
    assert __version__ == "0.1.1"
