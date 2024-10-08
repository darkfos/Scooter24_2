# Other libraries
import jwt
import logging as logger
from datetime import timedelta, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Union, Callable

# Local
from src.settings.engine_settings import Settings
from src.api.core.auth_catalog.schemas.auth_dto import CreateToken, Tokens, AccessToken
from src.api.authentication.hash_service.hashing import CryptographyScooter
from src.api.errors.general_exceptions import GeneralExceptions
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.database.repository.admin_repository import AdminRepository
from src.database.models.user import User
from src.database.models.admin import Admin
from src.api.dep.dependencies import IEngineRepository
from src.other.enums.auth_enum import AuthenticationEnum


logging = logger.getLogger(__name__)


class Authentication:

    def __init__(self):
        self.jwt_auth: OAuth2PasswordBearer = OAuth2PasswordBearer(
            tokenUrl="/api/v1/auth/login"
        )

    async def create_tokens(
        self, token_data: CreateToken, engine: IEngineRepository
    ) -> Tokens:
        """
        Создание токенов для доступа
        :param token_data:
        :return:
        """

        logging.info(msg=f"Сервис Аутентификации - создание токена")

        async with engine:
            res_to_find_user: Union[bool, User] = (
                await engine.user_repository.find_user_by_email_and_password(
                    email=token_data.email
                )
            )
            res_to_find_admin: Union[bool, Admin] = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.email, password=token_data.password
                )
            )

            if res_to_find_user or res_to_find_admin:

                # verify password
                check_password = CryptographyScooter().verify_password(
                    password=token_data.password,
                    hashed_password=(
                        res_to_find_user.password_user
                        if res_to_find_user
                        else res_to_find_admin.password_user
                    ),
                )

                if check_password:

                    data_for_token: Dict[str, str] = {
                        "email": token_data.email,
                        "password": (
                            res_to_find_user.password_user
                            if res_to_find_user
                            else res_to_find_admin.password_user
                        ),
                        "id_user": (
                            res_to_find_user.id
                            if res_to_find_user
                            else res_to_find_admin.id
                        ),
                    }

                    data_for_refresh_token: Dict[str, str] = data_for_token.copy()
                    data_for_token.update(
                        {
                            "exp": (
                                datetime.utcnow()
                                + timedelta(
                                    minutes=Settings.auth_settings.time_work_secret_key
                                )
                            )
                        }
                    )
                    data_for_refresh_token.update(
                        {
                            "exp": (
                                datetime.utcnow()
                                + timedelta(
                                    days=Settings.auth_settings.time_work_refresh_secret_key
                                )
                            )
                        }
                    )

                    jwt_token = jwt.encode(
                        data_for_token,
                        Settings.auth_settings.jwt_secret_key,
                        Settings.auth_settings.algorithm,
                    )
                    jwt_refresh_token = jwt.encode(
                        data_for_refresh_token,
                        Settings.auth_settings.jwt_secret_refresh_key,
                        Settings.auth_settings.algorithm,
                    )

                    return Tokens(token=jwt_token, refresh_token=jwt_refresh_token)
                
            logging.critical(msg=f"Сервис Аутентификации - не удалось создать токен, пользователь не был найден")
            await UserHttpError().http_user_not_found()

    async def decode_jwt_token(
        self, token: str, type_token: str
    ) -> Union[None, Dict[str, str]]:
        """
        Декодирует токен
        :param token:
        :return:
        """

        logging.info(msg=f"Сервис Аутентификации - декодирование токена")
        try:
            match type_token.lower():
                case "access":
                    token_data: Dict[str, str] = jwt.decode(
                        token,
                        Settings.auth_settings.jwt_secret_key,
                        algorithms=Settings.auth_settings.algorithm,
                    )
                    return token_data
                case "refresh":
                    token_data: Dict[str, str] = jwt.decode(
                        token,
                        Settings.auth_settings.jwt_secret_refresh_key,
                        algorithms=Settings.auth_settings.algorithm,
                    )
                    return token_data
                case _:
                    logging.info(msg=f"Сервис Аутентификации - ошибка декодирование токена, не удалось найти пользователя")
                    await UserHttpError().http_user_not_found()
        except jwt.PyJWTError as er:
            logging.exception(msg=f"Сервис Аутентификации - не удалось декодировать токен, ошибка={er}")
            await GeneralExceptions().http_auth_error()

    async def update_token(self, refresh_token: str) -> dict:
        """
        Обновляет токен
        :param refresh_token:
        :return:
        """

        logging.info(msg=f"Сервис Аутентификации - обновление токена")
        try:
            token_data: Dict[str, str] = await self.decode_jwt_token(
                token=refresh_token, type_token="refresh"
            )
            token_data.update(
                {
                    "exp": datetime.utcnow()
                    + timedelta(minutes=Settings.auth_settings.time_work_secret_key)
                }
            )
            new_access_token: str = jwt.encode(
                token_data,
                Settings.auth_settings.jwt_secret_key,
                Settings.auth_settings.algorithm,
            )
            return new_access_token
        except jwt.PyJWTError as jwterr:
            logging.info(msg=f"Сервис Аутентификации - ошибка обновления токена, error={jwterr}")
            await GeneralExceptions().http_auth_error()

    async def is_admin(self, session: AsyncSession, email: str, password: str) -> dict:
        """
        Проверка, что данные соответствуют данным какого-либо администратора.
        :param engine:
        :param email:
        :param password:
        """

        logging.info(msg=f"Сервис Аутентификации - проверка прав пользователя (на администратора), email={email}")
        is_admin: Union[Admin, None] = await AdminRepository(
            session=session
        ).find_admin_by_email_and_password(email=email, password=password)

        if is_admin:
            
            if CryptographyScooter().verify_password(password=password, hashed_password=is_admin.password_user):
                token_access_data: Dict[Union[str, int], Union[str, int]] = {
                    "email": email,
                    "id_admin": is_admin.id,
                }
                token_refresh_data: Dict[Union[str, int], Union[str, int]] = {
                    "email": email,
                    "is_admin": is_admin.id,
                }

                token_access_data.update(
                    {
                        "exp": (
                            datetime.now()
                            + timedelta(minutes=Settings.auth_settings.time_work_secret_key)
                        )
                    }
                )
                token_refresh_data.update(
                    {
                        "exp": (
                            datetime.now()
                            + timedelta(
                                days=Settings.auth_settings.time_work_refresh_secret_key
                            )
                        )
                    }
                )

                return Tokens(
                    token=jwt.encode(
                        token_access_data,
                        key=Settings.auth_settings.jwt_secret_key,
                        algorithm=Settings.auth_settings.algorithm,
                    ),
                    refresh_token=jwt.encode(
                        token_refresh_data,
                        key=Settings.auth_settings.jwt_secret_refresh_key,
                        algorithm=Settings.auth_settings.algorithm,
                    ),
                )

        await session.close()

        logging.critical(msg=f"Сервис Аутентификации - пользователь не прошел проверка на администратора, email={email}")
        await UserHttpError().http_user_not_found()

    def __call__(cls, worker: str):
        def auth_wrapper(func: Callable):
            async def auth_json_wrapper(*args, **kwargs):
                match worker:
                    case AuthenticationEnum.CREATE_TOKEN.value:
                        res = await cls.create_tokens(engine=kwargs["session"], token_data=kwargs["token_data"])
                        return await func(*args, **kwargs, token_data=res)
                    case AuthenticationEnum.DECODE_TOKEN.value:
                        print(kwargs, args)
                        res = await cls.decode_jwt_token(token=kwargs["token"], type_token="access")
                        return await func(*args, **kwargs, token_data=res)
                    case AuthenticationEnum.UPDATE_TOKEN.value:
                        res = await cls.update_token(refresh_token=kwargs["refresh_token"])
                        return await func(*args, **kwargs, new_token=res)
            return auth_json_wrapper
        return auth_wrapper
        
