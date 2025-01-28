from src.api.dep.dependencies import IEngineRepository
from src.api.core.garage_app.schemas.garage_dto import (
    ListGarageBase,
    GarageBase
)
from src.api.authentication.secure.authentication_service import Authentication
from src.other.enums.auth_enum import AuthenticationEnum
from src.api.core.user_app.error.http_user_exception import UserHttpError


auth: Authentication = Authentication()


class GarageService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def get_user_mt_from_garage(
            engine: IEngineRepository,
            token: str,
            token_data: dict = {}
    ) -> ListGarageBase:
        """
        Получение пользовательского транспорта

        :param engine:
        :param token:
        :param token_data:
        :return:
        """

        async with engine:
            user_moto_garage = await engine.garage_repository.all_by_id_user(id_user=token_data.get('sub'))
            return ListGarageBase(garage=[
                GarageBase(
                    id_garage=mt[0].id,
                    id_user=mt[0].id_user,
                    id_moto_type=mt[0].id_type_moto,
                    id_model=mt[0].id_model,
                    id_mark=mt[0].id_mark,
                    mark_data=mt[0].mark_data.read_model(),
                    moto_type_data=mt[0].type_moto_data.read_model(),
                    models_data=mt[0].model_data.read_model()
                )
                for mt in user_moto_garage
            ])
