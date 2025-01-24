# Other libraries
import datetime

from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import logging

from starlette.responses import RedirectResponse

# Local
from src.api.core.auth_catalog.schemas.auth_dto import (
    Tokens,
    CreateToken,
    RefreshUpdateToken,
    AccessToken,
    UpdateUserPassword
)
from src.api.core.user_catalog.schemas.user_dto import AddUser
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.user_catalog.service.user_service import UserService
from src.api.authentication.email_service import EmailService
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.other.enums.api_enum import APITagsEnum, APIPrefix
from src.settings.engine_settings import Settings


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
    response_model=AccessToken,
    status_code=status.HTTP_201_CREATED,
)
async def login_user(
    data_login: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    response: Response,
):
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

    # Set cookie's
    # response.set_cookie(key="access_key", value=tokens.token)
    # response.set_cookie(key="refresh_key", value=tokens.refresh_token)
    # response.set_cookie(key="token_type", value="bearer")

    return AccessToken(
        access_token=tokens.token,
        token_type="bearer",
        refresh_token=tokens.refresh_token,
    )


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
    back_task: BackgroundTasks,
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
        bt=back_task,
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
    response_model=Tokens,
    status_code=status.HTTP_201_CREATED,
)
async def update_by_refresh_token(refresh_token: RefreshUpdateToken) -> Tokens:
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

    data_tokens: str = await authentication_app.update_token(
        refresh_token=refresh_token.refresh_token
    )
    return Tokens(token=data_tokens, refresh_token=refresh_token.refresh_token)


@auth_router.post(
    path="/update_password",
    description="""
    ### ENDPOINT - Для обновления паролей.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Отправка сообщения по почте",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def create_and_send_secret_key(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    background_task: BackgroundTasks,
    user_data: Annotated[str, Depends(authentication_app.jwt_auth)],
) -> None:
    """
    Обновление пароля пользователя
    :user_email:
    """

    logger.info(
        msg="Auth-Router вызов метода создания "
        "секретного ключа (create_and_send_secret_key)"
    )

    token_data: dict = await authentication_app.decode_jwt_token(
        token=user_data, type_token="access"
    )
    return background_task.add_task(
        EmailService.send_secret_key_by_update_password,
        session,
        token_data.get("email"),
        user_data,
    )


@auth_router.patch(
    path="/update_password",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
    ### ENDPOINT - Обновление пароля пользователя
    """,
    summary="Обновление пароля"
)
async def update_user_password(
        engine: Annotated[IEngineRepository, Depends(EngineRepository)],
        data_update: UpdateUserPassword,
        user_data: Annotated[str, Depends(authentication_app.jwt_auth)]
) -> None:
    """
    Обновление пароля пользователя
    :param engine:
    :param data_update:
    "param user_data"
    """

    if await UserService.update_user_password(engine=engine, token=user_data, to_update=data_update):
        pass
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Не удалось обновить пароль пользователя"
        )

@auth_router.get(
    path="/access_create_account",
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
    await EmailService.access_user_account(
        engine=engine, user_email=email, secret_key=secret_key
    )

    return RedirectResponse(
        url=Settings.client_settings.front_url,
        status_code=307
    )
