from sqladmin import ModelView
from database.models.user_type import UserType
from typing import List, Any


class UserTypeAdminModel(ModelView, model=UserType):

    # Metadata
    name: str = "Тип пользователя"
    name_plural: str = "Тип"
    icon: str = "fa-regular fa-user-check"
    category: str = "Пользователь"

    can_edit: bool = False
    can_create: bool = False
    can_delete: bool = False
    can_export: bool = True
    can_view_details: bool = True

    # Columns
    column_list: List[Any] = [UserType.id, UserType.name_type]

    # Translate
    column_labels: dict = {
        UserType.id: "Идентификатор",
        UserType.name_type: "Название",
    }
