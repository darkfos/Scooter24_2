# Other libraries
from passlib.context import CryptContext
import logging as logger

# Local
...


logging = logger.getLogger(__name__)


class CryptographyScooter:

    def __init__(self):
        self.algorithm: str = ""
        self.crypto: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hashed_password(self, password) -> str:
        logging.info(msg="Хеширование пароля")
        hash_password: str = self.crypto.hash(password)
        return hash_password

    def hashed_img(self, img_name) -> str:
        logging.info(msg="Хеширование изображения")
        hash_image: str = self.crypto.hash(img_name)
        return hash_image

    def verify_password(self, password: str, hashed_password: str) -> bool:
        logging.info(msg="Верификация пользователя")
        check_password: bool = self.crypto.verify(secret=password, hash=hashed_password)
        return check_password
