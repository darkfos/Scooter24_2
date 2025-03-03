from sqladmin import ModelView
from database.models.marks import Mark
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
        Mark.model_data,
    ]
    column_labels: Dict[Any, str] = {
        Mark.id: "Идентификатор марки",
        Mark.name_mark: "Название марки",
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
        "model_data": {
            "fields": (
                "id",
                "name_model",
            ),
            "order_by": ("id", "name_model"),
        },
        "product_marks_data": {
            "fields": (
                "id",
                "id_product",
            ),
            "order_by": ("id", "id_product"),
        },
        "garage_data": {
            "fields": ("id", "id_type_moto"),
            "order_by": ("id", "id_type_moto"),
        },
    }
