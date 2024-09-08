from sqladmin import ModelView
from src.database.models.admin import Admin
from typing import List, Any


class AdminModelView(ModelView, model=Admin):

    #Metadata
    name: str = "Администратор"
    name_plural: str = "Создать администратора"
    icon: str = "fa-user-secret"
    category: str = "Пользователь"

    #Columns
    column_list: List[Any] = [Admin.id, Admin.date_create, Admin.date_update, Admin.email_admin, Admin.password_user]
    
    #Operations
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    #Form's
    form_create_rules: List = ["date_create", "date_update", "email_admin", "password_user"]
    form_edit_rules = form_create_rules[1:].copy()