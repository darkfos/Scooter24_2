from sqladmin import ModelView
from src.database.models.product import Product


class ProductModelView(ModelView, model=Product):

    # Metadata
    name: str = "Товары"
    name_plural: str = "Товар"
    icon: str = "fa fa-motorcycle"
    category: str = "Продукт"

    column_list: list = [
        Product.id,
        Product.brand,
        Product.id_sub_category,
        Product.brand_mark,
        Product.title_product,
        Product.article_product,
        Product.explanation_product,
        Product.weight_product,
        Product.quantity_product,
        Product.price_product,
        Product.date_create_product,
        Product.date_update_information,
        Product.sub_category_data,
        Product.brand_data,
        Product.product_models_data,
        Product.order,
        Product.reviews,
        Product.product_info_for_fav,
        Product.photos,
        Product.label_product,
        Product.brand_mark,
        Product.type_models,
    ]

    column_labels: dict = {
        Product.id: "Идентификатор продукта",
        Product.id_sub_category: "Идентификатор подкатегории",
        Product.brand: "Бренд",
        Product.brand_data: "Данные бренда",
        Product.title_product: "Заголовок",
        Product.article_product: "Артикл",
        Product.explanation_product: "Описание",
        Product.weight_product: "Объемный вес продукта",
        Product.quantity_product: "Количество",
        Product.product_discount: "Скидка",
        Product.price_product: "Цена без скидки",
        Product.date_create_product: "Дата создания",
        Product.date_update_information: "Дата обновления",
        Product.sub_category_data: "Данные подкатегории",
        Product.product_info_for_fav: "Избранные",
        Product.label_product: "Метка продукта",
        Product.product_models_data: "Модели продукта",
        Product.brand_mark: "Марки",
        Product.type_models: "Типы мототранспорта",
        Product.photos: "Фотографии",
    }

    # Operation's
    can_create: bool = True
    can_delete: bool = True
    can_edit: bool = True
    can_export: bool = True
    can_view_details: bool = True

    form_create_rules: list = [
        "sub_category_data",
        "brand_data",
        "title_product",
        "article_product",
        "explanation_product",
        "quantity_product",
        "product_discount",
        "weight_product",
        "price_product",
        "date_create_product",
        "date_update_information",
        "label_product",
        "type_models",
        "photos",
    ]

    form_edit_rules = [
        "brand_data",
        "title_product",
        "article_product",
        "explanation_product",
        "quantity_product",
        "product_discount",
        "weight_product",
        "price_product",
        "sub_category_data",
        "label_product",
        "photos",
    ]

    # Form's for FK
    form_ajax_refs: dict = {
        "brand_data": {
            "fields": ("id", "name_brand"),
            "order_by": "name_brand",
        },
        "brand_mark": {
            "fields": ("id", "id_product"),
            "order_by": ("id", "id_product"),
        },
        "reviews": {
            "fields": (
                "id",
                "id_user",
                "id_product",
            ),
            "order_by": ("id"),
        },
        "order": {
            "fields": (
                "id",
                "date_buy",
                "id_user",
            ),
            "order_by": ("id"),
        },
        "product_info_for_fav": {"fields": ("id",), "order_by": ("id")},
        "sub_category_data": {"fields": ("id", "name"), "order_by": ("id")},
        "product_models_data": {"fields": ("id",), "order_by": ("id")},
        "photos": {"fields": ("id", "photo_url"), "order_by": ("id")},
        "type_models": {"fields": ("id", "id_type_model"), "order_by": ("id")},
    }
