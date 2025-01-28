# System
from typing import List, Union


# Other libraries
from fastapi import APIRouter


# Local
from src.api.core.auth_app.router.authentication_router import auth_router
from src.api.core.category_app.router.category_router import category_router
from src.api.core.favourite_app.router.favourite_router import (
    favourite_router,
)
from src.api.core.order_app.router.order_router import order_router
from src.api.core.product_app.router.product_router import product_router
from src.api.core.review_app.router.review_router import review_router
from src.api.core.type_worker_app.router.type_worker_router import (
    type_worker_router,
)
from src.api.core.user_app.router.user_router import user_router
from src.api.core.vacancy_app.router.vacancies_router import (
    vacancies_router,
)
from src.api.core.mark_app.router.mark_router import mark_router
from src.api.core.brand_app.router.brand_router import brand_router
from src.api.core.product_models_app.router.product_models_router import (
    product_models_router,
)
from src.api.core.model_app.router.model_router import model_router
from src.api.core.subcategory_app.router.subcategory_router import (
    subcategory_router,
)
from src.api.core.user_type_app.routes.user_type_router import (
    user_type_router,
)
from src.api.core.photo_app.router.photo_router import photo_router
from src.api.core.type_moto_app.router.type_moto_router import (
    tm_router,
)  # noqa
from src.api.core.garage_app.router.garage_router import garage_router # noqa


class GeneralRouter:

    def __init__(self):
        self.__api_v1_router = APIRouter(prefix="/api/v1", tags=["API V1"])
        self.register_router()

    def register_router(self, new_router: Union[APIRouter, None] = None):
        """
        Добавление нового роутера
        :new_router:
        """

        routers: List[APIRouter] = [
            user_router,
            user_type_router,
            auth_router,
            product_router,
            photo_router,
            category_router,
            subcategory_router,
            mark_router,
            brand_router,
            model_router,
            type_worker_router,
            vacancies_router,
            type_worker_router,
            order_router,
            favourite_router,
            review_router,
            product_models_router,
            tm_router,
            garage_router
        ]

        if new_router:
            routers.extend(new_router)

        for router in routers:
            self.__api_v1_router.include_router(router=router)

    def register_events(self, event):
        """
        Добавление события
        :event:
        """

        self.__api_v1_router.add_event_handler(event)

    @property
    def get_api_v1(self) -> APIRouter:
        return self.__api_v1_router


api_v1_router = GeneralRouter()
