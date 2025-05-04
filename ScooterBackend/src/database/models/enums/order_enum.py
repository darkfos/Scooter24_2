import enum
from typing import Final


class OrderTypeOperationsEnum(enum.Enum):
    IN_PROCESS: Final[str] = (
        "В процессе"  # Купленный товар, в процессе доставки
    )
    CANCEL: Final[str] = "Отменен"  # Отмененный к покупке товар
    SUCCESS: Final[str] = "Оплачен"  # Купленный товар
    DELIVERED: Final[str] = "Доставлен"
    NO_BUY: Final[str] = "К оплате"  # Ещё не купленный товар
    RETURNED: Final[str] = "Возвращен"  # Возврат
