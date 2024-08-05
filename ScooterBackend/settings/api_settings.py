#System
from dotenv import load_dotenv
import os

#Other
from pydantic_settings import BaseSettings


#Прогружаем .env файл
load_dotenv()


class APISettings(BaseSettings):
    #API host
    api_host: str = os.getenv("API_HOST")

    #API port
    api_port: int = int(os.getenv("API_PORT"))
    
    #API reload
    reload: bool = bool(os.getenv("RELOAD"))