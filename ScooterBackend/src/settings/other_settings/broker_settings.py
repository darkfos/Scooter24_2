from settings.descriptor import SettingsDescriptor
from os import getenv
from dotenv import load_dotenv


class BrokerSettings:

    RABBIT_BROKER_URL: SettingsDescriptor = SettingsDescriptor()
    RABBIT_QUEUE_EMAIL: SettingsDescriptor = SettingsDescriptor()

    def __init__(self) -> None:
        load_dotenv()
        self.RABBIT_BROKER_URL: str = f"amqp://{getenv('RABBIT_USER')}:{getenv('RABBIT_PASSWORD')}@localhost:5672/"
        self.RABBIT_QUEUE_EMAIL: str = getenv("RABBIT_QUEUE_EMAIL")

    def __str__(self) -> str:
        return str(type(self))