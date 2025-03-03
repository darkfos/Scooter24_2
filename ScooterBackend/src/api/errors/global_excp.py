from fastapi import HTTPException, status


class APIError:
    """
    Класс для вызова ошибок в API
    """

    def __init__(self):
        pass

    async def api_error(
        self, code: status, detail_inf: str = "Ошибка", header: str = None
    ):
        """
        Базовая ошибка
        :param code:
        :param detail_inf:
        :param header:
        :return:
        """

        raise HTTPException(status_code=code, detail=detail_inf, headers=header)
