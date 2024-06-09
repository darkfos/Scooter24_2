import aiohttp
import asyncio
import requests
from ScooterBackend.database.db_worker import db_work
from ScooterBackend.api.dto.product_dto import ProductBase
from PIL import Image


async def create_products():
    """
    Создание товаров
    :return:
    """

    products: list[dict] = [
        {
          "title_product": "Зеркала на мотоцикл / скутер / мопед круглые S24 (встраиваемые в клипоны или руль) черные регулируемые / универсальные / для мотоцикла",
          "price_product": 996,
          "quantity_product": 23,
          "explanation_product": "2 шт. — зеркала, комплект адаптеров для установки.",
          "article_product": "SCOT78541892936",
          "tags": "1, год",
          "other_data": "Габариты: 5 x 13 x 13 cm,",
          "id_category": 4,
          "photo_product": "6449875038.jpg"
        },
        {
            "title_product": "Ручка газа короткоходная (механизм / пульт) грипсы и трос газа / универсальные «S24» (2 клавиши) черная (полный комплект)",
            "price_product": 1192,
            "quantity_product": 23,
            "explanation_product": "Короткоходная ручка газа, трос газа, грипсы (2 шт.)",
            "article_product": "SCOT7326746233481283",
            "tags": "2, года",
            "other_data": "Габариты: 7 × 10 × 20 cm,",
            "id_category": 4,
            "photo_product": "6449875650.jpg"
        },
        {
            "title_product": "Тахометр цифровой со счетчиком моточасов «S24» / Сменная батарея, в комплекте / Монтажный набор (электронный счетчик) на мотоцикл / скутер / мопед (Универсальный)",
            "price_product": 663,
            "quantity_product": 22,
            "explanation_product": "Счетчик моточасов",
            "article_product": "SCOT78235428916222",
            "tags": "2, год",
            "other_data": "Габариты: 3 × 6 × 5 cm,",
            "id_category": 4,
            "photo_product": "6449880136.jpg"
        },
        {
            "title_product": "Коленвал на китайский скутер 125/150 кубов (152QMI/157QMJ) 150cc",
            "price_product": 2521,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561302",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 20 × 10 cm,Вес: 1 kg,",
            "id_category": 5,
            "photo_product": "6439246916.jpg"
        },
        {
            "title_product": "Коленвал на китайский скутер 50 кубов (139QMB) 80cc",
            "price_product": 2219,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561303",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 20 × 10 cm,Вес: 1 kg,",
            "id_category": 5,
            "photo_product": "6439244719.jpg"
        },
        {
            "title_product": "Коленвал на китайский скутер Стелс / Венто 50 кубов (12 мм палец)(1e40qmb) Stels 50cc / Vento",
            "price_product": 2167,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561304",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 20 × 10 cm,Вес: 1 kg,",
            "id_category": 5,
            "photo_product": "6439246282.jpg"
        },
        {
            "title_product": "Коленвал на скутер Сузуки Адрес / Сепия 50 кубов (v50g) Suzuki Address / Sepia 50cc",
            "price_product": 2766,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561306",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 20 × 10 cm,Вес: 1 kg,",
            "id_category": 5,
            "photo_product": "6439246282.jpg"
        },
        {
            "title_product": "Коленвал на скутер Сузуки Летс / Верде 50 кубов (Morini) Suzuki Lets / Verde 50cc",
            "price_product": 3179,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561307",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 20 × 10 cm,Вес: 1 kg,",
            "id_category": 5,
            "photo_product": "6439246673.jpg"
        },
        {
            "title_product": "Коленвал на скутер Хонда Дио 50 кубов (32.5мм)(Af-34/35) Honda Dio ZX 50cc",
            "price_product": 3118,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561308",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 20 × 10 cm,Вес: 1 kg,",
            "id_category": 5,
            "photo_product": "6439245882.jpg"
        },
        {
            "title_product": "Коленвал на скутер Хонда Лид 90 кубов (Hf-05) Honda Lead 90cc",
            "price_product": 3110,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561313",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 20 × 10 cm,Вес: 1 kg,",
            "id_category": 5,
            "photo_product": "6439198834.jpg"
        },
        {
            "title_product": "Коленвал на скутер Ямаха Аксис 90 кубов (Ямаха Аксис)(3WF) Yamaha Axis 90cc",
            "price_product": 2679,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561314",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 20 × 10 cm,Вес: 1 kg,",
            "id_category": 5,
            "photo_product": "6439247131.jpg"
        },
        {
            "title_product": "Коленвал на скутер Ямаха Джог/Априо/Аерокс 50 кубов (3kj/5bm/Minarelli) Yamaha Jog / Aprio 50cc",
            "price_product": 1899,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561315",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 20 × 10 cm,Вес: 1 kg,",
            "id_category": 5,
            "photo_product": "6439246198.jpg"
        },
        {
            "title_product": "Набор прокладок на китайский скутер 50 кубов (139QMB) 80 кубов (80cc)",
            "price_product": 398,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561316",
            "tags": "1, год",
            "other_data": "Габариты: 20 × 10 cm,",
            "id_category": 5,
            "photo_product": "6447222252.jpg"
        },
        {
            "title_product": "Карбюратор на китайский скутер Стелс 50 кубов (1e40qmb) Stels Tactic / Vento",
            "price_product": 2210,
            "quantity_product": 22,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561293",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 15 × 10 cm,",
            "id_category": 7,
            "photo_product": "6439246782.jpg"
        },
        {
            "title_product": "Карбюратор на скутер Хонда Дио / Лид 50 кубов (Af-27/28) Honda Dio / Lead",
            "price_product": 1680,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT1267234561297",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 15 × 10 cm,",
            "id_category": 7,
            "photo_product": "6439246506.jpg"
        },
        {
            "title_product": "Топливный (бензиновый) фильтр разборной / стайлинг S24 (бензостойкая колба) на мотоцикл / мопед / скутер (Тюнинг)",
            "price_product": 476,
            "quantity_product": 23,
            "explanation_product": "Плотная упаковкапаковка, Запчасть на скутер",
            "article_product": "SCOT7882489023485",
            "tags": "1, год",
            "other_data": "Габариты: 2 × 7 × 7 cm,",
            "id_category": 7,
            "photo_product": "6449870141.jpg"
        },
        {
            "title_product": "Машинка тормозная (ГТЦ) универсальная «S24» (левая с выносным бачком) (черная) стайлинговая на мотоцикл / скутер / мопед (шланг и бочек брембо)",
            "price_product": 1193,
            "quantity_product": 22,
            "explanation_product": "Машинка тормозная (ГТЦ) универсальная (левая с выносным бачком) (черная)",
            "article_product": "SCOT6234589129354218",
            "tags": "1, год",
            "other_data": "Габариты: 5 × 6 × 15 cm,",
            "id_category": 8,
            "photo_product": "6449883508.jpg"
        },
        {
            "title_product": "Машинка тормозная (ГТЦ) универсальная «S24» (правая с выносным бачком) (черная) стайлинговая на мотоцикл / скутер / мопед (шланг и бочек брембо)",
            "price_product": 1193,
            "quantity_product": 22,
            "explanation_product": "Машинка тормозная (ГТЦ) универсальная (правая с выносным бачком) (черная)",
            "article_product": "SCOT6234589129354217",
            "tags": "1, год",
            "other_data": "Габариты: 5 × 6 × 15 cm,",
            "id_category": 8,
            "photo_product": "6449883741.jpg"
        },
        {
            "title_product": "Щека вариатора неподвижная на китайский скутер 125/150 кубов 152QMI/157QMJ 150cc внешняя",
            "price_product": 463,
            "quantity_product": 23,
            "explanation_product": "Щека вариатора внешняя неподвижная на 157QMJ",
            "article_product": "SCOT7825476452752123",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 10 × 10 cm,",
            "id_category": 9,
            "photo_product": "6478512376.jpg"
        },
        {
            "title_product": "Щека вариатора неподвижная на китайский скутер 50/80 кубов 139QMB 50cc внешняя",
            "price_product": 463,
            "quantity_product": 23,
            "explanation_product": "Щека вариатора внешняя неподвижная на 139QMB",
            "article_product": "SCOT2635894612754812",
            "tags": "1, год",
            "other_data": "Габариты: 10 × 10 × 10 cm,",
            "id_category": 9,
            "photo_product": "6478517794.jpg"
        },
        {
            "title_product": "Катушка зажигания на скутер стайлинг Хонда Дио (Af-18/27/34) и китайский скутер (139QMB/152QMI/157QMJ) Honda Dio / Tact (Тюнинг)",
            "price_product": 483,
            "quantity_product": 23,
            "explanation_product": "Стайлинговая картушка зажигания на китайский и японский скутер",
            "article_product": "SCOT2635894612754812",
            "tags": "1, год",
            "other_data": "Габариты: 2 × 8 × 2 cm,",
            "id_category": 10,
            "photo_product": "6478453611.jpg"
        },
        {
            "title_product": "Тахометр цифровой со счетчиком моточасов «S24» / Сменная батарея, в комплекте / Монтажный набор (электронный счетчик) на мотоцикл / скутер / мопед (Универсальный)",
            "price_product": 663,
            "quantity_product": 22,
            "explanation_product": "Счетчик моточасов",
            "article_product": "SCOT78235428916222",
            "tags": "1, год",
            "other_data": "Габариты: 3 × 6 × 5 cm,",
            "id_category": 10,
            "photo_product": "6449880136.jpg"
        },
    ]

    jwt_token: str = ""

    # Запись данных
    async with aiohttp.ClientSession() as session:
        # Токен
        async with session.post(
                url="http://127.0.0.1:5678/api/v1/auth/login",
                data={
                    "username": "gadshi@gmail.com",
                    "password": "chaiki45"
                }
        ) as j_session:
            jwt_token = (await j_session.json()).get("access_token")

        id_test: int = 1

        for product in products:
            file = open("/home/darkfos/PycharmProjects/Scooter24/ScooterBackend/test/data/photos/{}".format(product.get("photo_product")), "rb").read()

            req = requests.post(
                url="http://127.0.0.1:5678/api/v1/product/create_product",
                headers={"Authorization": f"Bearer {jwt_token}"},
                json={
                    "title_product": product.get("title_product"),
                    "price_product": product.get("price_product"),
                    "quantity_product": product.get("quantity_product"),
                    "explanation_product": product.get("explanation_product"),
                    "article_product": product.get("article_product"),
                    "tags": product.get("tags"),
                    "other_data": product.get("other_data"),
                    "id_category": product.get("id_category"),
                    "photo_product": "None"
                }
            )

            #Установка фотографии
            req_photo = requests.patch(
                url=f"http://127.0.0.1:5678/api/v1/product/update_product_photo/{id_test}",
                headers={"Authorization": f"Bearer {jwt_token}"},
                files={
                    "new_photo": file
                }
            )

            print(req.json())
            print(req_photo.status_code)
            id_test += 1

asyncio.run(create_products())