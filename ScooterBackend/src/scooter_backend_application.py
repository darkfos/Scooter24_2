# ROUTES
from src.api.core.user_app.router.user_router import (
    user_router as user_router,
)
from src.api.core.auth_app.router.authentication_router import (
    auth_router as auth_router,
)
from src.api.core.category_app.router.category_router import (
    category_router as category_router,
)
from src.api.core.review_app.router.review_router import (
    review_router as review_router,
)
from src.api.core.product_app.router.product_router import (
    product_router as product_router,
)
from src.api.core.order_app.router.order_router import (
    order_router as order_router,
)
from src.api.core.favourite_app.router.favourite_router import (
    favourite_router as favourite_router,
)
from src.api.core.type_worker_app.router.type_worker_router import (
    type_worker_router as type_worker_router,
)
from src.api.core.vacancy_app.router.vacancies_router import (
    vacancies_router as vacancies_router,
)
from src.api.core.mark_app.router.mark_router import mark_router
from src.api.core.brand_app.router.brand_router import brand_router
from src.api.core.model_app.router.model_router import model_router
from src.api.core.product_models_app.router.product_models_router import (
    product_models_router as pr_m_router,
)
from src.api.core.subcategory_app.router.subcategory_router import (
    subcategory_router,
)
from src.api.core.user_type_app.routes.user_type_router import (
    user_type_router,
)
from src.api.core.photo_app.router.photo_router import photo_router
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
            user_router,
            user_type_router,
            mark_router,
            model_router,
            brand_router,
            product_router,
            photo_router,
            pr_m_router,
            category_router,
            subcategory_router,
            favourite_router,
            order_router,
            review_router,
            type_worker_router,
            vacancies_router,
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
