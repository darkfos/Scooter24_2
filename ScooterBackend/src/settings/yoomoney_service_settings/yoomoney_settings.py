import dotenv
from os import getenv
from src.settings.descriptor import SettingsDescriptor


class YoomoneySettings:

    YOUMONEY_ACCESS_TOKEN: SettingsDescriptor = SettingsDescriptor()

    def __init__(self) -> None:

        dotenv.load_dotenv()

        self.YOUMONEY_ACCESS_TOKEN: str = getenv("YOUMONEY_ACCESS_TOKEN")

    def __str__(self):
        return str({"yoomoney_access_token": self.YOUMONEY_ACCESS_TOKEN})