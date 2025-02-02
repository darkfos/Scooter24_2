from src.api.dep.dependencies import IEngineRepository
from src.api.core.garage_app.schemas.garage_dto import (
    ListGarageBase,
    GarageBase,
    AddNewMotoToGarage,
)
from src.api.authentication.secure.authentication_service import Authentication
from src.other.enums.auth_enum import AuthenticationEnum
from src.database.models.garage import Garage
from src.api.core.garage_app.errors.garage_errors import GarageException
from src.store.tools import RedisTools


auth: Authentication = Authentication()
redis: RedisTools = RedisTools()


class GarageService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_moto_in_garage(
        engine: IEngineRepository,
        token: str,
        new_moto: AddNewMotoToGarage,
        token_data: dict = {},
    ) -> bool:
        """
        Добавление транспорта в гараж

        :param engine:
        :param token:
        :param new_moto:
        :param token_data:
        :return:
        """

        async with engine:
            added_to_garage = await engine.garage_repository.add_one(
                data=Garage(
                    id_mark=new_moto.id_mark,
                    id_user=token_data.get("sub"),
                    id_model=new_moto.id_model,
                    id_type_moto=new_moto.id_moto_type,
                )
            )

            if added_to_garage:
                return added_to_garage
            await GarageException.no_create_moto()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def get_user_mt_from_garage(
        engine: IEngineRepository, token: str, token_data: dict = {}
    ) -> ListGarageBase:
        """
        Получение пользовательского транспорта

        :param engine:
        :param token:
        :param token_data:
        :return:
        """

        async with engine:
            user_moto_garage = await engine.garage_repository.all_by_id_user(
                id_user=token_data.get("sub")
            )
            return ListGarageBase(
                garage=[
                    GarageBase(
                        id_garage=mt[0].id,
                        id_user=mt[0].id_user,
                        id_moto_type=mt[0].id_type_moto,
                        id_model=mt[0].id_model,
                        id_mark=mt[0].id_mark,
                        mark_data=mt[0].mark_data.read_model(),
                        moto_type_data=mt[0].type_moto_data.read_model(),
                        models_data=mt[0].model_data.read_model(),
                    )
                    for mt in user_moto_garage
                ]
            )

    @staticmethod
    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    async def delete_mt(
        token: str, engine: IEngineRepository, id_mt: int, token_data: dict = {}
    ) -> None:
        """
        Метод сервиса Garage для удаления транспорта
        :param token:
        :param engine:
        :param id_mt:
        :param token_data:
        :return:
        """

        async with engine:
            del_mt = await engine.garage_repository.delete_user_mt(
                id_user=token_data.get("sub"), id_mt=id_mt
            )
            print(del_mt)
            if del_mt:
                # Очищаем кэш в redis
                # await redis.delete_key(key="")
                return True
            return False
