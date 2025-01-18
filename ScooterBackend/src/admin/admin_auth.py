from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.responses import Response
from typing import Type, Union

from src.api.authentication.secure.authentication_service import Authentication
from src.database.db_worker import db_work
from src.api.core.auth_catalog.schemas.auth_dto import Tokens


class AdminPanelAuthentication(AuthenticationBackend):

    def __init__(
        self, secret_key: str, auth_service: Type[Authentication] = None
    ) -> None:
        super().__init__(secret_key=secret_key)
        self.auth_service: Type[Authentication] = auth_service

    async def login(self, request: Type[Request]) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate
        jwt_admin_data: Type[Tokens] = await self.auth_service.is_admin(
            session=await db_work.get_session(),
            email=username,
            password=password,
        )

        if jwt_admin_data:
            request.session.update(
                {
                    "access_token": jwt_admin_data.token,
                    "refresh_token": jwt_admin_data.refresh_token,
                    "token_type": jwt_admin_data.token_type,
                }
            )
            return True
        else:
            return False

    async def authenticate(
        self, request: Type[Request]
    ) -> Union[Type[Response], bool]:

        tokens: tuple = request.session.get(
            "access_token"
        ), request.session.get("refresh_token")

        if tokens[-1] not in (None, ""):
            return True
        else:
            return False

    async def logout(self, request: Type[Request]):
        request.session.clear()
        return RedirectResponse(url="http://localhost:8000/admin/login")
