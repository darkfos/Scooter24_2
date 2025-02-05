# ROUTES
from src.api.core.auth_app.router.authentication_router import (
    auth_router as auth_router,
)
from src.api.general_router import api_v1_router
from src.admin.admin_panel import AdminPanel


# Other libraries
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List


class ScooterBackendApplication:

    def __init__(self) -> None:
        self.scooter24_app: FastAPI = FastAPI(
            title="Scooter24 API",
            description="Программный интерфейс для сайта по"
            " продаже мото-деталей",
            # lifespan=connection_db
        )

        # Static's
        self.statics: StaticFiles = StaticFiles(directory="src/statics")
        self.scooter24_app.mount(
            path="/static", app=self.statics, name="static"
        )

        # Admjn panel
        self.admin: AdminPanel = AdminPanel(app=self.scooter24_app)

        # Initialize model's view
        self.admin.initialize_models_view(models=[])

        self.origins: List[str] = [
            "http://localhost:8000",
            "http://localhost:3000",
        ]

        self.include_router()
        self.added_middleware()

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
