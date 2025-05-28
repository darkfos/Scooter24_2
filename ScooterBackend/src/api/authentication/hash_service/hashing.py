import logging as logger
import bcrypt

logging = logger.getLogger(__name__)


class CryptographyScooter:

    def __init__(self):
        self.algorithm: str = ""

    def hashed_password(self, password: str) -> bytes:
        logging.info(msg="Хеширование пароля")
        hash_password: bytes = bcrypt.hashpw(
            password=password.encode("utf-8"), salt=bcrypt.gensalt()
        )
        return hash_password

    def hashed_img(self, img_name: str) -> bytes:
        logging.info(msg="Хеширование изображения")
        hash_image: bytes = bcrypt.hashpw(
            password=img_name.encode("utf-8"), salt=bcrypt.gensalt()
        )
        return hash_image

    def verify_password(self, password: str, hashed_password: bytes) -> bool:
        logging.info(msg="Верификация пользователя")
        check_password: bool = bcrypt.checkpw(
            password=password.encode("utf-8"), hashed_password=hashed_password
        )
        return check_password
