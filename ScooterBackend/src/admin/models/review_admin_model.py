from sqladmin.models import ModelView
from src.database.models.review import Review
from typing import List, Any


class ReviewModelView(ModelView, model=Review):

    #Metadata
    name: str = "Отзывы"
    name_plural: str = "Добавить отзыв"
    icon: str = "fa fa-comment"
    category: str = "Товар"

    column_list: List[Any] = [Review.id, Review.id_product, Review.id_user, Review.text_review, Review.estimation_review]

    #Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    #Form's for FK
    form_ajax_refs: dict = {
        "product": {
            "fields": ("id", "title_product", ),
            "order_by": ("id", )
        },
        "user": {
            "fields": ("id", "name_user", ),
            "order_by": ("id", )
        }
    }