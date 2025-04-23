from src.settings.descriptor import SettingsDescriptor
from os import getenv
from dotenv import load_dotenv


class BrokerSettings:

    RABBIT_USER: SettingsDescriptor = SettingsDescriptor()
    RABBIT_BROKER_URL: SettingsDescriptor = SettingsDescriptor()
    RABBIT_QUEUE_EMAIL: SettingsDescriptor = SettingsDescriptor()
    RABBIT_QUEUE_HOST: SettingsDescriptor = SettingsDescriptor()
    RABBIT_PASSWORD: SettingsDescriptor = SettingsDescriptor()

    def __init__(self) -> None:
        load_dotenv()
        self.RABBIT_USER: str = getenv("RABBIT_USER")
        self.RABBIT_PASSWORD: str = getenv("RABBIT_PASSWORD")
        self.RABBIT_BROKER_URL: str = (
            f"amqp://{getenv('RABBIT_USER')}:{getenv('RABBIT_PASSWORD')}@localhost:5672/" # noqa
        )
        self.RABBIT_QUEUE_EMAIL: str = getenv("RABBIT_QUEUE_EMAIL")
        self.RABBIT_QUEUE_HOST: str = getenv("RABBIT_QUEUE_HOST")

    def __str__(self) -> str:
        return str(type(self))
