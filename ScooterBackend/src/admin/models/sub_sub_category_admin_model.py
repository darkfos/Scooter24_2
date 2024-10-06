from sqladmin import ModelView
from typing import List, Dict, Any
from src.database.models.sub_sub_category import SubSubCategory


class SSCategoryModelView(ModelView, model=SubSubCategory):

    # Metadata
    name: str = "Подкатегории товаров 2 ур."
    name_plural: str = "Подкатегории 2 ур."
    category: str = "Продукт"
    icon: str = "fa fa-bookmark"

    column_list: List[Any] = [SubSubCategory.id, SubSubCategory.name, SubSubCategory.id_sub_category, SubSubCategory.product_data, SubSubCategory.sub_category_data]
    column_labels: Dict[Any, str] = {
        SubSubCategory.id: "Идентификатор подкатегории",
        SubSubCategory.name: "Название подкатегории",
        SubSubCategory.id_sub_category: "Идентификатор подкатегории",
        SubSubCategory.product_data: "Данные продукта",
        SubSubCategory.sub_category_data: "Данные подкатегории"
    }

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_ajax_refs: Dict[str, dict] = {
        "product_data": {"fields": ("id", "title_product", ), "order_by": ("id", "title_product")},
        "sub_category_data": {"fields": ("id", "name", ), "order_by": ("id", "name")}
    }