from pydantic_settings import BaseSettings

# System
import os
from typing import Union, Type
from dotenv import load_dotenv

# Local
from src.settings.descriptor import SettingsDescriptor


class DatabaseSettings:
    """
    Settings for connect to db (PostgreSQL)
    """

    db_user: Union[str, Type[SettingsDescriptor]] = SettingsDescriptor()
    db_password: Union[str, Type[SettingsDescriptor]] = SettingsDescriptor()
    db_host: Union[str, Type[SettingsDescriptor]] = SettingsDescriptor()
    db_port: Union[str, Type[SettingsDescriptor]] = SettingsDescriptor()
    db_name: Union[str, Type[SettingsDescriptor]] = SettingsDescriptor()
    db_url: str = ""

    def __init__(self) -> None:
        load_dotenv()
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.db_url = f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"

    def __str__(self) -> str:
        return f"{type(self)}"
