from enum import Enum
from typing import Final


class TypeBuy(Enum):
    CARD: Final[str] = "Картой"
    CASH: Final[str] = "Наличными"
