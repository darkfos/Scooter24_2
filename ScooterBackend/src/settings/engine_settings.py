from settings.api_settings.api_settings import APISettings
from settings.database_settings.database_settings import DatabaseSettings
from settings.auth_settings.authenticate_settings import Authentication
from settings.other_settings.email_transfer_settings import (
    EmailTransferSettings,
)
from settings.database_settings.redis_settings import RedisSettings
from settings.other_settings.client_settings import ClientSettings
from settings.other_settings.cloud_settings import CloudSettings
from settings.other_settings.broker_settings import BrokerSettings


class Settings:

    api_settings: APISettings = APISettings()
    database_settings: DatabaseSettings = DatabaseSettings()
    auth_settings: Authentication = Authentication()
    email_tr_settings: EmailTransferSettings = EmailTransferSettings()
    redis_settings: RedisSettings = RedisSettings()
    client_settings: ClientSettings = ClientSettings()
    cloud_settings: CloudSettings = CloudSettings()
    broker_settings: BrokerSettings = BrokerSettings()
