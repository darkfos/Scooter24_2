#System
from typing import Union

#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from ScooterBackend.database.repository.admin_repository import AdminRepository
from ScooterBackend.api.dto.admin_dto import *
from ScooterBackend.database.models.admin import Admin
from ScooterBackend.api.authentication.hashing import CryptographyScooter
from ScooterBackend.api.dep.dependencies import IEngineRepository, EngineRepository


class AdminService:

    @staticmethod
    async def create_admin(engine: IEngineRepository, new_admin: AdminBase):
        """
        Создание нового администратора
        :param session:
        :param new_admin:
        :return:
        """

        #Hash password
        hash_password: str = CryptographyScooter().hashed_password(password=new_admin.password_user)
        new_admin.password_user = hash_password

        async with engine:
            #Create new admin
            res_to_create_admin: Union[None, Admin] = await engine.admin_repository.add_one(data=Admin(
                **new_admin.model_dump()
            ))

            return AdminIsCreated(
                is_created=True if res_to_create_admin else False
            )