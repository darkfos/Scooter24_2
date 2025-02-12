from sqladmin import ModelView
from src.database.models.product_models import ProductModels
from typing import List, Any, Dict


class ProductModelsModelView(ModelView, model=ProductModels):

    # Metadata
    name: str = "Модели продукта"
    name_plural: str = "Модели продукта"
    category: str = "Продукт"
    icon: str = "fa-solid fa-motorcycle"

    column_list: List[Any] = [
        ProductModels.id,
        ProductModels.id_model,
        ProductModels.id_product,
        ProductModels.model_data,
        ProductModels.product_data,
    ]
    column_labels: Dict[Any, str] = {
        ProductModels.id: "Идентификатор модели продукта",
        ProductModels.id_model: "Идентификатор модели",
        ProductModels.id_product: "Идентификатор продукта",
        ProductModels.model_data: "Данные модели",
        ProductModels.product_data: "Данные продукта",
    }

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules = ["model_data", "product_data"]
    form_edit_rules = ["model_data", "product_data"]

    form_ajax_refs: Dict[str, dict] = {
        "model_data": {
            "fields": (
                "id",
                "name_model",
            ),
            "order_by": ("name_model"),
        },
        "product_data": {
            "fields": (
                "id",
                "title_product",
            ),
            "order_by": ("title_product"),
        },
    }
