from sqladmin import ModelView
from database.models.category import Category
from typing import List, Any


class CategoryModelView(ModelView, model=Category):

    #Metadata
    name: str = "Категории"
    name_plural: str = "Добавить категорию"
    icon: str = "fa-star-half-o"
    category: str = "Товар"

    column_list: List[Any] = [Category.id, Category.name_category]

    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules = ["name_category"]
    form_edit_rules = form_create_rules.copy()