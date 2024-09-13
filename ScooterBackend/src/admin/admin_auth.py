from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.responses import Response

from src.api.authentication.authentication_service import Authentication
from src.database.db_worker import db_work
from src.api.dto.auth_dto import Tokens


class AdminPanelAuthentication(AuthenticationBackend):

    def __init__(self, secret_key: str, auth_service: Authentication = None) -> None:
        super().__init__(secret_key=secret_key)
        self.auth_service: Authentication = auth_service
    
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        #Validate
        jwt_admin_data: Tokens = await self.auth_service.is_admin(
            session=await db_work.get_session(),
            email=username,
            password=password
        )

        request.session.update({"access_token": jwt_admin_data.token, "refresh_token": jwt_admin_data.refresh_token, "token_type": jwt_admin_data.token_type})
        return True
        

    async def authenticate(self, request: Request) -> Response | bool:
        tokens: tuple = request.session.get("token"), request.session.get("refresh_token")
        
        if tokens[-1]:
            #Check jwt token and update this as needed
            update_tokens = await self.auth_service.update_token(refresh_token=tokens[-1])
            #request.session.update(update_tokens)
            return True
        return False
    
    async def logout(self, request: Request):
        request.session.clear()
        return RedirectResponse(url="http://localhost:8000/admin/login")