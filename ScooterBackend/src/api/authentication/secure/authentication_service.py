# Other libraries
import jwt
import logging as logger
from datetime import timedelta, datetime

from fastapi import HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Union, Callable, Annotated

from src.database.repository.user_repository import UserRepository

# Local
from src.settings.engine_settings import Settings
from src.api.core.auth_app.schemas.auth_dto import CreateToken, Tokens
from src.other.enums.user_type_enum import UserTypeEnum
from src.api.authentication.hash_service.hashing import CryptographyScooter
from src.api.errors.general_exceptions import GeneralExceptions
from src.api.core.user_app.error.http_user_exception import UserHttpError
from src.database.models.user import User
from src.api.dep.dependencies import IEngineRepository
from src.other.enums.auth_enum import AuthenticationEnum
from src.other.enums.api_enum import APIPrefix


logging = logger.getLogger(__name__)


class Authentication:

    __instance: Union[None, "Authentication"] = None
    jwt_auth: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl=(
            (APIPrefix.API_V_PREFIX.value + APIPrefix.AUTH_PREFIX.value)
            + "/login"  # noqa
        )
    )

    def __new__(cls, *args, **kwargs) -> "Authentication":
        if cls.__instance is None:
            Authentication.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    async def auth_user(self, request: Request, response: Response) -> str:
        """
        Аутентификация пользователя
        :param request:
        """

        try:
            token_data: str = request.headers.get("Authorization").split(" ")[1]

            print(token_data)

            token_access_data: dict[str, str | int] = jwt.decode(  # noqa
                request.headers.get("Authorization").split(" ")[1],
                Settings.auth_settings.jwt_secret_key,
                algorithms=Settings.auth_settings.algorithm,
            )

            return token_data
        except (KeyError, jwt.PyJWTError, jwt.DecodeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Ошибка авторизации",
            )

    async def create_tokens(
        self, token_data: CreateToken, engine: IEngineRepository
    ) -> Tokens:
        """
        Создание токенов для доступа
        :param token_data:
        :return:
        """

        logging.info(msg="Сервис Аутентификации - создание токена")

        async with engine:
            res_to_find_user: Union[bool, User] = (
                await engine.user_repository.find_user_by_email_and_password(
                    email=token_data.email
                )
            )

            if res_to_find_user:

                if res_to_find_user.is_active is False:
                    await UserHttpError().user_no_activated()

                # verify password
                check_password = CryptographyScooter().verify_password(
                    password=token_data.password,
                    hashed_password=res_to_find_user.password_user,
                )

                if check_password:

                    data_for_token: Dict[str, str] = {
                        "is_admin": (
                            True
                            if res_to_find_user.id_type_user == 2
                            else False
                        ),
                        "sub": str(res_to_find_user.id),
                    }

                    data_for_refresh_token: Dict[str, str] = (
                        data_for_token.copy()
                    )
                    data_for_token.update(
                        {
                            "exp": (
                                datetime.utcnow()
                                + timedelta(  # noqa
                                    minutes=Settings.auth_settings.time_work_secret_key  # noqa
                                )
                            )
                        }
                    )
                    data_for_refresh_token.update(
                        {
                            "exp": (
                                datetime.utcnow()
                                + timedelta(  # noqa
                                    days=Settings.auth_settings.time_work_refresh_secret_key  # noqa
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

                    return Tokens(
                        token=jwt_token, refresh_token=jwt_refresh_token
                    )

            logging.critical(
                msg="Сервис Аутентификации - не удалось создать"
                " токен, пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    async def decode_jwt_token(
        self, token: str, type_token: str
    ) -> Union[None, Dict[str, str]]:
        """
        Декодирует токен
        :param token:
        :return:
        """

        logging.info(msg="Сервис Аутентификации - декодирование токена")
        try:
            match type_token.lower():  # fmt: skip
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
                    logging.info(
                        msg="Сервис Аутентификации - ошибка декодирование"
                        " токена, не удалось найти пользователя"
                    )
                    await UserHttpError().http_user_not_found()
        except jwt.PyJWTError as er:
            logging.exception(
                msg=f"Сервис Аутентификации - не удалось"
                f" декодировать токен, ошибка={er}"
            )
            await GeneralExceptions().http_auth_error()

    async def update_token(self, refresh_token: str) -> dict:
        """
        Обновляет токен
        :param refresh_token:
        :return:
        """

        logging.info(msg="Сервис Аутентификации - обновление токена")
        try:
            token_data: Dict[str, str] = await self.decode_jwt_token(
                token=refresh_token, type_token="refresh"
            )
            token_data.update(
                {
                    "exp": datetime.utcnow()
                    + timedelta(  # noqa
                        minutes=Settings.auth_settings.time_work_secret_key  # noqa
                    )
                }
            )
            new_access_token: str = jwt.encode(
                token_data,
                Settings.auth_settings.jwt_secret_key,
                Settings.auth_settings.algorithm,
            )
            return new_access_token
        except jwt.PyJWTError as jwterr:
            logging.info(
                msg=f"Сервис Аутентификации - ошибка"
                f" обновления токена, error={jwterr}"
            )
            await GeneralExceptions().http_auth_error()

    async def is_admin(
        self, session: AsyncSession, email: str, password: str
    ) -> dict:
        """
        Проверка, что данные соответствуют данным какого-либо администратора.
        :param engine:
        :param email:
        :param password:
        """

        logging.info(
            msg=f"Сервис Аутентификации - проверка прав"
            f" пользователя (на администратора), email={email}"
        )
        is_admin: Union[User, None] = await UserRepository(
            session
        ).find_user_by_email_and_password(email=email)

        if is_admin and is_admin.id_type_user == UserTypeEnum.ADMIN.value:

            if CryptographyScooter().verify_password(
                password=password, hashed_password=is_admin.password_user
            ):
                token_access_data: Dict[Union[str, int], Union[str, int]] = {
                    "sub": is_admin.id,
                    "is_admin": True,
                }
                token_refresh_data: Dict[Union[str, int], Union[str, int]] = {
                    "sub": is_admin.id,
                    "is_admin": True,
                }

                token_access_data.update(
                    {
                        "exp": (
                            datetime.now()
                            + timedelta(  # noqa
                                minutes=Settings.auth_settings.time_work_secret_key  # noqa
                            )
                        )
                    }
                )
                token_refresh_data.update(
                    {
                        "exp": (
                            datetime.now()
                            + timedelta(  # noqa
                                days=Settings.auth_settings.time_work_refresh_secret_key  # noqa
                            )
                        )  # noqa
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

        logging.critical(
            msg=f"Сервис Аутентификации - пользователь не "
            f"прошел проверка на администратора, email={email}"
        )
        await UserHttpError().http_user_not_found()

    def __call__(cls, worker: str):
        def auth_wrapper(func: Callable):
            async def auth_json_wrapper(*args, **kwargs):
                match worker:
                    case AuthenticationEnum.CREATE_TOKEN.value:
                        res = await cls.create_tokens(
                            engine=kwargs["session"],
                            token_data=kwargs["token_data"],
                        )
                        return await func(*args, **kwargs, token_data=res)
                    case AuthenticationEnum.DECODE_TOKEN.value:
                        res = await cls.decode_jwt_token(
                            token=kwargs["token"], type_token="access"
                        )
                        return await func(*args, **kwargs, token_data=res)
                    case AuthenticationEnum.UPDATE_TOKEN.value:
                        res = await cls.update_token(
                            refresh_token=kwargs["refresh_token"]
                        )
                        return await func(*args, **kwargs, new_token=res)

            return auth_json_wrapper

        return auth_wrapper
