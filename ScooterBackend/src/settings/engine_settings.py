from src.settings.api_settings import APISettings
from src.settings.database_settings import DatabaseSettings
from src.settings.authenticate_settings import Authentication
from src.settings.email_transfer_settings import EmailTransferSettings
from typing import Type, Union, ClassVar


class Settings:

    api_settings: Type[APISettings] = APISettings()
    database_settings: Type[DatabaseSettings] = DatabaseSettings()
    auth_settings: Type[Authentication] = Authentication()
    email_tr_settings: Type[EmailTransferSettings] = EmailTransferSettings()
