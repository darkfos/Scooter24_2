#System
from typing import Union, List


#Other libraries
from random import choice, randint


#Local
from settings.engine_settings import Settings


class SecretKey:

    def __init__(self, len_password = 80):
        self.len_password: int = len_password
        self.symbols: List[Union[int, str]] = [chr(numb) for numb in range(97, 126)]
        self.symbols.extend([chr(numb) for numb in range(65, 91)])
        self.symbols.extend(Settings.email_tr_settings.secret_symbols)

    def generate_password(self) -> str:
        """
        Генерация секретного ключа
        """

        size_key: int = randint(int(Settings.email_tr_settings.min_length_key), self.len_password)
        secret_key: str = ""

        while len(secret_key) != size_key:
            secret_key += choice(self.symbols)

        return secret_key