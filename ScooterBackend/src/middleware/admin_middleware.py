from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class FixMixedContentMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Проверяем только HTML-ответы
        if response.headers.get("content-type", "").startswith("text/html"):
            # Получаем содержимое ответа ПРАВИЛЬНЫМ способом
            body = b""

            async for chunk in response.body_iterator:
                body += chunk

            # Заменяем HTTP на HTTPS в ссылках
            new_body = body.replace(
                b"http://xn--24-olct5adih.xn--p1ai",
                b"https://xn--24-olct5adih.xn--p1ai"
            )

            new_body = new_body.replace(
                b"http://localhost:8000",
                b"https://xn--24-olct5adih.xn--p1ai"
            )

            headers = dict(response.headers)
            headers.pop("content-length", None)

            return Response(
                content=new_body,
                status_code=response.status_code,
                headers=headers,
                media_type=response.media_type
            )
        return response
