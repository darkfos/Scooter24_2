from src.api.core.model_app.schemas.model_dto import ModelBase, AllModelBase
from src.api.core.model_app.errors.http_model_exceptions import (
    ModelException,
)
from src.database.models.model import Model
from src.api.core.user_app.error.http_user_exception import UserHttpError
from src.api.dep.dependencies import IEngineRepository
from src.api.authentication.secure.authentication_service import (
    Authentication,
    AuthenticationEnum,
)
from src.store.tools import RedisTools


auth: Authentication = Authentication()
redis: RedisTools = RedisTools()


class ModelService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def add_new_model(
        engine: IEngineRepository,
        token: str,
        new_model: ModelBase,
        token_data: dict = {},
    ) -> None:
        """
        Метод сервиса ModelService - создание новой модели
        """

        async with engine:

            is_admin = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                is_created = await engine.model_repository.add_one(
                    data=Model(name_model=new_model.name_model)
                )
                if is_created:
                    return
                else:
                    await ModelException().no_create_a_new_model()
            await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_model_by_id(
        engine: IEngineRepository, id_model: int
    ) -> ModelBase:
        """
        Метод сервиса ModelService - получение модели по идентификатору
        """

        async with engine:

            model_data = await engine.model_repository.find_one(
                other_id=id_model
            )

            return (
                ModelBase(
                    id_model=model_data[0].id,
                    name_model=model_data[0].name_model,
                )
                if model_data
                else await ModelException().no_found_a_model_by_id()
            )

    @redis
    @staticmethod
    async def get_all_models(
        engine: IEngineRepository, redis_search_data: str = ""
    ) -> AllModelBase:
        """
        Метод сервиса ModelService - получение всех моделей
        """

        async with engine:

            models = await engine.model_repository.find_all()

            if models:
                return AllModelBase(
                    all_models=[
                        ModelBase(
                            id_model=model[0].id,
                            name_model=model[0].name_model,
                        )
                        for model in models
                    ]
                )
            return AllModelBase(all_models=[])

    @staticmethod
    async def delete_model_by_id(
        engine: IEngineRepository,
        token: str,
        id_model: int,
        token_data: dict = {},
    ) -> None:
        """
        Метод сервиса ModelService - удаление модели по идентификатору
        """

        async with engine:

            is_admin = (
                await engine.admin_repository.find_admin_by_email_and_password(
                    email=token_data.get("email")
                )
            )

            if is_admin:
                is_deleted = await engine.model_repository.delete_one(
                    other_id=id_model
                )
                if is_deleted:
                    return
                await ModelException().no_delete_model_by_id()
            await UserHttpError().http_user_not_found()

    @staticmethod
    async def find_by_mark(
        engine: IEngineRepository, id_mark: int
    ) -> AllModelBase:
        """
        Получение всех моделей по id_mark
        :param engine:
        :param id_mark:
        :return:
        """

        async with engine:
            all_models = await engine.model_repository.find_all_by_mark(
                id_mark=id_mark
            )
            return AllModelBase(
                all_models=[
                    ModelBase(
                        id_model=model[0].id, name_model=model[0].name_model
                    )
                    for model in all_models
                ]
            )
