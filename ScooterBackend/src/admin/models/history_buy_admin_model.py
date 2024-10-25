from sqladmin import ModelView
from typing import List, Any
from src.database.models.history_buy import HistoryBuy


class HistoryBuyModelView(ModelView, model=HistoryBuy):

    # Metadata
    name: str = "История покупок"
    name_plural: str = "История"
    icon: str = "fa fa-archive"
    category: str = "Данные пользователей"

    column_list: List[Any] = [
        HistoryBuy.id,
        HistoryBuy.id_user,
        HistoryBuy.id_product,
        HistoryBuy.hst_user,
        HistoryBuy.product_data,
    ]
    column_labels: dict = {
        HistoryBuy.id: "Идентификатор истории",
        HistoryBuy.id_user: "Идентификатор пользователя",
        HistoryBuy.id_product: "Идентификатор продукта",
        HistoryBuy.hst_user: "Пользователь",
        HistoryBuy.product_data: "Данные продуктов",
    }

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules = ["hst_user", "product_data"]

    # Form's
    form_ajax_refs: dict = {
        "hst_user": {
            "fields": (
                "id",
                "name_user",
            ),
            "order_by": ("id"),
        },
        "product_data": {"fields": ("id", "title_product"), "order_by": ("id")},
    }
