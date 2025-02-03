from src.settings.api_settings.api_settings import APISettings
from src.settings.database_settings.database_settings import DatabaseSettings
from src.settings.auth_settings.authenticate_settings import Authentication
from src.settings.other_settings.email_transfer_settings import (
    EmailTransferSettings,
)
from src.settings.database_settings.redis_settings import RedisSettings
from src.settings.other_settings.client_settings import ClientSettings
from src.settings.other_settings.cloud_settings import CloudSettings


class Settings:

    api_settings: APISettings = APISettings()
    database_settings: DatabaseSettings = DatabaseSettings()
    auth_settings: Authentication = Authentication()
    email_tr_settings: EmailTransferSettings = EmailTransferSettings()
    redis_settings: RedisSettings = RedisSettings()
    client_settings: ClientSettings = ClientSettings()
    cloud_settings: CloudSettings = CloudSettings()
