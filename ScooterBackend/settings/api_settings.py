from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    #API host
    api_host: str = "127.0.0.1"
    #API port
    api_port: int = 5678
    #API reload
    reload: bool = True