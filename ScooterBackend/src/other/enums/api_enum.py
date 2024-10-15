from enum import Enum
from typing import Final


class APITagsEnum(Enum):

    # Теги связанные с пользователем
    USER: Final[str] = "User"
    USER_TYPE: Final[str] = "UserType"

    # Теги связанные с товаром
    PRODUCT: Final[str] = "Product"
    CATEGORY: Final[str] = "Category"
    SUB_CATEGORY: Final[str] = "SubCategory"
    SSUB_CATEGORY: Final[str] = "SSubCategory"
    BRAND: Final[str] = "Brand"
    MARK: Final[str] = "Mark"
    MODEL: Final[str] = "Model"
    PRODUCT_MODEL: Final[str] = "ProductModel"
    REVIEW: Final[str] = "Review"

    # Теги связанные с заказами
    ORDER: Final[str] = "Order"
    FAVOURITE: Final[str] = "Favourite"
    HISTORY_BUY: Final[str] = "HistoryBuy"

    # Теги связанные с работой
    TYPE_WORKER: Final[str] = "TypeWorker"
    VACANCIES: Final[str] = "Vacancies"

    # Другое
    API_V: Final[str] = "/api/v1"
    AUTH: Final[str] = "/auth"


class APIPrefix(Enum):

    # Префиксы для роутеров
    AUTH_PREFIX: Final[str] = "/auth"
    USER_PREFIX: Final[str] = "/user"
    USER_TYPE_PREFIX: Final[str] = "/user_type"
    PRODUCT_PREFIX: Final[str] = "/product"
    CATEGORY_PREFIX: Final[str] = "/category"
    SUB_CATEGORY_PREFIX: Final[str] = "/sub_category"
    SSUB_CATEGORY_PREFIX: Final[str] = "/sub/subcategory"
    BRAND_PREFIX: Final[str] = "/brand"
    MARK_PREFIX: Final[str] = "/mark"
    MODEL_PREFIX: Final[str] = "/model"
    PRODUCT_MODEL_PREFIX: Final[str] = "/product_model"
    REVIEW_PREFIX: Final[str] = "/review"
    ORDER_PREFIX: Final[str] = "/order"
    FAVOURITE_PREFIX: Final[str] = "/favourite"
    HISTORY_BUY_PREFIX: Final[str] = "/history_buy"
    TYPE_WORKER_PREFIX: Final[str] = "/type_worker"
    VACANCIES_PREFIX: Final[str] = "/vacancies"