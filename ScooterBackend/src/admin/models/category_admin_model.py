from sqladmin import ModelView
from src.database.models.category import Category
from typing import List, Any


class CategoryModelView(ModelView, model=Category):

    name: str = "Категории"
    name_plural: str = "Категории"
    icon: str = "fa fa-tags"
    category: str = "Продукт"

    column_list: List[Any] = [
        Category.id,
        Category.name_category,
        Category.icon_category,
        Category.subcategory_data,
    ]
    column_labels: dict = {
        Category.id: "Идентификатор категории",
        Category.name_category: "Название категории",
        Category.icon_category: "Иконка",
        Category.subcategory_data: "Подкатегории",
    }

    column_searchable_list: list[str] = [
        "name_category",
        "icon_category",
        "subcategory_data.name",
    ]

    column_sortable_list: list[str] = ["name_category", "id"]

    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules = ["name_category", "icon_category"]
    form_edit_rules = form_create_rules.copy()
    column_sortable_list = [Category.name_category]
    form_columns: list = [
        Category.id,
        Category.name_category,
        Category.icon_category,
    ]
