from enum import Enum


class HeaderMessage(Enum):
    header_update: str = "Ошибка обновления"
    header_delete: str = "Ошибка удаления"
    header_find: str = "Ошибка поиска"
    header_create: str = "Ошибка создания"
    header_auth: str = "Ошибка авторизации"
