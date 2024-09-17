# System
import sys
from typing import List, Union


# Other libraries
from fastapi import APIRouter


# Local
from src.api.routers.admin_router import admin_router
from src.api.routers.authentication_router import auth_router
from src.api.routers.category_router import category_router
from src.api.routers.favourite_router import favourite_router
from src.api.routers.history_buy_router import history_buy_router
from src.api.routers.order_router import order_router
from src.api.routers.product_router import product_router
from src.api.routers.review_router import review_router
from src.api.routers.type_worker_router import type_worker_router
from src.api.routers.user_router import user_router
from src.api.routers.vacancies_router import vacancies_router


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
