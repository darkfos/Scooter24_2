from enum import Enum
from typing import Final


class UserTypeEnum(Enum):
    """
    Enum for user type
    """
    USER: Final[int] = 1
    ADMIN: Final[int] = 2
