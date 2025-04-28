# System
from typing import Union, List
import logging as logger


# Other libraries
from random import choice

# Local
from src.settings.engine_settings import Settings


logging = logger.getLogger(__name__)


class SecretKey:

    def __init__(self, len_password=6):
        self.len_password: int = len_password
        self.symbols: List[Union[int, str]] = [chr(numb) for numb in range(97, 122)]
        self.symbols.extend([chr(numb) for numb in range(65, 91)])

    def generate_password(self) -> str:
        """
        Генерация секретного ключа
        """

        logging.info(
            msg="Генерация пароля для пользователя" " (Система восстановления пароля)"
        )
        size_key: int = Settings.email_tr_settings.min_length_key
        secret_key: str = ""

        while len(secret_key) != size_key:
            secret_key += choice(self.symbols)

        return secret_key
