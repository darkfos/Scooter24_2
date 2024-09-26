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
        SubCategory.level,
        SubCategory.id_category,
        SubCategory.id_sub_category,
        SubCategory.product_data_1,
        SubCategory.product_data_2,
        SubCategory.category_data,
        SubCategory.subcategory_data
    ]

    column_labels: dict = {
        SubCategory.id: "Идентификатор",
        SubCategory.name: "Название",
        SubCategory.level: "Уровень подкатегории",
        SubCategory.id_category: "Категория",
        SubCategory.id_sub_category: "Подкатегория",
        SubCategory.product_data_1: "Данные товара №1",
        SubCategory.product_data_2: "Данные товара №2",
        SubCategory.category_data: "Данные категории",
        SubCategory.subcategory_data: "Данные подкатегории"
    }

    form_ajax_refs: dict = {
        "subcategory_data": {"fields": ("id", ), "order_by": ("id")}
    }

    # Operations
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True