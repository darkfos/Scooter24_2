#Other libraries
import jwt
from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Union

#Local
from src.settings.engine_settings import Settings
from src.api.dto.auth_dto import CreateToken, Tokens, AccessToken
from src.api.authentication.hashing import CryptographyScooter
from src.api.exception.general_exceptions import GeneralExceptions
from src.api.exception.http_user_exception import UserHttpError
from src.database.repository.user_repository import UserRepository
from src.database.repository.admin_repository import AdminRepository
from src.database.models.user import User
from src.database.models.admin import Admin
from src.api.dep.dependencies import IEngineRepository, EngineRepository


class Authentication:

    def __init__(self):
        self.jwt_auth: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

    async def create_tokens(self, token_data: CreateToken, engine: IEngineRepository) -> Tokens:
        """
        Создание токенов для доступа
        :param token_data:
        :return:
        """

        async with engine:
            res_to_find_user: Union[bool, User] = await engine.user_repository.find_user_by_email_and_password(
                email=token_data.email)
            res_to_find_admin: Union[bool, Admin] = await engine.admin_repository.find_admin_by_email_and_password(
                email=token_data.email,
                password=token_data.password
            )

            if res_to_find_user or res_to_find_admin:

                # verify password
                check_password = CryptographyScooter().verify_password(
                    password=token_data.password,
                    hashed_password=res_to_find_user.password_user if res_to_find_user else res_to_find_admin.password_user)

                if check_password:

                    data_for_token: Dict[str, str] = {
                        "email": token_data.email,
                        "password": res_to_find_user.password_user if res_to_find_user else res_to_find_admin.password_user,
                        "id_user": res_to_find_user.id if res_to_find_user else res_to_find_admin.id
                    }

                    data_for_refresh_token: Dict[str, str] = data_for_token.copy()
                    data_for_token.update({"exp": (datetime.utcnow() + timedelta(minutes=Settings.auth_settings.time_work_secret_key))})
                    data_for_refresh_token.update({"exp": (datetime.utcnow() + timedelta(days=Settings.auth_settings.time_work_refresh_secret_key))})


                    jwt_token = jwt.encode(data_for_token, Settings.auth_settings.jwt_secret_key, Settings.auth_settings.algorithm)
                    jwt_refresh_token = jwt.encode(data_for_refresh_token, Settings.auth_settings.jwt_secret_refresh_key, Settings.auth_settings.algorithm)

                    return Tokens(
                        token=jwt_token,
                        refresh_token=jwt_refresh_token
                    )

            await UserHttpError().http_user_not_found()

    async def decode_jwt_token(self, token: str, type_token: str) -> Union[None, Dict[str, str]]:
        """
        Декодирует токен
        :param token:
        :return:
        """

        try:
            match type_token.lower():
                case "access":
                    token_data: Dict[str, str] = jwt.decode(token, Settings.auth_settings.jwt_secret_key, algorithms=Settings.auth_settings.algorithm)
                    return token_data
                case "refresh":
                    token_data: Dict[str, str] = jwt.decode(token, Settings.auth_settings.jwt_secret_refresh_key, algorithms=Settings.auth_settings.algorithm)
                    return token_data
                case _:
                    await UserHttpError().http_user_not_found()
        except jwt.PyJWTError as er:
            await GeneralExceptions().http_auth_error()

    async def update_token(self, refresh_token: str) -> str:
        """
        Обновляет токен
        :param refresh_token:
        :return:
        """

        try:
            token_data: Dict[str, str] = await self.decode_jwt_token(token=refresh_token, type_token="refresh")
            token_data.update({"exp": datetime.utcnow() + timedelta(minutes=Settings.auth_settings.time_work_secret_key)})
            new_access_token: str = jwt.encode(token_data, Settings.auth_settings.jwt_secret_key, Settings.auth_settings.algorithm)
            return new_access_token
        except jwt.PyJWTError as jwterr:
            await GeneralExceptions().http_auth_error()

    async def is_admin(self, session: AsyncSession, email: str, password: str) -> dict:
        """
        Проверка, что данные соответствуют данным какого-либо администратора.
        :param engine:
        :param email:
        :param password:
        """

        hash_password: str = CryptographyScooter().hashed_password(password=password)
        is_admin: Union[Admin, None] = await AdminRepository(session=session).find_admin_by_email_and_password(
            email=email, password=hash_password
        )

        if is_admin:
            
            token_access_data: Dict[Union[str, int], Union[str, int]] = {
                "email": email,
                "password": hash_password,
                "id_admin": is_admin.id
            }
            token_refresh_data: Dict[Union[str, int], Union[str, int]] = {
                "email": email,
                "password": hash_password,
                "is_admin": is_admin.id
            }

            token_access_data.update({"exp": (datetime.now() + timedelta(minutes=Settings.auth_settings.time_work_secret_key))})
            token_refresh_data.update({"exp": (datetime.now() + timedelta(days=Settings.auth_settings.time_work_refresh_secret_key))})

            return Tokens(
                token=jwt.encode(token_access_data, key=Settings.auth_settings.jwt_secret_key, algorithm=Settings.auth_settings.algorithm),
                refresh_token=jwt.encode(token_refresh_data, key=Settings.auth_settings.jwt_secret_refresh_key, algorithm=Settings.auth_settings.algorithm)
            )
        
        session.close()
        
        await UserHttpError().http_user_not_found()
