from api.dep.dependencies import IEngineRepository
from api.core.photo_app.dto.photo_dto import AllPhotos, PhotoBase
from store.tools import RedisTools
from api.core.photo_app.exception.photo_excp import PhotoAPIError


redis: RedisTools = RedisTools()


class PhotoService:

    @redis
    @staticmethod
    async def get_photo_product_by_id(
        uow: IEngineRepository, id_photo: int, redis_search_data: str = ""
    ) -> PhotoBase:
        async with uow:
            req = await uow.photos_repository.find_one(other_id=id_photo)
            if req:
                return PhotoBase(
                    photo_url=req[0].photo_url,
                )
            await PhotoAPIError().photo_not_found()

    @redis
    @staticmethod
    async def get_all_photos_product(
        uow: IEngineRepository, id_product: int, redis_search_data: str = ""
    ) -> AllPhotos:
        async with uow:
            req = await uow.photos_repository.find_by_product_id(
                id_product=id_product
            )
            if req:
                return AllPhotos(
                    photos=[
                        PhotoBase(photo_url=row[0].photo_url) for row in req
                    ]
                )
            await PhotoAPIError().photos_not_found()
