from enum import Enum
from typing import Final


class UserTypeEnum(Enum):
    USER: Final[int] = 1
    ADMIN: Final[int] = 2
