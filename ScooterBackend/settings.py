from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


#Load
load_dotenv()


class DatabaseSettings(BaseSettings):
    """
    Settings for connect to db (PostgreSQL)
    """

    #Database user
    db_user: str = Field(validation_alias="DB_USER")

    #Database password
    db_password: str = Field(alias="DB_PASSWORD")

    #Database host
    db_host: str = Field(alias="DB_HOST")

    #Database port
    db_port: str = Field(alias="DB_PORT")

    #Database name
    db_name: str = Field(alias="DB_NAME")

    #Database url
    db_url: str = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


class APISettings(BaseSettings):

    #API host
    api_host: str = "127.0.0.1"

    #API port
    api_port: int = 8090

    #API reload
    reload: bool = True