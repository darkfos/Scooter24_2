from src.settings.api_settings.api_settings import APISettings
from src.settings.database_settings.database_settings import DatabaseSettings
from src.settings.auth_settings.authenticate_settings import Authentication
from src.settings.other_settings.email_transfer_settings import (
    EmailTransferSettings,
)
from src.settings.database_settings.redis_settings import RedisSettings
from typing import Type


class Settings:

    api_settings: Type[APISettings] = APISettings()
    database_settings: Type[DatabaseSettings] = DatabaseSettings()
    auth_settings: Type[Authentication] = Authentication()
    email_tr_settings: Type[EmailTransferSettings] = EmailTransferSettings()
    redis_settings: Type[RedisSettings] = RedisSettings()
