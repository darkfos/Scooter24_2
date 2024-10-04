# System
import sys
from typing import List, Union


# Other libraries
from fastapi import APIRouter


# Local
from src.api.core.admin_catalog.router.admin_router import admin_router
from src.api.core.auth_catalog.router.authentication_router import auth_router
from src.api.core.category_catalog.router.category_router import category_router
from src.api.core.favourite_catalog.router.favourite_router import favourite_router
from src.api.core.history_catalog.router.history_buy_router import history_buy_router
from src.api.core.order_catalog.router.order_router import order_router
from src.api.core.product_catalog.router.product_router import product_router
from src.api.core.review_catalog.router.review_router import review_router
from src.api.core.type_worker_catalog.router.type_worker_router import type_worker_router
from src.api.core.user_catalog.router.user_router import user_router
from src.api.core.vacancy_catalog.router.vacancies_router import vacancies_router
from src.api.core.mark_catalog.router.mark_router import mark_router
from src.api.core.brand_catalog.router.brand_router import brand_router


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
            product_router,
            category_router,
            mark_router,
            brand_router,
            user_router,
            auth_router,
            type_worker_router,
            vacancies_router,
            type_worker_router,
            order_router,
            favourite_router,
            review_router,
            admin_router,
            history_buy_router,
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
