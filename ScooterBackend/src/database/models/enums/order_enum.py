import enum
from typing import Final


class OrderTypeOperationsEnum(enum.Enum):
    IN_PROCESS: Final[str] = (
        "В процессе"  # Купленный товар, в процессе доставки
    )
    CANCEL: Final[str] = "Отменен"
    SUCCESS: Final[str] = "Доставлен"  # Купленный и доставленный товар
