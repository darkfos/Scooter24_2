from sqladmin import ModelView
from src.database.models.subcategory import SubCategory
from typing import Any, List


class SubCategoryModelView(ModelView, model=SubCategory):

    # Metadata
    name: str = "Подкатегории товаров"
    name_plural: str = "Подкатегории"
    icon: str = "fa fa-bookmark"
    category: str = "Продукт"

    column_list: List[Any] = [
        SubCategory.id,
        SubCategory.name,
        SubCategory.id_category,
        SubCategory.sub_sub_category_data
    ]

    column_labels: dict = {
        SubCategory.id: "Идентификатор",
        SubCategory.name: "Название",
        SubCategory.id_category: "Категория",
        SubCategory.sub_sub_category_data: "Данные подкатегории"
    }

    form_ajax_refs: dict = {
        "sub_sub_category_data": {"fields": ("id", ), "order_by": ("id")}
    }

    # Operations
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True