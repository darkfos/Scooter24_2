import enum
from typing import Final


class OrderTypeOperationsEnum(enum.Enum):
    IN_PROCESS: Final[str] = "В процессе"
    CANCEL: Final[str] = "Отменен"
    SUCCESS: Final[str] = "Оплачен"
    DELIVERED: Final[str] = "Доставлен"
    NO_BUY: Final[str] = "К оплате"
    RETURNED: Final[str] = "Возвращен"
