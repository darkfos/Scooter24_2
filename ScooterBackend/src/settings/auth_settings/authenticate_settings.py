# Other libraries
from dotenv import load_dotenv
from typing import Union, Type
import os

# Local
from src.settings.descriptor import SettingsDescriptor


class Authentication:
    """
    Settings for authentication
    """

    jwt_secret_key: Union[str, SettingsDescriptor, int] = SettingsDescriptor()
    jwt_secret_refresh_key: Union[str, SettingsDescriptor, int] = (
        SettingsDescriptor()
    )
    time_work_secret_key: Union[str, SettingsDescriptor, int] = (
        SettingsDescriptor()
    )
    time_work_refresh_secret_key: Union[str, SettingsDescriptor, int] = (
        SettingsDescriptor()
    )
    algorithm: Union[str, Type[SettingsDescriptor], int] = SettingsDescriptor()

    def __init__(self) -> None:
        load_dotenv()
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY")
        self.jwt_secret_refresh_key = os.getenv("JWT_REFRESH_SECRET_KEY")
        self.time_work_secret_key = int(os.getenv("SECRET_TIME_WORK"))
        self.time_work_refresh_secret_key = int(
            os.getenv("REFRESH_SECRET_TIME_WORK")
        )
        self.algorithm = os.getenv("ALGORITHM")

    def __str__(self) -> str:
        return f"{type(self)}"
