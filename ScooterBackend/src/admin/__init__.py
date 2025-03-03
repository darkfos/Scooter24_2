from typing import List

# Model's
from admin.models.category_admin_model import CategoryModelView
from admin.models.favourite_admin_model import FavouriteModelView
from admin.models.order_admin_model import OrderModelView
from admin.models.product_admin_model import ProductModelView
from admin.models.review_admin_model import ReviewModelView
from admin.models.type_worker_admin_model import TypeWorkerModelView
from admin.models.user_admin_model import UserModelView
from admin.models.vacancies_admin_model import VacanciesModelView
from admin.models.sub_category_admin_model import SubCategoryModelView
from admin.models.brand_admin_model import BrandModelView
from admin.models.mark_admin_model import MarkModelView
from admin.models.model_admin_model import ModelModelView
from admin.models.product_model_admin_model import ProductModelsModelView
from admin.models.user_type_admin_model import UserTypeAdminModel
from admin.models.product_marks_admin_model import ProductMarksAdminModel
from admin.models.garage_admin_model import GarageAdminModel
from admin.models.product_type_model_admin_model import (
    ProductTypeModelAdminModel,
)
from admin.models.type_models_admin_model import TypeMotoAdminModel
from admin.models.product_photos_admin_model import ProductPhotosAdminModel


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
]
