# System
from typing import Union, Coroutine, Any, Dict
import logging

# Other libraries

# Local
from src.api.core.admin_catalog.schemas.admin_dto import *
from src.database.models.admin import Admin
from src.api.authentication.hash_service.hashing import CryptographyScooter
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.api.dep.dependencies import IEngineRepository


auth: Authentication = Authentication()


class AdminService:
    
    @auth
    @staticmethod
    async def create_admin(
        engine: IEngineRepository, new_admin: AdminBase, user_data: str, token_data: dict = dict()
    ):
        """
        Создание нового администратора
        :param session:
        :param new_admin:
        :return:
        """
        
        logging.info(msg=f"{AdminService.__name__} Создание нового администратора")
        token_data["password"] = CryptographyScooter().hashed_password(
            password=token_data.get("password")
        )

        # Hash password
        hash_password: str = CryptographyScooter().hashed_password(
            password=new_admin.password_user
        )
        new_admin.password_user = hash_password

        async with engine:

            # Check admin data
            is_admin: Union[Admin, None] = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email"), password=token_data["password"]
                )
            )

            if is_admin:
                # Create new admin
                res_to_create_admin: Union[None, Admin] = (
                    await engine.admin_repository.add_one(
                        data=Admin(**new_admin.model_dump())
                    )
                )

                return AdminIsCreated(is_created=True if res_to_create_admin else False)
            else:
                logging.critical(msg=f"{AdminService.__name__} Не удалось создать нового администратора")
                await UserHttpError().http_failed_to_create_a_new_user()
