#Other libraries
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from typing import Annotated

#Local
from api.dto.auth_dto import Tokens, CreateToken, RegistrationUser, RefreshUpdateToken, AccessToken
from api.dto.user_dto import AddUser
from database.db_worker import db_work
from api.authentication.authentication_service import Authentication
from api.service.user_service import UserService
from api.dep.dependencies import IEngineRepository, EngineRepository
from other.data_email_transfer import email_transfer


auth_router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["Auth - Система аутентификации, авторизации, регистрации"]
)
authentication_app: Authentication = Authentication()


@auth_router.post(
    path="/login",
    description="""
    ### Endpoint - (Авторизация | Создание токена).
    Данный метод необходим для АВТОРИЗАЦИИ пользователя, и получения токенов доступа.\n
    При успешном выполнении запроса выдаётся 2 токена, access token и refresh token.\n\n
    1. Access токен - обычный токен, необходимый для выполнений всех дальнейших запросов.
    2. Refresh токен - необходим только для ОБНОВЛЕНИЯ, получения нового ACCESS токена.\n\n
    Для корректной обработки необходимо ввести почту и пароль.
    """,
    summary="Авторизация",
    response_model=AccessToken,
    status_code=status.HTTP_201_CREATED
)
async def login_user(data_login: Annotated[OAuth2PasswordRequestForm, Depends()],
                     session: Annotated[IEngineRepository, Depends(EngineRepository)]):
    """
    Take user data and create jwt tokens for access
    :param session:
    :return:
    """

    tokens = await authentication_app.create_tokens(
        token_data=CreateToken(email=data_login.username, password=data_login.password),
        engine=session
    )
    return AccessToken(access_token=tokens.token, token_type=tokens.token_type, refresh_token=tokens.refresh_token)


@auth_router.post(
    path="/registration",
    description="""
    ### Endpoint - Регистрация.
    Данный метод необходим для регистрации пользователей.
    Для успешной регистрации необходима почта и пароль.
    """,
    summary="Авторизация",
    response_model=RegistrationUser,
    status_code=status.HTTP_201_CREATED
)
async def registration_user(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    new_user: AddUser
) -> RegistrationUser:
    """
    Создание нового пользователя
    :param session:
    :param new_user:
    :return:
    """

    return await UserService.create_a_new_user(engine=session, new_user=new_user)


@auth_router.post(
    path="/update_token",
    description="""
    ### Endpoint - Обновление токена.
    Данный метод необходим для ОБНОВЛЕНИЯ access токена.\n
    При успешном выполнении запроса выдаётся 2 токена, access token (Обновлённый) и refresh token.
    """,
    summary="Обновление токена",
    response_model=Tokens,
    status_code=status.HTTP_201_CREATED
)
async def update_by_refresh_token(
    refresh_token: RefreshUpdateToken
) -> Tokens:
    """
    Обновление существующего токена
    :param session:
    :param refresh_token:
    :return:
    """

    data_tokens: str = await authentication_app.update_token(refresh_token=refresh_token.refresh_token)
    return Tokens(token=data_tokens, refresh_token=refresh_token.refresh_token)


@auth_router.post(
    path="/update_password",
    description="""
    ### ENDPOINT - Для обновления паролей.
    Необходим jwt ключ и Bearer в заголовке запроса.
    """,
    summary="Отправка сообщения по почте",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
async def create_and_send_secret_key(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(authentication_app.jwt_auth)],
    user_email: EmailStr
) -> None:
    """
    Обновление пароля пользователя
    :user_email:
    """

    return await UserService.send_secret_key_by_update_password(engine=session, email=user_email, token=user_data)


@auth_router.post(
    path="/update_password_get_new_password",
    description="""
    ### ENDPOINT - Обновление пароля.
    Необходим jwt ключ и Bearer в заголовке запроса.
    Необходим новый пароль.""",
    summary="Обновление пароля",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_password_with_email(
    session: Annotated[IEngineRepository, Depends(EngineRepository)],
    user_data: Annotated[str, Depends(authentication_app.jwt_auth)],
    secret_key: str,
    new_password: str
) -> None:
    """
    Обновление пароля пользователя
    """

    return await UserService.check_secret_key(
        engine=session,
        secret_key=secret_key,
        token=user_data,
        new_password=new_password
    )