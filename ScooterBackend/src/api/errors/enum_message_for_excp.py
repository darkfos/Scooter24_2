from enum import Enum


class HeaderMessage(Enum):
    header_update = "Ошибка обновления"
    header_delete = "Ошибка удаления"
    header_find = "Ошибка поиска"
    header_create = "Ошибка создания"
    header_auth = "Ошибка авторизации"
