from typing import List

#Model's
from admin.models.admin_admin_model import AdminModelView
from admin.models.category_admin_model import CategoryModelView
from admin.models.favourite_admin_model import FavouriteModelView
from admin.models.history_buy_admin_model import HistoryBuyModelView
from admin.models.order_admin_model import OrderModelView
from admin.models.product_admin_model import ProductModelView
from admin.models.review_admin_model import ReviewModelView
from admin.models.type_worker_admin_model import TypeWorkerModelView
from admin.models.user_admin_model import UserModelView
from admin.models.vacancies_admin_model import VacanciesModelView
from admin.models.product_category_admin_model import ProductCategoryModelView

all_modesl: List = [AdminModelView, UserModelView, ProductCategoryModelView, CategoryModelView,
                    FavouriteModelView, OrderModelView, ReviewModelView, HistoryBuyModelView, ProductModelView,
                    TypeWorkerModelView, VacanciesModelView]