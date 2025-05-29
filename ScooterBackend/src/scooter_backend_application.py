from src.api.core.auth_app.router.authentication_router import (
    auth_router as auth_router,
)
from src.api.general_router import api_v1_router
from src.admin.admin_panel import AdminPanel


import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator

from src.middleware.admin_middleware import FixMixedContentMiddleware

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
statics_dir = os.path.join(BASE_DIR, "statics")


class ScooterBackendApplication:

    def __init__(self) -> None:
        self.scooter24_app: FastAPI = FastAPI(
            title="Scooter24 API",
            description="Программный интерфейс для сайта по"
            " продаже мото-деталей",
            docs_url="/docs",
            redoc_url="/redoc",
        )

        def custom_openapi():
            if self.scooter24_app.openapi_schema:
                return self.scooter24_app.openapi_schema
            openapi_schema = FastAPI.openapi(self.scooter24_app)
            openapi_schema["servers"] = [{"url": "/api"}]
            self.scooter24_app.openapi_schema = openapi_schema
            return openapi_schema

        self.scooter24_app.openapi = custom_openapi

        self.statics: StaticFiles = StaticFiles(directory=statics_dir)
        self.scooter24_app.mount(
            path="/statics", app=self.statics, name="static"
        )

        self.admin: AdminPanel = AdminPanel(app=self.scooter24_app)

        self.admin.initialize_models_view(models=[])

        self.origins: List[str] = [
            "http://37.77.105.239:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "https://xn--24-olct5adih.xn--p1ai",
            "https://24скутер.рф"
        ]

        self.include_router()
        self.added_middleware()

        Instrumentator().instrument(self.scooter24_app).expose(
            self.scooter24_app
        )

    def include_router(self, routers: List[APIRouter] = []) -> None:

        based_routers: List[APIRouter] = [
            auth_router,
            api_v1_router.get_api_v1,
        ]

        if routers:
            based_routers.extend(routers)

        for router in based_routers:
            self.scooter24_app.include_router(router=router)

    def added_middleware(self) -> None:
        self.scooter24_app.add_middleware(
            CORSMiddleware,
            allow_origins=self.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.scooter24_app.add_middleware(FixMixedContentMiddleware)
