from src.database.repository.user_type_repository import UserTypeRepository, UserType
from src.api.core.user_type_catalog.error.user_type_error import UserTypeException
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.api.core.user_type_catalog.schemas.user_type_dto import UserTypeBase, NewUserType, AllUserType
from src.api.authentication.secure.authentication_service import Authentication, AuthenticationEnum
from src.api.dep.dependencies import IEngineRepository
from typing import Union, List

auth: Authentication = Authentication()

class UserTypeService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_user_type(engine: IEngineRepository, token: str, new_user_type: NewUserType, token_data: dict = {}) -> None:
        """
        Метод сервиса UserTypeService - создание новой роли пользователя
        """

        # Проверка на администратора
        if token_data.get("is_admin"):
            async with engine:
                result = await engine.user_type_repository.add_one(data=UserType(name_type=new_user_type.name_type))
                if result:
                    return
                await UserTypeException().no_create_user_type()
        await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_all_user_types(engine: IEngineRepository) -> AllUserType:
        """
        Метод сервиса UserTypeService - получение всех типов пользователей
        """

        async with engine:
            result = await engine.user_type_repository.find_all()
            if result:
                return AllUserType(
                    user_types=[
                        UserType(
                            id=data[0].id,
                            name_type=data[0].name_type
                        )
                        for data in result
                    ]
                )
            return AllUserType(user_types=[])