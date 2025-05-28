from sqladmin import ModelView

from src.database.models.subcategory import SubCategory
from typing import Any, List


class SubCategoryModelView(ModelView, model=SubCategory):

    name: str = "Подкатегория товаров, 1 ур."
    name_plural: str = "Подкатегории 1 ур."
    icon: str = "fa fa-bookmark"
    category: str = "Продукт"

    column_list: List[Any] = [
        SubCategory.id,
        SubCategory.name,
        SubCategory.id_category,
        SubCategory.category_data,
    ]

    column_labels: dict = {
        SubCategory.id: "Идентификатор",
        SubCategory.name: "Название",
        SubCategory.id_category: "Категория",
        SubCategory.category_data: "Данные категории",
    }

    column_searchable_list: List[str] = ["name", "id_category"]

    column_sortable_list: List[str] = ["id", "name", "id_category"]

    form_create_rules = ["name", "category_data"]

    column_select_related_list = ["category_data"]

    form_ajax_refs = {
        "category_data": {
            "fields": ("name_category", "id"),
            "order_by": ("name_category"),
            "placeholder": "Выберите категорию",
        }
    }

    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True
