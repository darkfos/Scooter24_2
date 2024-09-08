from sqladmin.models import ModelView
from typing import List, Any
from src.database.models.order import Order


class OrderModelView(ModelView, model=Order):

    #Metadata
    name: str = "Заказы"
    name_plural: str = "Добавить заказ"
    icon: str = "fa fa-shopping-cart"
    category: str = "Товар"

    column_list: List[Any] = [Order.id, Order.id_product, Order.id_user, Order.date_buy, Order.ord_user, Order.product_info]

    #Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    #Form's for FK
    form_ajax_refs: dict = {
        "ord_user": {
            "fields": ("id", "name_user", ),
            "order_by": ("id", )
        },
        "product_info": {
            "fields": ("id", "title_product", ),
            "order_by": ("id", )
        }
    }