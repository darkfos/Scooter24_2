from src.api.dep.dependencies import IEngineRepository
from src.database.models.subcategory import SubCategory
from src.api.core.subcategory_app.errors.http_subcategory_exceptions import (  # noqa
    SubCategoryException,
)
from src.api.core.subcategory_app.schemas.subcategory_dto import (
    AllSubCategories,
    SubCategoryAllData,
    SubCategoryBase,
)
from src.api.authentication.secure.authentication_service import (
    Authentication,
    AuthenticationEnum,
)
from src.api.core.user_app.error.http_user_exception import UserHttpError
from src.store.tools import RedisTools


redis: RedisTools = RedisTools()
auth: Authentication = Authentication()


class SubCategoryService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def added_new_model_to_product(
        engine: IEngineRepository,
        token: str,
        new_model: SubCategoryBase,
        token_data: dict = {},
    ) -> None:
        """
        Метод сервиса ProductModels для добавления
        новой модели к продукту
        """

        async with engine:

            is_admin = await engine.user_repository.find_user_by_email_and_password(
                email=token_data.get("email")
            )
            if is_admin:

                is_added = await engine.product_models_repository.add_one(
                    data=SubCategory(
                        name=SubCategoryBase.name,
                        id_category=SubCategoryBase.id_category,
                    )
                )

                if is_added:
                    return
                await SubCategoryException().no_create_a_new_subcategory()
            await UserHttpError().http_user_not_found()

    @redis
    async def get_subcategories_by_id_category(
        engine: IEngineRepository, id_category: int, redis_search_data: str = ""
    ) -> SubCategoryAllData:
        """
        Метод сервиса ProductModels для получения моделей
        продукта по идентификатору продукта
        """

        async with engine:

            all_models_by_id_category = await engine.subcategory_repository.find_subcategories_by_id_category(  # noqa
                id_category=id_category
            )  # noqa

            if all_models_by_id_category:
                return AllSubCategories(
                    all_subcategory=[
                        SubCategoryAllData(
                            id_subcategory=model[0].id,
                            id_category=model[0].id_category,
                            name=model[0].name,
                        )
                        for model in all_models_by_id_category
                    ]
                )
            await SubCategoryException().no_found_a_subcategory()

    async def get_all_product_models(
        engine: IEngineRepository,
    ) -> SubCategoryAllData:
        """
        Метод сервиса ProductModels для получения всех моделей продуктов
        """

        async with engine:
            all_subcategory_models = await engine.subcategory_repository.find_all()
            if all_subcategory_models:
                return AllSubCategories(
                    all_subcategory=[
                        SubCategoryAllData(
                            id_category=model[0].id_category,
                            id_subcategory=model[0].id,
                            name=model[0].name,
                        )
                        for model in all_subcategory_models
                    ]
                )
            return AllSubCategories(all_subcategory=[])

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    async def delete_product_models_by_id(
        engine: IEngineRepository,
        token: str,
        id_subcategory: int,
        token_data: dict = {},
    ) -> None:
        """
        Метод сервиса ProductModels для удаления модели
        продукта по идентификатору
        """

        async with engine:

            is_admin = await engine.user_repository.find_user_by_email_and_password(
                email=token_data["email"]
            )

            if is_admin and is_admin.id_type_user == 2:
                is_deleted = await engine.subcategory_repository.delete_one(
                    other_id=id_subcategory
                )

                if is_deleted:
                    return
                await SubCategoryException().no_delete_a_subcategory()

            await UserHttpError().http_user_not_found()
