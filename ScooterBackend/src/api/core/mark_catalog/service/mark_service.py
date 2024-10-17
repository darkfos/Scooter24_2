from src.api.dep.dependencies import IEngineRepository
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.api.core.mark_catalog.schemas.mark_dto import MarkBase, AllMarks
from src.database.models.marks import Mark
from src.api.core.mark_catalog.errors.http_mark_exception import MarkException
from src.api.authentication.secure.authentication_service import Authentication
from src.api.authentication.secure.authentication_service import (
    AuthenticationEnum,
)
from src.api.authentication.hash_service.hashing import CryptographyScooter
from src.store.tools import RedisTools
from typing import NoReturn, List, Union


auth: Authentication = Authentication()
crypt_scooter: CryptographyScooter = CryptographyScooter()
redis: RedisTools = RedisTools()


class MarkService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_a_new_mark(
        engine: IEngineRepository,
        token: str,
        new_mark_data: MarkBase,
        token_data: dict = dict(),
    ) -> NoReturn:
        """
        Метод сервиса марок по созданию новой марки
        """

        async with engine:

            # Проверка на администратора
            is_admin = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data["email"]
                )
            )

            if is_admin:

                # Создание новой марки
                new_mark = Mark(name_mark=new_mark_data.name_mark)

                is_added = await engine.mark_repository.add_one(new_mark)
                if is_added:
                    return
            await UserHttpError().http_user_not_found()

    @redis
    @staticmethod
    async def get_all_marks(
        engine: IEngineRepository, redis_search_data: dict = {}
    ) -> Union[List, List[MarkBase]]:
        """
        Метод сервиса марок для получения всех марок
        """

        async with engine:

            all_marks: Union[List, List[MarkBase]] = (
                await engine.mark_repository.find_all()
            )
            return (
                AllMarks(
                    marks=[
                        MarkBase(name_mark=mark[0].name_mark)
                        for mark in all_marks
                    ]
                )
                if all_marks
                else []
            )

    @redis
    @staticmethod
    async def get_mark_by_id(
        engine: IEngineRepository, id_mark: int, redis_search_data: dict = {}
    ) -> MarkBase:
        """
        Метод сервиса марок для получения данных об уникальной марке
        """

        async with engine:

            mark_data: Union[None, Mark] = (
                await engine.mark_repository.find_one(other_id=id_mark)
            )

            if mark_data:
                return MarkBase(name_mark=mark_data[0].name_mark)
            await MarkException().not_found_a_mark()

    @staticmethod
    async def delete_mark_by_id(
        engine: IEngineRepository, id_mark: int
    ) -> None:
        """
        Метод сервиса марок для удаления марки
        по уникальному идентификатору
        """

        async with engine:
            is_deleted = await engine.mark_repository.delete_one(
                other_id=id_mark
            )

            if is_deleted:
                return True
            await MarkException().no_delete_mark()
