from src.database.repository.product_models_repository import ProductModelsRepository
from src.api.dep.dependencies import IEngineRepository
from src.database.models.product_models import ProductModels
from src.api.core.product_models_catalog.errors.http_product_models_exception import ProductModelsException
from src.api.core.product_models_catalog.schemas.product_models_dto import ProductModelsBase, AllProductModels
from src.api.authentication.secure.authentication_service import Authentication, AuthenticationEnum
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.store.tools import RedisTools


redis: RedisTools = RedisTools()
auth: Authentication = Authentication()


class ProductModelsService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def added_new_model_to_product(engine: IEngineRepository, token: str, new_model: ProductModelsBase, token_data: dict = {}) -> None:
        """
        Метод сервиса ProductModels для добавления новой модели к продукту
        """

        async with engine:
            
            is_admin = await engine.admin_repository.find_admin_by_email_and_password(email=token_data.get("email"))

            if is_admin:
                
                is_added = await engine.product_models_repository.add_one(
                    data=ProductModels(id_product=new_model.id_product, id_model=new_model.id_model)
                )

                if is_added:
                    return
                
                await ProductModelsException().no_create_a_new_product_models()
        
            await UserHttpError().http_user_not_found()

    @redis
    async def get_model_by_id_product(engine: IEngineRepository, id_product: int, redis_search_data: str = "") -> AllProductModels:
        """
        Метод сервиса ProductModels для получения моделей продукта по идентификатору продукта
        """
        
        async with engine:

            all_models_by_id_product = await engine.product_models_repository.find_all_models_by_id_product(id_product=id_product)
            if all_models_by_id_product:
                return AllProductModels(
                    all_models=[ProductModelsBase(id_product=model[0].id_product, id_model=model[0].id_model) for model in all_models_by_id_product]
                )
            await ProductModelsException().no_found_a_product_models_by_id_product()

    async def get_all_product_models(engine: IEngineRepository) -> AllProductModels:
        """
        Метод сервиса ProductModels для получения всех моделей продуктов
        """

        async with engine:
            
            all_product_models = await engine.product_models_repository.find_all()
            if all_product_models:
                return AllProductModels(
                    all_models=[ProductModelsBase(id_product=model[0].id_product, id_model=model[0].id_model) for model in all_product_models]
                )
            return AllProductModels(
                all_models=[]
            )
        
    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    async def delete_product_models_by_id(engine: IEngineRepository, token: str, id_pr_m: int, token_data: dict = {}) -> None:
        """
        Метод сервиса ProductModels для удаления модели продукта по идентификатору
        """

        async with engine:

            is_admin = await engine.admin_repository.find_admin_by_email_and_password(token_data=token_data.get("email"))
            
            if is_admin:
                
                is_deleted = await engine.product_models_repository.delete_one(other_id=id_pr_m)

                if is_deleted:
                    return
                await ProductModelsException().no_to_delete_product_models_by_id()

            await UserHttpError().http_user_not_found()