from enum import Enum


class AuthenticationEnum(Enum):
    # For create token
    CREATE_TOKEN: str = "create_token"

    # For decode token
    DECODE_TOKEN: str = "decode_token"

    # For update token
    UPDATE_TOKEN: str = "update_token"
