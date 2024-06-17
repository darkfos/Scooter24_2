#System
from typing import Annotated
from os import getenv


#Other libraries
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


#Local
...


load_dotenv()


class EmailTransferSettings(BaseSettings):

    email: Annotated[str, getenv("EMAIL")]
    password: Annotated[str, getenv("PASSWORD")]
    secret_symbols: Annotated[str, getenv("SECRET_SYMBOLS")]
    min_length_key: Annotated[str, getenv("MIN_LENGTH_KEY")]