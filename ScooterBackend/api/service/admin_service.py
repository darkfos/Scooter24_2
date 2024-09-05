#System
from typing import Union

#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from database.repository.admin_repository import AdminRepository
from api.dto.admin_dto import *
from database.models.admin import Admin
from api.authentication.hashing import CryptographyScooter
from api.authentication.authentication_service import Authentication
from api.exception.http_user_exception import UserHttpError
from api.dep.dependencies import IEngineRepository, EngineRepository


class AdminService:

    @staticmethod
    async def create_admin(engine: IEngineRepository, new_admin: AdminBase, user_data: str):
        """
        Создание нового администратора
        :param session:
        :param new_admin:
        :return:
        """

        #Decode token
        token_data = await Authentication().decode_jwt_token(token=user_data, type_token="access")
        token_data["password"] = CryptographyScooter().hashed_password(password=token_data.get("password"))

        #Hash password
        hash_password: str = CryptographyScooter().hashed_password(password=new_admin.password_user)
        new_admin.password_user = hash_password

        async with engine:
            
            #Check admin data
            is_admin: Union[Admin, None] = await engine.admin_repository.find_admin_by_email_and_password(email=token_data.get("email"), password=token_data["password"])

            if is_admin:
                #Create new admin
                res_to_create_admin: Union[None, Admin] = await engine.admin_repository.add_one(data=Admin(
                    **new_admin.model_dump()
                ))

                return AdminIsCreated(
                    is_created=True if res_to_create_admin else False
                )
            else:
                await UserHttpError().http_failed_to_create_a_new_user()