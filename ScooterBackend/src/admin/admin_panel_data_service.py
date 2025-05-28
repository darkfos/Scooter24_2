import random

from starlette.responses import Response, RedirectResponse
from fastapi import status
from starlette.requests import Request
import pandas
from src.api.dep.dependencies import EngineRepository
from src.database.models.brand import Brand
from src.database.models.model import Model
from src.database.models.product_marks import ProductMarks
from src.database.models.product_models import ProductModels
from src.database.models.product import Product
from src.database.models.category import Category
from src.database.models.marks import Mark
from src.database.models.product_photos import ProductPhotos
from src.database.models.product_type_models import ProductTypeModels
from src.database.models.subcategory import SubCategory
from src.database.models.type_moto import TypeMoto
from src.other.s3_service.file_manager import S3EnumStorage, FileS3Manager


class AdminPanelService:

    id_product: int = None
    lst_to_add_product_models: list[int] = []

    @staticmethod
    async def add_product(  # noqa
        request: Request,
        file: pandas.DataFrame,
        session: EngineRepository,
        data_to_response: str,
    ) -> Response:

        cnt_to_add: int = 0
        cnt_row: int = 0

        async with session:
            session: EngineRepository = session
            try:
                for index, row in file.iterrows():

                    if pandas.notna(row["Подкатегория первого уровня"]):
                        id_subcat_1: SubCategory = (
                            await session.subcategory_repository.find_by_name(
                                name_subcategory=str(
                                    row["Подкатегория первого уровня"]
                                ).strip()
                            )
                        )

                        if id_subcat_1:
                            id_subcat_1 = id_subcat_1[0].id

                        if not id_subcat_1:

                            create_subcat_1 = (
                                await session.subcategory_repository.add_one(
                                    SubCategory(
                                        name=row.get(
                                            "Подкатегория первого уровня"
                                        ).strip(),
                                        id_category=int(row.get("Категория")),
                                    )
                                )
                            )
                            id_subcat_1 = create_subcat_1

                    if str(row.get("Бренд")) not in (None, "nan"):
                        id_brand = await session.brand_repository.find_by_name(
                            name_brand_to_find=str(row.get("Бренд")).strip(),
                        )

                        if not id_brand:
                            create_brand = (
                                await session.brand_repository.add_one(
                                    data=Brand(name_brand=row.get("Бренд"))
                                )
                            )
                            id_brand = create_brand

                    if str(row.get("Марка")) not in (None, "nan"):
                        all_marks: list[int] = []
                        marks = row.get("Марка").split(", ")

                        for mark in marks:
                            id_mark = (
                                await session.mark_repository.find_by_name(
                                    name_mark=mark
                                )
                            )

                            if not id_mark:
                                create_mark = (
                                    await session.mark_repository.add_one(
                                        data=Mark(name_mark=mark)
                                    )
                                )

                                id_mark = create_mark

                            all_marks.append(id_mark)

                    if str(row.get("Модель")) not in (None, "nan"):
                        await AdminPanelService.add_new_model(
                            line=row.get("Модель"),
                            engine=session,
                            id_mark=id_mark,
                        )

                    if pandas.notna(row.get("Тип")):
                        all_type_motos: list[int] = []
                        type_motos = str(row.get("Тип")).split(", ")

                        for tp_moto in type_motos:
                            type_moto = (
                                await session.type_moto_repository.find_name(
                                    tp_moto
                                )
                            )

                            if type_moto:
                                type_moto = type_moto[0].id
                                all_type_motos.append(type_moto)
                            else:
                                create_type_moto = (
                                    await session.type_moto_repository.add_one(
                                        data=TypeMoto(name_moto_type=tp_moto)
                                    )
                                )

                                all_type_motos.append(create_type_moto)

                    weight_product = (
                        float(row["Объемный вес, кг"])
                        if pandas.notna(row["Объемный вес, кг"])
                        else 0
                    )
                    quantity_product = (
                        int(row["Доступно к продаже по схеме FBS, шт."])
                        if pandas.notna(
                            row["Доступно к продаже по схеме FBS, шт."]
                        )
                        else 0
                    )
                    price_product = float(
                        row["Цена до скидки (перечеркнутая цена), ₽"]
                        if pandas.notna(
                            row["Цена до скидки (перечеркнутая цена), ₽"]
                        )
                        else 0
                    )

                    new_product = Product(
                        article_product=(
                            row["Артикул"]
                            if pandas.notna(row["Артикул"])
                            else "Неопределен"
                        ),
                        title_product=row["Наименование товара"],
                        brand=id_brand,
                        weight_product=weight_product,
                        id_sub_category=(
                            id_subcat_1[0].id
                            if isinstance(id_subcat_1, dict)
                            else id_subcat_1
                        ),  # Noqa
                        explanation_product=(
                            row["Описание"]
                            if str(row["Описание"]) not in (None, "nan")
                            else "Неопределено"
                        ),
                        quantity_product=quantity_product,
                        price_product=price_product,
                        product_discount=0,
                    )

                    res_to_add = await session.product_repository.add_one(
                        new_product
                    )

                    if res_to_add:

                        for mark in all_marks:
                            await session.product_marks_repository.add_one(
                                data=ProductMarks(
                                    id_mark=mark, id_product=res_to_add
                                )
                            )

                        for tp_mt in all_type_motos:
                            await session.product_type_models_repository.add_one(  # noqa
                                data=ProductTypeModels(
                                    id_type_model=tp_mt, id_product=res_to_add
                                )
                            )

                        if pandas.notna(row["Фото"]):
                            row["Фото"] = row["Фото"].replace("[", "")
                            row["Фото"] = row["Фото"].replace("]", "")
                            row["Фото"] = row["Фото"].replace("'", "")
                            photos = row["Фото"].split(", ")
                            for photo in photos:
                                filename = photo.split("/")[-2]
                                is_saved = (
                                    await FileS3Manager().upload_file_from_url(
                                        url_file=photo,
                                        file_name=filename
                                        + "".join(  # noqa
                                            [
                                                str(random.randint(1, 100))
                                                for _ in range(
                                                    1, random.randint(5, 30)
                                                )
                                            ]
                                        )
                                        + ".jpeg",  # noqa
                                        directory=S3EnumStorage.PRODUCTS.value,
                                    )
                                )

                                if is_saved:
                                    await session.photos_repository.add_one(
                                        data=ProductPhotos(
                                            photo_url=is_saved,
                                            id_product=res_to_add,
                                        )
                                    )

                        AdminPanelService.id_product = res_to_add
                        await AdminPanelService.add_product_model(
                            engine=session
                        )

                        cnt_to_add += 1
                    cnt_row += 1
            except KeyError:
                request.session["error_message"] = (
                    "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не удалось обработать файл"
                )
                return RedirectResponse(
                    url=f"/admin/{data_to_response}/list",
                    status_code=status.HTTP_303_SEE_OTHER,
                )
            else:
                if cnt_row == cnt_to_add - 1:
                    return RedirectResponse(
                        url="/admin", status_code=status.HTTP_303_SEE_OTHER
                    )
                else:
                    request.session["warning_message"] = (
                        f"Удалось добавить {cnt_to_add} из"
                        f" {cnt_row} записей"
                    )
                    return RedirectResponse(
                        url=f"/admin/{data_to_response}/list",
                        status_code=status.HTTP_303_SEE_OTHER,
                    )

    @staticmethod
    async def add_category(  # noqa
        request: Request,
        file: pandas.DataFrame,
        session: EngineRepository,
        data_to_response: str,
    ) -> Response:
        cnt_to_add: int = 0
        cnt_row: int = 0

        async with session:
            session: EngineRepository = session
            try:
                for index, row in file.itertuples():
                    name_category, image = row["Категория"], row["Фото"]
                    res_to_add = await session.category_repository.add_one(
                        Category(
                            name_category=name_category,
                            icon_category=image if image else "Неопределенно",
                        )
                    )
                    if res_to_add:
                        cnt_to_add += 1
                    cnt_row += 1
            except KeyError:
                request.session["error_message"] = (
                    "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не удалось обработать файл"
                )
                return RedirectResponse(
                    url=f"/admin/{data_to_response}/list",
                    status_code=status.HTTP_303_SEE_OTHER,
                )
            except ValueError:
                request.session["error_message"] = (
                    "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не верный формат файла"
                )
                return RedirectResponse(
                    url=f"/admin/{data_to_response}/list",
                    status_code=status.HTTP_303_SEE_OTHER,
                )
            else:
                if cnt_row == cnt_to_add - 1:
                    return RedirectResponse(
                        url="/admin", status_code=status.HTTP_303_SEE_OTHER
                    )
                else:
                    request.session["warning_message"] = (
                        f"Удалось добавить {cnt_to_add} из {cnt_row} записей"
                    )
                    return RedirectResponse(
                        url=f"/admin/{data_to_response}/list",
                        status_code=status.HTTP_303_SEE_OTHER,
                    )

    @staticmethod
    async def add_sub_category(
        request: Request,
        file: pandas.DataFrame,
        session: EngineRepository,
        data_to_response: str,
    ) -> Response:

        cnt_to_add: int = 0
        cnt_row: int = 0

        async with session:
            session: EngineRepository = session
            try:
                for index, row in file.iterrows():
                    res_to_add = await session.subcategory_repository.add_one(
                        SubCategory(
                            name=row.get("Подкатегория"),
                            id_category=row.get("Категория"),
                        )
                    )
                if res_to_add:
                    cnt_to_add += 1
                cnt_row += 1
            except KeyError:
                request.session["error_message"] = (
                    "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не удалось обработать файл"
                )
                return RedirectResponse(
                    url=f"/admin/{data_to_response}/list",
                    status_code=status.HTTP_303_SEE_OTHER,
                )
            else:
                if cnt_row == cnt_to_add - 1:
                    return RedirectResponse(
                        url="/admin", status_code=status.HTTP_303_SEE_OTHER
                    )
                else:
                    request.session["warning_message"] = (
                        f"Удалось добавить "
                        f"{cnt_to_add} из {cnt_row - 1} записей"
                    )
                    return RedirectResponse(
                        url=f"/admin/{data_to_response}/list",
                        status_code=status.HTTP_303_SEE_OTHER,
                    )

    @classmethod
    async def add_new_model(
        cls, line: str, engine: EngineRepository, id_mark: int
    ) -> None:
        for line_data in line.split(";"):
            find_model = await engine.model_repository.find_by_name(
                name_model=line_data
            )

            if not find_model:
                new_model = await engine.model_repository.add_one(
                    data=Model(name_model=line_data, id_mark=id_mark)
                )
                if new_model:
                    cls.lst_to_add_product_models.append(new_model)

    @classmethod
    async def add_product_model(cls, engine: EngineRepository) -> None:
        for el in cls.lst_to_add_product_models:
            await engine.product_models_repository.add_one(
                data=ProductModels(id_product=cls.id_product, id_model=el)
            )

        cls.lst_to_add_product_models.clear()
        cls.id_product = None

    @staticmethod
    async def add_mark(name_mark: str, engine: EngineRepository) -> None:
        return await engine.mark_repository.add_one(
            data=Mark(name_mark=name_mark)
        ).id

    @staticmethod
    async def update_product(
        request, engine: EngineRepository, file: pandas.DataFrame
    ):
        cnt_to_update: int = 0
        cnt_result_update: int = 0

        async with engine:
            for index, row in file.iterrows():
                product_data = (
                    await engine.product_repository.find_product_by_name(
                        name_product=row["Наименование товара"]
                    )
                )
                if product_data:
                    product_data = product_data[0].id
                    is_updated = await engine.product_repository.update_one(
                        other_id=product_data,
                        data_to_update={
                            "price_with_discount": row[
                                "Текущая цена с учетом скидки, ₽"
                            ],
                            "price_product": row[
                                "Цена до скидки (перечеркнутая цена), ₽"
                            ],
                            "quantity_product": row[
                                "Доступно к продаже по схеме FBS, шт."
                            ],
                        },
                    )

                    if is_updated:
                        cnt_result_update += 1
                cnt_to_update += 1

        request.session["warning_message"] = (
            f"Удалось обновить "
            f"{cnt_result_update} из {cnt_result_update} записей"
        )
        return RedirectResponse(
            url="/admin/product/list",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    @staticmethod
    async def update_category(  # noqa
        request: Request,
        file: pandas.DataFrame,
        session: EngineRepository,
        data_to_response: str,
    ) -> Response:
        cnt_to_update: int = 0
        cnt_row: int = 0

        async with session:
            session: EngineRepository = session
            try:
                for index, row in file.itertuples():
                    name_category, image = row["Категория"], row["Фото"]

                    category = await session.category_repository.find_by_name(
                        category_name=name_category, type_find=True
                    )

                    if category:
                        category = category[0].id

                        is_updated = (
                            await session.category_repository.update_one(
                                other_id=category,
                                data_to_update={"icon_category": image},
                            )
                        )

                        if is_updated:
                            cnt_to_update += 1
                    cnt_row += 1

            except KeyError as k:
                request.session["error_message"] = (
                    "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не удалось обработать файл"
                )
                return RedirectResponse(
                    url=f"/admin/{data_to_response}/list",
                    status_code=status.HTTP_303_SEE_OTHER,
                )
            except ValueError:
                request.session["error_message"] = (
                    "ОШИБКА ОБРАБОТКИ ФАЙЛА: Не верный формат файла"
                )
                return RedirectResponse(
                    url=f"/admin/{data_to_response}/list",
                    status_code=status.HTTP_303_SEE_OTHER,
                )
            else:
                if cnt_row == cnt_to_update - 1:
                    return RedirectResponse(
                        url="/admin", status_code=status.HTTP_303_SEE_OTHER
                    )
                else:
                    request.session["warning_message"] = (
                        f"Удалось обновить {cnt_to_update} из {cnt_row} записей"
                    )
                    return RedirectResponse(
                        url=f"/admin/{data_to_response}/list",
                        status_code=status.HTTP_303_SEE_OTHER,
                    )
