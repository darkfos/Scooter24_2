from sqladmin import ModelView
from src.database.models.marks import Mark
from typing import List, Dict, Any


class MarkModelView(ModelView, model=Mark):

    # Metadata
    name: str = "Марки"
    name_plural: str = "Марки"
    icon: str = "fa-solid fa-circle-xmark"
    category: str = "Продукт"

    column_list: List[Any] = [
        Mark.id,
        Mark.name_mark,
        Mark.product_data,
        Mark.model_data,
    ]
    column_labels: Dict[Any, str] = {
        Mark.id: "Идентификатор марки",
        Mark.name_mark: "Название марки",
        Mark.product_data: "Данные продукта",
        Mark.model_data: "Модели",
    }

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules: list[str] = ["name_mark"]
    form_ajax_refs: Dict[str, dict] = {
        "product_data": {
            "fields": (
                "id",
                "title_product",
            ),
            "order_by": ("id", "title_product"),
        }
    }
