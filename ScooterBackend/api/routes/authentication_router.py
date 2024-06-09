#Other libraries
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

#Local
from ScooterBackend.api.dto.auth_dto import Tokens, CreateToken, RegistrationUser, RefreshUpdateToken, AccessToken
from ScooterBackend.api.dto.user_dto import AddUser
from ScooterBackend.database.db_worker import db_work
from ScooterBackend.api.authentication.authentication_service import Authentication
from ScooterBackend.api.service.user_service import UserService


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
                     session: Annotated[AsyncSession, Depends(db_work.get_session)]):
    """
    Take user data and create jwt tokens for access
    :param session:
    :return:
    """

    tokens = await authentication_app.create_tokens(
        token_data=CreateToken(email=data_login.username, password=data_login.password),
        session=session
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
        session: Annotated[AsyncSession, Depends(db_work.get_session)],
        new_user: AddUser
) -> RegistrationUser:
    """
    Создание нового пользователя
    :param session:
    :param new_user:
    :return:
    """

    return await UserService.create_a_new_user(session=session, new_user=new_user)


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
        session: Annotated[AsyncSession, Depends(db_work.get_session)],
        refresh_token: RefreshUpdateToken
) -> Tokens:
    """
    Обновление существующего токена
    :param session:
    :param refresh_token:
    :return:
    """

    data_tokens: str =  await authentication_app.update_token(refresh_token=refresh_token.refresh_token)
    return Tokens(token=data_tokens, refresh_token=refresh_token.refresh_token)