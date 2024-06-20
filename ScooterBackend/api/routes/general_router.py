#System
import sys


#Other libraries
from fastapi import APIRouter


#Local
...


class GeneralRouter:

    def __init__(self):
        self.__api_v1_router = APIRouter(
            prefix="/api/v1",
            tags=["API V1"]
        )

    def register_router(self, new_router: APIRouter):
        """
        Добавление нового роутера
        :new_router:
        """

        self.__api_v1_router.include_router(
            new_router
        )

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