from src.database.repository.sub_sub_categiry_repository import SubSubCategoryRepository, SubSubCategory
from src.api.dep.dependencies import IEngineRepository, EngineRepository
from src.api.core.ss_category_catalog.schemas.sub_subcategory_dto import AllSubSubCategory, SubSubCategoryBase
from src.api.authentication.secure.authentication_service import Authentication, AuthenticationEnum
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.api.core.ss_category_catalog.errors.sub_subcategory_exceptions import SubSubCategoryException
from src.store.tools import RedisTools


auth: Authentication = Authentication()
redis: RedisTools = RedisTools()


class SubSubCategoryService:

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def create_new_sub_subcategory(
        engine: IEngineRepository,
        token: str,
        new_s_sc: SubSubCategoryBase,
        token_data: dict = {}
        ) -> None:
        """
        Метод сервиса  SubSubCategoryService - создание новой под подкатегории товара
        """

        async with engine:
            
            is_admin = await engine.admin_repository.find_admin_by_email_and_password(email=token_data.get("email"))
            if is_admin:

                is_created = await engine.sub_subcategory_repository.add_one(data=SubSubCategory(
                    name=new_s_sc.name,
                    id_sub_category=new_s_sc.id_sub_category
                ))

                if is_created:
                    return
                await SubSubCategoryException().no_create_a_new_sub_subcategory()
            await UserHttpError().http_user_not_found()
    
    @redis
    @staticmethod
    async def get_sub_subcategory_by_id_s(engine: IEngineRepository, id_s: int, redis_search_data: str = "") -> AllSubSubCategory:
        """
        Метод сервиса SubSubCategoryService - получение всех подкатегорий 2-го уровня для подкатегории 1-го уровня
        """

        async with engine:

            all_sub_subcategory = await engine.sub_subcategory_repository.find_all_s_subcategory_by_id_s(id_s=id_s)
            if all_sub_subcategory:
                return AllSubSubCategory(
                    all_sub_subcategories=[SubSubCategoryBase(name=model[0].name, id_sub_category=model[0].id_sub_category) for model in all_sub_subcategory]
                )
            await SubSubCategoryException().no_found_a_sub_subcategory()
    
    @redis
    @staticmethod
    async def get_all_sub_subcategory(engine: IEngineRepository, redis_search_data: str = "") -> AllSubSubCategory:
        """
        Метод сервиса SubSubCategoryService - получение всех подкатегорий 2-го уровня
        """

        async with engine:

            all_sub_subcategory = await engine.sub_subcategory_repository.find_all()
            if all_sub_subcategory:
                return AllSubSubCategory(
                    all_sub_subcategories=[SubSubCategoryBase(name=model[0].name, id_sub_category=model[0].id_sub_category) for model in all_sub_subcategory]
                )
            return AllSubSubCategory(
                all_sub_subcategories=[]
            )
    
    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_sub_subcategory_by_id(engine: IEngineRepository, token: str, id_s_sc: int, token_data: dict = {}) -> None:
        """
        Метод сервиса SubSubCategoryService - удаление подкатегории 2-го уровня
        """

        async with engine:

            is_admin = await engine.admin_repository.find_admin_by_email_and_password(email=token.get("email"))
            if is_admin:
                is_deleted = await engine.sub_subcategory_repository.delete_one(other_id=id_s_sc)
                if is_deleted:
                    return
                await SubSubCategoryException().no_delete_sub_subcategory()
            await UserHttpError().http_user_not_found()