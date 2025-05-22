from sqladmin import ModelView
from typing import Dict, List, Any
from src.database.models.product_type_models import ProductTypeModels


class ProductTypeModelAdminModel(ModelView, model=ProductTypeModels):

    # Metadata
    name: str = "Мототранспорт товара"
    name_plural: str = "Мототранспорт товара"
    icon: str = "fa-solid fa-motorcycle"
    category: str = "Продукт"

    column_list: List[Any] = [
        ProductTypeModels.id,
        ProductTypeModels.id_type_model,
        ProductTypeModels.id_product,
        ProductTypeModels.product_data,
        ProductTypeModels.type_models_data,
    ]
    column_labels: Dict[Any, str] = {
        ProductTypeModels.id: "Идентификатор",
        ProductTypeModels.id_type_model: "Идентификатор мототранспорта",
        ProductTypeModels.id_product: "Идентификатор товара",
        ProductTypeModels.product_data: "Товары",
        ProductTypeModels.type_models_data: "Модели транспорта",
    }

    column_searchable_list: List[str] = ["id_product", "id_type_model", "product_data.title_product"]

    column_sortable_list: List[str] = ["id", "id_product", "id_type_model"]

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules: List[str] = ["id", "id_type_models", "id_product"]
    form_ajax_refs: Dict[str, dict] = {
        "product_data": {
            "fields": (
                "id",
                "title_product",
            ),
            "order_by": ("id", "title_product"),
        },
        "type_models_data": {
            "fields": ("id", "name_moto_type"),
            "order_by": ("id", "name_moto_type"),
        },
    }
