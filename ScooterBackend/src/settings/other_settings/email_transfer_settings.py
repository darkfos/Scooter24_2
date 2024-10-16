# System
import os
from typing import Union, Type
from dotenv import load_dotenv

# Local
from src.settings.descriptor import SettingsDescriptor


class EmailTransferSettings:

    email: Union[str, Type[SettingsDescriptor]] = SettingsDescriptor()
    password: Union[str, Type[SettingsDescriptor]] = SettingsDescriptor()
    secret_symbols: Union[str, Type[SettingsDescriptor]] = SettingsDescriptor()
    min_length_key: Union[
        str,
        Type[SettingsDescriptor],
        int
    ] = SettingsDescriptor()

    def __init__(self) -> None:
        load_dotenv()
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.secret_symbols = os.getenv("SECRET_SYMBOLS")
        self.min_length_key = int(os.getenv("MIN_LENGTH_KEY"))

    def __str__(self) -> str:
        return f"{type(self)}"
