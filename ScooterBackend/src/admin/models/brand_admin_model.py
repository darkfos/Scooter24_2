from sqladmin import ModelView
from src.database.models.brand import Brand
from typing import List, Any, Dict


class BrandModelView(ModelView, model=Brand):

    name: str = "Бренд"
    name_plural: str = "Бренд"
    icon: str = "fa-solid fa-motorcycle"
    category: str = "Продукт"

    column_list: List[Any] = [Brand.id, Brand.name_brand, Brand.product_data]
    column_labels: Dict[Any, str] = {
        Brand.id: "Идентификатор бренда",
        Brand.name_brand: "Название бренда",
        Brand.product_data: "Продукты бренда",
        Brand.url_photo: "Фотография",
    }

    column_searchable_list: List[str] = [
        "name_brand",
        "product_data.title_product",
    ]

    column_sortable_list: List[str] = ["name_brand", "id"]

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules: List[str] = ["name_brand"]
    form_edit_rules: List[str] = ["name_brand", "url_photo"]

    form_ajax_refs: Dict[str, dict] = {
        "product_data": {
            "fields": (
                "id",
                "title_product",
            ),
            "order_by": ("id", "title_product"),
        }
    }
