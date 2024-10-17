from dotenv import load_dotenv
from src.settings.descriptor import SettingsDescriptor
from os import getenv
from typing import Type


class RedisSettings:
    REDIS_HOST: Type[SettingsDescriptor] = SettingsDescriptor()
    REDIS_PORT: Type[SettingsDescriptor] = SettingsDescriptor()

    def __init__(self) -> None:
        load_dotenv()

        self.REDIS_HOST = getenv("REDIS_HOST")
        self.REDIS_PORT = getenv("REDIS_PORT")

    def __str__(self) -> str:
        return str(type(self))
