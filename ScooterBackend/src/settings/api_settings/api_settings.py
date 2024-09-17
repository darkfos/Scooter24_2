# System
from typing import Union
from dotenv import load_dotenv
import os

# Local
from src.settings.descriptor import SettingsDescriptor


class APISettings:

    api_host: Union[str, SettingsDescriptor, int] = SettingsDescriptor()
    api_port: Union[str, SettingsDescriptor, int] = SettingsDescriptor()
    reload: Union[str, SettingsDescriptor, int] = SettingsDescriptor()

    def __init__(self) -> None:
        load_dotenv()
        self.api_host = os.getenv("API_HOST")
        self.api_port = os.getenv("API_PORT")
        self.reload = os.getenv("RELOAD")

    def __str__(self) -> str:
        return f"{type(self)}"
