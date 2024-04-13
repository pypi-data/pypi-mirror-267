"""Module representing the ansi_colors enum"""

# Standard Libraries
from enum import StrEnum


class AnsiColors(StrEnum):
    """Used for accessing a list of colo customization for writing in the terminal"""

    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BLACK_BACKGROUND = "\033[40m"
    RED_BACKGROUND = "\033[41m"
    GREEN_BACKGROUND = "\033[42m"
    YELLOW_BACKGROUND = "\033[43m"
    BLUE_BACKGROUND = "\033[44m"
    PURPLE_BACKGROUND = "\033[45m"
    CYAN_BACKGROUND = "\033[46m"
    WHITE_BACKGROUND = "\033[47m"
    CLEAR = "\033[H\033[2J"
