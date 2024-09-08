from sqladmin import ModelView
from src.database.models.favourite import Favourite
from typing import List, Any


class FavouriteModelView(ModelView, model=Favourite):

    #Metadata
    name: str = "Избранные товары"
    name_plural: str = "Добавить избранное"
    icon: str = "fa-star-half-o"
    category: str = "Пользователь"

    column_list: List[Any] = [Favourite.id, Favourite.id_user, Favourite.id_product, Favourite.fav_user, Favourite.product_info]
    
    #Operations
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    #Form's for FK
    form_ajax_refs: dict = {
        "fav_user": {
            "fields": {"id", "name_user", },
            "order_by": ("id", )
        },
        "product_info": {
            "fields": {"id", "title_product", },
            "order_by": {"id, "}
        }
    }