from sqladmin import ModelView
from src.database.models.user import User
from typing import List, Any


class UserModelView(ModelView, model=User):

    #Metadata
    name: str = "Пользователь"
    name_plural: str = "Создать пользователя"
    icon: str = "fa fa-user-circle"
    category: str = "Пользователь"

    #Columns
    column_list: List[Any] = [
        User.id, User.name_user, User.email_user, User.password_user,
        User.surname_user, User.main_name_user, User.surname_user_address,
        User.address_area, User.address_index, User.address_locality,
        User.country_address, User.address_phone_number, User.address_rl_et_home,
        User.name_company_address, User.date_registration, User.date_update]
    
    #Operations
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True


    form_create_rules: List[Any] = ["name_user", "email_user", "surname_user", "main_name_user", "surname_user_address",
                               "address_area", "address_index", "address_locality", "country_address", "address_phone_number",
                               "address_rl_et_home", "name_company_address", "password_user", "date_update", "date_registration"]
    form_edit_rules = form_create_rules[:-1].copy()

    #Form's
    form_ajax_refs: dict = {
        "reviews": {
            "fields": ("id", ),
            "order_by": ("id", )
        },
        "orders_user": {
            "fields": ("id", ),
            "order_by": ("id", )
        },
        "favourites_user": {
            "fields": ("id", ),
            "order_by": ("id", )
        },
        "history_buy_user": {
            "fields": ("id", ),
            "order_by": ("id", )
        }
    }