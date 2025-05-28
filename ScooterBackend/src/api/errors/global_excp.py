from fastapi import HTTPException, status


class APIError:
    def __init__(self):
        pass

    async def api_error(
        self, code: status, detail_inf: str = "Ошибка", header: str = None
    ):
        raise HTTPException(
            status_code=code, detail=detail_inf, headers=header
        )
