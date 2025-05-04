from enum import Enum


class DeliveryMethod(Enum):
    PICKUP: str = "Самовывоз"
    EXPRESS: str = "Экспресс"
    STANDARD: str = "Стандарт"