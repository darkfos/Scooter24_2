#System
from typing import List, Union, Dict

#Other libraries
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from ScooterBackend.database.repository.type_worker_repository import TypeWorkerRepository, TypeWorker
from ScooterBackend.database.repository.admin_repository import AdminRepository
from ScooterBackend.api.dto.type_worker_dto import TypeWorkerBase
from ScooterBackend.api.authentication.authentication_service import Authentication
from ScooterBackend.api.exception.http_type_worker_exceptions import TypeWorkerExceptions
from ScooterBackend.api.exception.http_user_exception import UserHttpError


class TypeWorkerService:

    @staticmethod
    async def create_a_new_type_worker(session: AsyncSession, token: str, new_type_worker: TypeWorkerBase) -> None:
        """
        Метод сервиса для создания нового типа работника
        :session:
        :new_type_worker:
        """


        #Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Проверка на администратора
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(email=jwt_data.get("email"))

        if is_admin:
            is_created: bool = await TypeWorkerRepository(session=session).add_one(data=TypeWorker(
                name_type=new_type_worker.name_type
            ))
            if is_created:
                return
            await TypeWorkerExceptions().http_dont_create_a_new_type_worker()
        await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_all_types(session: AsyncSession) -> List[TypeWorkerBase]:
        """
        Метод сервиса для получение всех категорий работников.
        :session:
        """

        all_types_workers: Union[List, List[TypeWorkerBase]] = await TypeWorkerRepository(session=session).find_all()

        if all_types_workers:
            return [TypeWorkerBase(name_type=worker[0].name_type) for worker in all_types_workers]
        else:
            return []

    @staticmethod
    async def get_type_worker_by_id(session: AsyncSession, id_type_worker: int) -> TypeWorkerBase:
        """
        Получение типа работника по id.
        :session:
        :id_type_worker:
        """

        type_worker: Union[None, List[TypeWorker]] = await TypeWorkerRepository(session=session).find_one(other_id=id_type_worker)

        if type_worker:
            return TypeWorkerBase(name_type=type_worker[0].name_type)
        await TypeWorkerExceptions().http_not_found_type_worker()