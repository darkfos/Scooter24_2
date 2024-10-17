from sqladmin import ModelView
from src.database.models.model import Model
from typing import List, Any, Dict


class ModelModelView(ModelView, model=Model):

    # Metadata
    name: str = "Модели"
    name_plural: str = "Модели"
    icon: str = "fa-solid fa-motorcycle"
    category: str = "Продукт"

    column_list: List[Any] = [
        Model.id,
        Model.name_model,
        Model.product_models_data,
    ]
    column_labels: Dict[Any, str] = {
        Model.id: "Идентификатор модели",
        Model.name_model: "Название модели",
        Model.product_models_data: "Данные продукта",
    }

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_ajax_refs: Dict[str, dict] = {
        "product_models_data": {"fields": ("id",), "order_by": ("id")}
    }
