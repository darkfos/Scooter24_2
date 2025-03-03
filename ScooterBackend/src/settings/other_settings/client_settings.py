from dotenv import load_dotenv
from typing import Union
from os import getenv
from settings.descriptor import SettingsDescriptor

load_dotenv()


class ClientSettings:
    front_url: Union[str, SettingsDescriptor] = SettingsDescriptor()

    def __init__(self):
        self.front_url = getenv("FRONT_URL_ADDRESS")

    def __str__(self) -> str:
        return f"{type(self)}"
