from types import SimpleNamespace


TERMINAL_COLORS = SimpleNamespace(
    YELLOW="\x1b[33m",
    CYAN="\x1b[36m",
    WHITE="\x1b[37m",
    BLUE="\x1b[34m",
    RED="\x1b[31m",
)


TERMINAL_FORMAT = SimpleNamespace(S_BOLD="\033[1m", E_BOLD="\033[0m")


fmt_currency = lambda price: f"{price/100:.2f}"
