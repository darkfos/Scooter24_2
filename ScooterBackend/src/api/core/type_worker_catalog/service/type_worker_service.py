# System
from typing import List, Union, Dict, Coroutine, Any, Type
import logging

# Other libraries
...

# Local
from src.database.repository.type_worker_repository import TypeWorker
from src.api.core.type_worker_catalog.schemas.type_worker_dto import TypeWorkerBase, TypeWorkerList
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.type_worker_catalog.error.http_type_worker_exceptions import TypeWorkerExceptions
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.api.dep.dependencies import IEngineRepository


# Redis
from src.store.tools import RedisTools


redis: Type[RedisTools] = RedisTools()


class TypeWorkerService:

    @staticmethod
    async def create_a_new_type_worker(
        engine: IEngineRepository, token: str, new_type_worker: TypeWorkerBase
    ) -> None:
        """
        Метод сервиса для создания нового типа работника
        :session:
        :new_type_worker:
        """

        logging.info(msg=f"{TypeWorkerService.__name__} Создание нового типа работника")
        # Данные токена
        jwt_data: Coroutine[Any, Any, Dict[str, str] | None] = (
            await Authentication().decode_jwt_token(token=token, type_token="access")
        )

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=jwt_data.get("email")
                )
            )

            if is_admin:
                is_created: bool = await engine.type_worker_repository.add_one(
                    data=TypeWorker(name_type=new_type_worker.name_type)
                )
                if is_created:
                    return
                logging.critical(msg=f"{TypeWorkerService.__name__} Не удалось создать нового типа работника")
                await TypeWorkerExceptions().http_dont_create_a_new_type_worker()
            logging.critical(msg=f"{TypeWorkerService.__name__} Не удалось создать нового типа работника, пользователь не был найден")
            await UserHttpError().http_user_not_found()

    @redis
    @staticmethod
    async def get_all_types(
        engine: IEngineRepository, redis_search_data: str
    ) -> List[TypeWorkerBase]:
        """
        Метод сервиса для получение всех категорий работников.
        :session:
        """

        logging.info(msg=f"{TypeWorkerService.__name__} Получение всех категорий работников")
        async with engine:
            all_types_workers: Union[List, List[TypeWorkerBase]] = (
                await engine.type_worker_repository.find_all()
            )

            if all_types_workers:
                return TypeWorkerList(
                    type_worker=[
                        TypeWorkerBase(name_type=worker[0].name_type)
                        for worker in all_types_workers
                    ]
                )
            else:
                return []

    @redis
    @staticmethod
    async def get_type_worker_by_id(
        engine: IEngineRepository, id_type_worker: int, redis_search_data: str
    ) -> TypeWorkerBase:
        """
        Получение типа работника по id.
        :session:
        :id_type_worker:
        """

        logging.info(msg=f"{TypeWorkerService.__name__} Получение типа работника по id={id_type_worker}")
        async with engine:
            type_worker: Union[None, List[TypeWorker]] = (
                await engine.type_worker_repository.find_one(other_id=id_type_worker)
            )

            if type_worker:
                return TypeWorkerBase(name_type=type_worker[0].name_type)
            logging.critical(msg=f"{TypeWorkerService.__name__} Не удалось получить тип работника, не был найден")
            await TypeWorkerExceptions().http_not_found_type_worker()

    @staticmethod
    async def delete_type_worker(
        engine: IEngineRepository, id_type_worker: int, token: str
    ) -> None:
        """
        Удаление типа работника
        :session:
        :id_type_worker:
        """

        logging.info(msg=f"{TypeWorkerService.__name__} Удаление типа работника")
        # Данные токена
        jwt_data: Dict[str, Union[str, int]] = await Authentication().decode_jwt_token(
            token=token, type_token="access"
        )

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=jwt_data.get("email")
                )
            )

            if is_admin:
                is_deleted: bool = await engine.type_worker_repository.delete_one(
                    other_id=id_type_worker
                )
                if is_deleted:
                    return
                logging.critical(msg=f"{TypeWorkerService.__name__} Не удалось удалить тип работника")
                await TypeWorkerExceptions().http_dont_delete_type_worker()
            logging.critical(msg=f"{TypeWorkerService.__name__} Не удалось удалить тип работника, пользователь не был найден")
            await UserHttpError().http_user_not_found()