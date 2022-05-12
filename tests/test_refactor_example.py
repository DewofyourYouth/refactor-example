from pytest import mark
from refactor_example import __version__


@mark.it("The version is accurate.")
def test_version():
    assert __version__ == "0.1.2"
