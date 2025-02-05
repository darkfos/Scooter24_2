from enum import Enum
from typing import Final


class S3EnumStorage(Enum):
    PRODUCTS: Final[str] = "products"
    CATEGORY: Final[str] = "category"
    BRANDS: Final[str] = "brands"
