from sqladmin import ModelView
from typing import List, Any
from src.database.models.product_photos import ProductPhotos


class ProductPhotosAdminModel(ModelView, model=ProductPhotos):

    name: str = "Фотографии продукта"
    name_plural: str = "Фотографии"
    icon: str = "fa-solid fa-photo-film"
    category: str = "Продукт"

    can_view_details: bool = True
    can_create: bool = True
    can_edit: bool = True
    can_delete: bool = True
    can_view_details: bool = True

    column_list: List[Any] = [
        ProductPhotos.id,
        ProductPhotos.photo_url,
        ProductPhotos.id_product,
        ProductPhotos.product_data,
    ]

    column_labels: dict = {
        "id": "Идентификатор",
        "photo_url": "Ссылка",
        "id_product": "Продукт",
        "product_data": "Данные продукта",
    }

    column_searchable_list: list[str] = [
        "photo_url",
        "id_product",
        "product_data.title_product",
    ]

    column_sortable_list: list[str] = ["id", "id_product"]

    form_ajax_refs: dict = {
        "product_data": {"fields": ("id", "title_product"), "order_by": ("id")}
    }
