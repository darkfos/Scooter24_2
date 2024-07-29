#Other libraries
from passlib.context import CryptContext

#Local
from settings.authenticate_settings import auth


class CryptographyScooter:

    def __init__(self):
        self.algorithm: str = ""
        self.crypto: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hashed_password(self, password) -> str:
        hash_password = self.crypto.hash(password)
        return hash_password

    def verify_password(self, password: str, hashed_password: str) -> bool:
        check_password = self.crypto.verify(secret=password, hash=hashed_password)
        return check_password