from dotenv import load_dotenv
from os import getenv


from src.settings.descriptor import SettingsDescriptor


class CloudSettings:

    S3_ACCESS_KEY: SettingsDescriptor = SettingsDescriptor()
    S3_SECRET_KEY: SettingsDescriptor = SettingsDescriptor()
    SELECTEL_URL: SettingsDescriptor = SettingsDescriptor()
    CLOUD_NAME: SettingsDescriptor = SettingsDescriptor()

    def __init__(self) -> None:
        load_dotenv()
        self.S3_ACCESS_KEY: str = getenv("S3_ACCESS_KEY")
        self.S3_SECRET_KEY: str = getenv("S3_SECRET_KEY")
        self.SELECTEL_URL: str = getenv("SELECTEL_URL")
        self.CLOUD_NAME: str = getenv("CLOUD_NAME")

    def __str__(self):
        return str(type(self))
