#Other libraries
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Authentication(BaseSettings):
    """
    Settings for authentication
    """

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_secret_refresh_key: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    time_work_secret_key: int = int(os.getenv("SECRET_TIME_WORK"))
    time_work_refresh_secret_key: int = int(os.getenv("REFRESH_SECRET_TIME_WORK"))
    algorithm: str = os.getenv("ALGORITHM")


auth = Authentication()