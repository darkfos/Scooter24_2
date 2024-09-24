from sqladmin import ModelView
from typing import List, Any
from src.database.models.history_buy import HistoryBuy


class HistoryBuyModelView(ModelView, model=HistoryBuy):

    # Metadata
    name: str = "История покупок"
    name_plural: str = "История"
    icon: str = "fa fa-archive"
    category: str = "Пользователь"

    column_list: List[Any] = [
        HistoryBuy.id,
        HistoryBuy.id_user,
        HistoryBuy.id_product,
        HistoryBuy.hst_user,
    ]
    column_labels: dict = {
        HistoryBuy.id: "Идентификатор истории",
        HistoryBuy.id_user: "Идентификатор пользователя",
        HistoryBuy.id_product: "Идентификатор продукта",
        HistoryBuy.hst_user: "Пользователь",
    }

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    # Form's
    form_ajax_refs: dict = {
        "hst_user": {
            "fields": (
                "id",
                "name_user",
            ),
            "order_by": ("id"),
        }
    }
