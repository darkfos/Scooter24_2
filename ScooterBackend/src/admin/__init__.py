from typing import List

# Model's
from src.admin.models.admin_admin_model import AdminModelView
from src.admin.models.category_admin_model import CategoryModelView
from src.admin.models.favourite_admin_model import FavouriteModelView
from src.admin.models.history_buy_admin_model import HistoryBuyModelView
from src.admin.models.order_admin_model import OrderModelView
from src.admin.models.product_admin_model import ProductModelView
from src.admin.models.review_admin_model import ReviewModelView
from src.admin.models.type_worker_admin_model import TypeWorkerModelView
from src.admin.models.user_admin_model import UserModelView
from src.admin.models.vacancies_admin_model import VacanciesModelView
from src.admin.models.product_category_admin_model import ProductCategoryModelView

all_models: List = [
    AdminModelView,
    UserModelView,
    ProductCategoryModelView,
    CategoryModelView,
    FavouriteModelView,
    OrderModelView,
    ReviewModelView,
    HistoryBuyModelView,
    ProductModelView,
    TypeWorkerModelView,
    VacanciesModelView,
]
