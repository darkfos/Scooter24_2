from enum import Enum


class AuthenticationEnum(Enum):
    CREATE_TOKEN: str = "create_token"

    DECODE_TOKEN: str = "decode_token"

    UPDATE_TOKEN: str = "update_token"
