from enum import Enum
from typing import Final


class FilteredDescProduct(Enum):
    NOT_DESC: Final[str] = "asc"
    DEFAULT: Final[str] = "default"
    DESC: Final[str] = "desc"
