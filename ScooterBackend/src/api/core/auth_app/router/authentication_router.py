import datetime

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
)
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import logging


from src.api.core.auth_app.schemas.auth_dto import (
    CreateToken,
    UpdateUserPassword,
)
from src.api.core.user_app.schemas.user_dto import AddUser
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.user_app.service.user_service import UserService
from src.api.authentication.email_service import EmailService
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix
from src.other.broker.producer.producer import (
    send_message_registration_on_email,
)

auth_router: APIRouter = APIRouter(
    prefix=APIPrefix.AUTH_PREFIX.value, tags=[APITagsEnum.AUTH.value]
)
authentication_app: Authentication = Authentication()
logger = logging.getLogger(__name__)


@auth_router.post(
    path="/login",
    description="""
    ### Endpoint - (Авторизация | Создание токена).
    Данный метод необходим для АВТОРИЗАЦИИ пользователя,
    и получения токенов доступа.
    При успешном выполнении запроса выдаётся 2 токена,
    access token и refresh token.\n\n
    1. Access токен - обычный токен, необходимый для выполнений
    всех дальнейших запросов.
    2. Refresh токен - необходим только для ОБНОВЛЕНИЯ,
    получения нового ACCESS токена.\n\n
    Для корректной обработки необходимо ввести почту и пароль.
    """,
    summary="Авторизация",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
async def login_user(
    data_login: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    response: Response,
) -> None:
    """
    Take user data and create jwt tokens for access
    :param session:
    :return:
    """

    logger.info(
        msg="Auth-Router вызов метода авторизации пользователя (login_user)"
    )

    tokens = await authentication_app.create_tokens(
        token_data=CreateToken(
            email=data_login.username, password=data_login.password
        ),
        engine=session,
    )

    response.set_cookie(
        key="access_key",
        value=tokens.token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 15,
    )

    response.set_cookie(
        key="refresh_key",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24 * 30,
    )


@auth_router.post(
    path="/logout",
    description="""
    Выход пользователя из сессии
    """,
    summary="Выход пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def exit_user(response: Response):
    response.delete_cookie(key="access_key")
    response.delete_cookie(key="refresh_key")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@auth_router.post(
    path="/registration",
    description="""
    ### Endpoint - Регистрация.
    Данный метод необходим для регистрации пользователей.
    Для успешной регистрации необходима почта и пароль.
    """,
    summary="Регистрация",
    status_code=status.HTTP_201_CREATED,
)
async def registration_user(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    new_user: AddUser,
):
    """
    Создание нового пользователя
    :param session:
    :param new_user:
    :return:
    """

    logger.info(
        msg="Auth-Router вызов метода регистрации"
        " пользователя (registration_user)"
    )

    new_user.date_registration = datetime.date.today()

    await UserService.create_a_new_user(
        engine,
        new_user,
        bt=send_message_registration_on_email,
        func_to_bt=EmailService.send_secret_key_for_register,
    )


@auth_router.post(
    path="/update_token",
    description="""
    ### Endpoint - Обновление токена.
    Данный метод необходим для ОБНОВЛЕНИЯ access токена.
    При успешном выполнении запроса выдаётся 2 токена,
    access token (Обновлённый) и refresh token.
    """,
    summary="Обновление токена",
    status_code=status.HTTP_201_CREATED,
)
async def update_by_refresh_token(refresh_token: str) -> dict[str, str]:
    """
    Обновление существующего токена
    :param session:
    :param refresh_token:
    :return:
    """

    logger.info(
        msg="Auth-Router вызов метода "
        "обновления токена (update_by_refresh_token)"
    )

    try:
        data_tokens: str = await authentication_app.update_token(
            refresh_token=refresh_token
        )

        return {"access_token": data_tokens}

    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ключ для обновлений не был найден",
        )


@auth_router.post(
    path="/update/password",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
    ### ENDPOINT - Обновление пароля пользователя
    """,
    summary="Обновление пароля",
)
async def update_user_password(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    data_update: UpdateUserPassword,
) -> None:
    """
    Обновление пароля пользователя
    :param engine:
    :param data_update:
    "param user_data"
    """

    return await UserService.update_user_password(
        engine=engine,
        to_update=data_update,
    )


@auth_router.post(
    path="/access/create",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    description="""
    ### ENDPOINT - Подтверждение регистрации пользователя
    """,
    summary="Подтверждение регистрации пользователя",
)
async def access_user(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    secret_key: str,
    email: str,
) -> None:

    result = await EmailService.access_user_account(
        engine=engine, user_email=email, secret_key=secret_key
    )

    if result:
        return None

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Не удалось подвердить аккаунт",
    )


@auth_router.post(
    path="/access/update/password",
    description="""### ENDPOINT Обновление пароля""",
    summary="Подтверждение изменение пароля пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def access_update_user_password(
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    password_data: UpdateUserPassword,
    secret_key: str,
) -> None:
    return await UserService.access_update_user_password(
        engine=engine, update_data=password_data, secret_key=secret_key
    )


@auth_router.post(
    path="/auth/update/password",
    description="""### ENDPOINT Обновление пароля авторизированного пользователя""", # noqa
    summary="Обновление пароля",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_auth_user_password( # noqa
    auth: Annotated[str, Depends(authentication_app.auth_user)],
    engine: Annotated[IEngineRepository, Depends(EngineRepository)],
    old_password: str,
    new_password: str,
) -> None:
    return await UserService.update_auth_user_password(
        token=auth, engine=engine,
        old_password=old_password, new_password=new_password
    )
