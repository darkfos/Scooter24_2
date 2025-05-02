# System
from typing import List, Union, Type
import logging as logger

# Local
from src.database.repository.type_worker_repository import TypeWorker
from src.api.core.type_worker_app.schemas.type_worker_dto import (
    TypeWorkerBase,
    TypeWorkerList,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.api.core.type_worker_app.error.http_type_worker_exceptions import (
    TypeWorkerExceptions,
)
from src.api.core.user_app.error.http_user_exception import UserHttpError
from src.api.dep.dependencies import IEngineRepository
from src.other.enums.auth_enum import AuthenticationEnum


# Redis
from src.store.tools import RedisTools


redis: Type[RedisTools] = RedisTools()
auth: Authentication = Authentication()
logging = logger.getLogger(__name__)


class TypeWorkerService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_a_new_type_worker(
        engine: IEngineRepository,
        token: str,
        new_type_worker: TypeWorkerBase,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для создания нового типа работника
        :session:
        :new_type_worker:
        """

        logging.info(
            msg=f"{TypeWorkerService.__name__}"
            f" Создание нового типа работника"
        )
        async with engine:
            # Проверка на администратора
            is_admin: bool = token_data.get("is_admin")

            if is_admin:
                is_created: bool = await engine.type_worker_repository.add_one(
                    data=TypeWorker(name_type=new_type_worker.name_type)
                )
                if is_created:
                    return
                logging.critical(
                    msg=f"{TypeWorkerService.__name__} "
                    f"Не удалось создать нового типа работника"
                )
                (
                    await TypeWorkerExceptions().http_dont_create_a_new_type_worker()  # noqa
                )  # noqa
            logging.critical(
                msg=f"{TypeWorkerService.__name__} "
                f"Не удалось создать нового типа работника,"
                f" пользователь не был найден"
            )
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

        logging.info(
            msg=f"{TypeWorkerService.__name__} "
            f"Получение всех категорий работников"
        )
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
                return TypeWorkerList(
                    type_worker=[]
                )

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

        logging.info(
            msg=f"{TypeWorkerService.__name__} "
            f"Получение типа работника по "
            f"id={id_type_worker}"
        )
        async with engine:
            type_worker: Union[None, List[TypeWorker]] = (
                await engine.type_worker_repository.find_one(
                    other_id=id_type_worker
                )
            )

            if type_worker:
                return TypeWorkerBase(name_type=type_worker[0].name_type)
            logging.critical(
                msg=f"{TypeWorkerService.__name__} "
                f"Не удалось получить тип работника,"
                f" не был найден"
            )
            await TypeWorkerExceptions().http_not_found_type_worker()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_type_worker(
        engine: IEngineRepository,
        id_type_worker: int,
        token: str,
        token_data: dict = dict(),
    ) -> None:
        """
        Удаление типа работника
        :session:
        :id_type_worker:
        """

        logging.info(
            msg=f"{TypeWorkerService.__name__} " f"Удаление типа работника"
        )

        async with engine:
            # Проверка на администратора
            is_admin: bool = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                is_deleted: bool = (
                    await engine.type_worker_repository.delete_one(
                        other_id=id_type_worker
                    )
                )
                if is_deleted:
                    return
                logging.critical(
                    msg=f"{TypeWorkerService.__name__} "
                    f"Не удалось удалить тип работника"
                )
                await TypeWorkerExceptions().http_dont_delete_type_worker()
            logging.critical(
                msg=f"{TypeWorkerService.__name__} "
                f"Не удалось удалить тип работника, "
                f"пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()
