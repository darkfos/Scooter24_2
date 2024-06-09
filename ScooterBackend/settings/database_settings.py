from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

#Load
load_dotenv()


class DatabaseSettings(BaseSettings):
    """
    Settings for connect to db (PostgreSQL)
    """

    #Database user
    db_user: str = os.getenv("DB_USER")
    #Database password
    db_password: str = os.getenv("DB_PASSWORD")
    #Database host
    db_host: str = os.getenv("DB_HOST")
    #Database port
    db_port: int = int(os.getenv("DB_PORT"))
    #Database name
    db_name: str = os.getenv("DB_NAME")
    #Database url
    db_url: str = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"