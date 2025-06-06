from typing import List

# Model's
from src.admin.models.category_admin_model import CategoryModelView
from src.admin.models.favourite_admin_model import FavouriteModelView
from src.admin.models.order_admin_model import OrderModelView
from src.admin.models.product_admin_model import ProductModelView
from src.admin.models.review_admin_model import ReviewModelView
from src.admin.models.type_worker_admin_model import TypeWorkerModelView
from src.admin.models.user_admin_model import UserModelView
from src.admin.models.vacancies_admin_model import VacanciesModelView
from src.admin.models.sub_category_admin_model import SubCategoryModelView
from src.admin.models.brand_admin_model import BrandModelView
from src.admin.models.mark_admin_model import MarkModelView
from src.admin.models.model_admin_model import ModelModelView
from src.admin.models.product_model_admin_model import ProductModelsModelView
from src.admin.models.user_type_admin_model import UserTypeAdminModel
from src.admin.models.product_marks_admin_model import ProductMarksAdminModel
from src.admin.models.garage_admin_model import GarageAdminModel
from src.admin.models.product_type_model_admin_model import (
    ProductTypeModelAdminModel,
)
from src.admin.models.type_models_admin_model import TypeMotoAdminModel
from src.admin.models.product_photos_admin_model import ProductPhotosAdminModel
from src.admin.models.vacancies_requests_admin_model import (
    VacanciesRequestsAdminModel,
)


all_models: List = [
    UserModelView,
    CategoryModelView,
    FavouriteModelView,
    OrderModelView,
    ReviewModelView,
    ProductModelView,
    TypeWorkerModelView,
    VacanciesModelView,
    SubCategoryModelView,
    BrandModelView,
    MarkModelView,
    ModelModelView,
    ProductModelsModelView,
    UserTypeAdminModel,
    ProductPhotosAdminModel,
    ProductMarksAdminModel,
    GarageAdminModel,
    ProductTypeModelAdminModel,
    TypeMotoAdminModel,
    ProductPhotosAdminModel,
    VacanciesRequestsAdminModel,
]
