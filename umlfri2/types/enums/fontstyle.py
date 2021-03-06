from enum import Enum, unique


@unique
class FontStyle(Enum):
    italic = 1
    bold = 2
    underline = 3
    strike = 4
