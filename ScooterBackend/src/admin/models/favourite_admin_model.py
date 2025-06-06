from sqladmin import ModelView
from typing import List, Any

from src.database.models.favourite import Favourite


class FavouriteModelView(ModelView, model=Favourite):

    name: str = "Избранные товары"
    name_plural: str = "Избранное"
    icon: str = "fa fa-bookmark"
    category: str = "Данные пользователей"

    column_list: List[Any] = [
        Favourite.id,
        Favourite.id_user,
        Favourite.id_product,
        Favourite.fav_user,
        Favourite.product_info,
    ]
    column_labels: dict = {
        Favourite.id: "Идентификатор избр. товара",
        Favourite.id_user: "Идентификатор пользователя",
        Favourite.id_product: "Идентификатор продукта",
        Favourite.fav_user: "Пользователь",
        Favourite.product_info: "Продукт",
    }

    column_searchable_list: list[str] = [
        "id_user",
        "id_product",
        "product_info.title_product",
        "fav_user.email_user",
    ]

    column_sortable_list: list[str] = ["id_user", "id_product", "id"]

    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_ajax_refs: dict = {
        "fav_user": {
            "fields": (
                "id",
                "name_user",
            ),
            "order_by": ("id"),
        },
        "product_info": {
            "fields": (
                "id",
                "title_product",
            ),
            "order_by": ("id"),
        },
    }
