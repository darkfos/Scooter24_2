from src.api.dep.dependencies import IEngineRepository
from src.api.core.type_moto_catalog.schemas.type_moto_dto import (
    ListTypeModelBase,
    TypeModelBase
)
from src.store.tools import RedisTools


redis: RedisTools = RedisTools()


class TypeMotoService:

    @redis
    @staticmethod
    async def all_tm(engine: IEngineRepository, redis_search_data: str) -> ListTypeModelBase:
        """
        Получение всех типов мото
        :param engine:
        :return:
        """

        async with engine:
            all_type_moto = await engine.type_moto_repository.find_all()
            return ListTypeModelBase(
                moto_types=[
                    TypeModelBase(
                        id_mt=tm[0].id,
                        name_type=tm[0].name_moto_type
                    )
                    for tm in all_type_moto
                ]
            )
