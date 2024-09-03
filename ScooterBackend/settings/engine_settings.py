from settings.api_settings import APISettings
from typing import Type

class Settings:
    api_settings: Type[APISettings] = APISettings()