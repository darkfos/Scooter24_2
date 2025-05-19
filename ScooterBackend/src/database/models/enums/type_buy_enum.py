from enum import Enum
from typing import Final


class TypeBuy(Enum):
    NO_BUY: Final[str] = "не куплен"
    BUY: Final[str] = "куплен"