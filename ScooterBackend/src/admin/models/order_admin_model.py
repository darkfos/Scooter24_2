from sqladmin.models import ModelView
from typing import List, Any
from src.database.models.order import Order


class OrderModelView(ModelView, model=Order):

    # Metadata
    name: str = "Заказы"
    name_plural: str = "Заказ"
    icon: str = "fa fa-shopping-cart"
    category: str = "Данные пользователей"

    column_list: List[Any] = [
        Order.id,
        Order.id_user,
        Order.transaction_id,
        Order.date_buy,
        Order.ord_user,
        Order.type_operation,
        Order.email_user,
        Order.price_result,
        Order.delivery_method,
        Order.product_list,
    ]
    column_labels: dict = {
        Order.id: "Идентификатор заказа",
        Order.transaction_id: "Номер транзакции",
        Order.id_user: "Идентификатор пользователя",
        Order.date_buy: "Дата покупки",
        Order.ord_user: "Пользователь",
        Order.product_list: "Товары",
        Order.type_operation: "Тип операции",
        Order.email_user: "Почта пользователя",
        Order.price_result: "Итоговая сумма",
        Order.delivery_method: "Тип доставки",
    }

    column_searchable_list: List[str] = ["id_user", "date_buy", "product_list.title_product", "transaction_id"]

    column_sortable_list: List[str] = ["id", "id_user", "date_buy", "email_user",
                                       "transaction_id", "type_operation", "delivery_method"]

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    # Form's for FK
    form_ajax_refs: dict = {
        "ord_user": {
            "fields": (
                "id",
                "name_user",
            ),
            "order_by": ("id"),
        },
        "product_list": {
            "fields": ("id", "id_product"),
            "order_by": ("id")
        }
    }
