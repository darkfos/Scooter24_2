from .user_router import user_router
from .authentication_router import auth_router
from .category_router import category_router
from .admin_router import admin_router
from .review_router import review_router
from .product_router import product_router
from .order_router import order_router
from .favourite_router import favourite_router
from .history_buy_router import history_buy_router
from .type_worker_router import type_worker_router
from .vacancies_router import vacancies_router

from fastapi import APIRouter


api_v1 = APIRouter(
    prefix="/api/v1",
    tags=["API V1"]
)

api_v1.include_router(auth_router)
api_v1.include_router(user_router)
api_v1.include_router(admin_router)
api_v1.include_router(category_router)
api_v1.include_router(product_router)
api_v1.include_router(review_router)
api_v1.include_router(order_router)
api_v1.include_router(favourite_router)
api_v1.include_router(history_buy_router)
api_v1.include_router(type_worker_router)
api_v1.include_router(vacancies_router)