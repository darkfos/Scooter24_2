from sqladmin import ModelView
from src.database.models.user_type import UserType
from typing import List, Any


class UserTypeAdminModel(ModelView, model=UserType):

    # Metadata
    name: str = "Тип пользователя"
    name_plural: str = name
    icon: str = "fa-regular fa-user-check"
    category: str = "Пользователь"

    can_edit: bool = True
    can_create: bool = True
    can_delete: bool = True
    can_export: bool = True
    can_view_details: bool = True

    # Columns
    column_list: List[Any] = [UserType.id, UserType.name_type]

    form_create_rules: List[str] = ["name_type"]

    column_searchable_list: List[str] = ["name_type"]

    column_sortable_list: List[str] = ["id", "name_type"]

    # Translate
    column_labels: dict = {
        UserType.id: "Идентификатор",
        UserType.name_type: "Название",
    }
