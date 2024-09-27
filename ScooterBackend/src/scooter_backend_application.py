# Local
import logging.config
from src.settings.api_settings.api_settings import APISettings

# ROUTES
from src.api.core.user_catalog.router.user_router import user_router as user_router
from src.api.core.auth_catalog.router.authentication_router import auth_router as auth_router
from src.api.core.category_catalog.router.category_router import category_router as category_router
from src.api.core.admin_catalog.router.admin_router import admin_router as admin_router
from src.api.core.review_catalog.router.review_router import review_router as review_router
from src.api.core.product_catalog.router.product_router import product_router as product_router
from src.api.core.order_catalog.router.order_router import order_router as order_router
from src.api.core.favourite_catalog.router.favourite_router import favourite_router as favourite_router
from src.api.core.history_catalog.router.history_buy_router import history_buy_router as history_buy_router
from src.api.core.type_worker_catalog.router.type_worker_router import type_worker_router as type_worker_router
from src.api.core.vacancy_catalog.router.vacancies_router import vacancies_router as vacancies_router
from src.api.general_router import api_v1_router
from src.admin.admin_panel import AdminPanel


# Other libraries
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List


class ScooterBackendApplication:

    def __init__(self) -> None:
        self.scooter24_app: FastAPI = FastAPI(
            title="Scooter24 API",
            description="Программный интерфейс для сайта по продаже мото-деталей",
            # lifespan=connection_db
        )

        # Static's
        self.statics: StaticFiles = StaticFiles(directory="src/static")
        self.scooter24_app.mount(path="/static", app=self.statics, name="static")

        # Admjn panel
        self.admin: AdminPanel = AdminPanel(app=self.scooter24_app)

        # Initialize model's view
        self.admin.initialize_models_view(models=[])

        self.origins: List[str] = ["*", "http://localhost:8000"]

        self.include_router()

    def include_router(self, routers: List[APIRouter] = []) -> None:

        routers_list: List[APIRouter] = [
            auth_router,
            user_router,
            admin_router,
            product_router,
            favourite_router,
            category_router,
            vacancies_router,
            type_worker_router,
            api_v1_router.get_api_v1,
            history_buy_router,
            order_router,
            review_router,
        ]
        if routers:
            routers_list.extend(routers)

        for router in routers_list:
            self.scooter24_app.include_router(router=router)

    def added_middleware(self) -> None:
        self.scooter24_app.add_middleware(
            CORSMiddleware,
            allow_origins=self.origins,
            allow_credentials=True,
            allow_method=["*"],
            allow_headers=["*"],
        )

    @staticmethod
    @asynccontextmanager
    async def connection_db(app: FastAPI) -> None:
        # lifespan for db
        # await db_work.create_tables()
        # yield
        pass
