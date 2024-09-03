from settings.api_settings import APISettings
from settings.database_settings import DatabaseSettings
from settings.authenticate_settings import Authentication
from settings.email_transfer_settings import EmailTransferSettings
from typing import Type, Union, ClassVar


class Settings:

    api_settings: Type[APISettings] = APISettings()
    database_settings: Type[DatabaseSettings] = DatabaseSettings()
    auth_settings: Type[Authentication] = Authentication()
    email_tr_settings: Type[EmailTransferSettings] = EmailTransferSettings()