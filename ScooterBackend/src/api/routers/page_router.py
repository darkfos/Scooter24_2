#Other libraries
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, status


page_router: APIRouter = APIRouter(
    prefix="/site"
)
templates = Jinja2Templates(directory="templates")


@page_router.get(
    path="/main",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_main_page(request: Request) -> HTMLResponse:
    """
        Переход на главную страницу сайта
    """

    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@page_router.get(
    path="/jobs",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_job_page(request: Request) -> HTMLResponse:
    """
        Переход на страницу 'Работа'
    """

    return templates.TemplateResponse(
        request=request, name="jobs.html"
    )


@page_router.get(
    path="/accessories",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_accessories_page(request: Request) -> HTMLResponse:
    """
        Переход на страницу 'Акссесуары'
    """

    return templates.TemplateResponse(
        request=request, name="accessories.html"
    )


@page_router.get(
    path="/brake_sys",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_brake_system_page(request: Request) -> HTMLResponse:
    """
        Получение страницы Тормозная система
    """

    return templates.TemplateResponse(
        request=request, name="brake-system.html"
    )


@page_router.get(
    path="/brands",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_brands_page(request: Request) -> HTMLResponse:
    """
        Получение страница Бренды
    """

    return templates.TemplateResponse(
        request=request, name="brands.html"
    )


@page_router.get(
    path="/data_protection",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_data_protection_page(request: Request) -> HTMLResponse:
    """
        Получение страницы Защита данных
    """

    return templates.TemplateResponse(
        request=request, name="dataprotection.html"
    )


@page_router.get(
    path="/delivery",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_delivery_page(request: Request) -> HTMLResponse:
    """
        Получение страницы Доставка
    """

    return templates.TemplateResponse(
        request=request, name="delivery.html"
    )


@page_router.get(
    path="/electrics",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_electrics_page(request: Request) -> HTMLResponse:
    """
        Получение страницы Электроника
    """

    return templates.TemplateResponse(
        request=request, name="electrics.html"
    )


@page_router.get(
    path="/engine",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_engine_page(request: Request) -> HTMLResponse:
    """
        Получение страницы Двигатели
    """

    return templates.TemplateResponse(
        request=request, name="engine.html"
    )


@page_router.get(
    path="/fuel_system",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_fuel_system_page(request: Request) -> HTMLResponse:
    """
        Получение страницы Топливная система
    """

    return templates.TemplateResponse(
        request=request, name="fuel-system.html"
    )


@page_router.get(
    path="/legal",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_legal_page(request: Request) -> HTMLResponse:
    """
        Получение страницы Правила
    """

    return templates.TemplateResponse(
        request=request, name="legal.html"
    )


@page_router.get(
    path="/pay",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_pay_page(request: Request) -> HTMLResponse:
    """
        Получение страницы Оплата
    """

    return templates.TemplateResponse(
        request=request, name="pay.html"
    )


@page_router.get(
    path="/product",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_product_page(request: Request) -> HTMLResponse:
    """
        Получение страницы Продукт
    """

    return templates.TemplateResponse(
        request=request, name="product.html"
    )


@page_router.get(
    path="/return",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_return_page(request: Request) -> HTMLResponse:
    """
        Получение страницы 'Обратной связи'
    """

    return templates.TemplateResponse(
        request=request, name="return.html"
    )


@page_router.get(
    path="/revocation",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_revocation_page(request: Request) -> HTMLResponse:
    """
        Получение страницы 'Сводки правил'
    """

    return templates.TemplateResponse(
        request=request, name="revocation.html"
    )


@page_router.get(
    path="/salesroom",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_salesroom_page(request: Request) -> HTMLResponse:
    """
        Получение страницы 'Торговля'
    """

    return templates.TemplateResponse(
        request=request, name="Salesroom.html"
    )


@page_router.get(
    path="/suspension",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_suspension_page(request: Request) -> HTMLResponse:
    """
        Получение страницы 'Подвеска'
    """

    return templates.TemplateResponse(
        request=request, name="suspension.html"
    )


@page_router.get(
    path="/techtips",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_techtips_page(request: Request) -> HTMLResponse:
    """
        Получение страницы 'Теххнические советы'
    """

    return templates.TemplateResponse(
        request=request, name="techtips.html"
    )


@page_router.get(
    path="/transmission",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_transmission_page(request: Request) -> HTMLResponse:
    """
        Получение страницы 'Трансмиссия'
    """

    return templates.TemplateResponse(
        request=request, name="transmission.html"
    )


@page_router.get(
    path="/uncategorized",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK
)
async def get_uncategorized_page(request: Request) -> HTMLResponse:
    """
        Получение страницы 'Все категории'
    """

    return templates.TemplateResponse(
        request=request, name="uncategorized.html"
    )