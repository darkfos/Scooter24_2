from src.settings.descriptor import SettingsDescriptor
from os import getenv
from dotenv import load_dotenv


class BrokerSettings:

    RABBIT_BROKER_URL: SettingsDescriptor = SettingsDescriptor()

    def __init__(self) -> None:
        load_dotenv()
        self.RABBIT_BROKER_URL: str = f"amqp://{getenv('RABBIT_USER')}:{getenv('RABBIT_PASSWORD')}@localhost:5672/"

    def __str__(self) -> str:
        return str(type(self))