from starlette.responses import Response, RedirectResponse
from fastapi import status
from starlette.requests import Request
import pandas
from src.api.dep.dependencies import EngineRepository
from src.database.models.brand import Brand
from src.database.models.model import Model
from src.database.models.product_models import ProductModels
from src.database.models.sub_sub_category import SubSubCategory
from src.database.models.product import Product
from src.database.models.category import Category
from src.database.models.marks import Mark
from src.database.models.subcategory import SubCategory


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
        """
        Добавление новых продуктов
        """

        cnt_to_add: int = 0
        cnt_row: int = 0

        async with session:
            session: EngineRepository = session
            try:
                for index, row in file.iterrows():
                    category_data = id_subcat_1 = id_subcat_2 = (
                        None  # Initial data for fk
                    )

                    # Find fk in other tables
                    if str(row["Категория"]) not in (None, "nan"):
                        category_data: Category = (
                            await session.category_repository.find_by_name(
                                category_name=row["Категория"], type_find=True
                            )
                        )

                        if not category_data:
                            create_category = (
                                await session.category_repository.add_one(
                                    Category(
                                        name_category=row.get("Категория"),
                                        icon_category="icon",
                                    )
                                )
                            )
                            category_data = create_category

                    if str(row["Подкатегория первого уровня"]) not in (
                        None,
                        "nan",
                    ):
                        id_subcat_1: SubCategory = (
                            await session.subcategory_repository.find_by_name(
                                name_subcategory=row[
                                    "Подкатегория первого уровня"
                                ]
                            )
                        )

                        if not id_subcat_1:
                            create_subcat_1 = (
                                await session.subcategory_repository.add_one(
                                    SubCategory(
                                        name=row.get(
                                            "Подкатегория первого уровня"
                                        ),
                                        id_category=category_data,
                                    )
                                )
                            )
                            id_subcat_1 = create_subcat_1

                    if str(row["Подкатегория второго уровня"]) not in (
                        None,
                        "nan",
                    ):
                        id_subcat_2: SubCategory = (
                            await session.subcategory_repository.find_by_name(
                                name_subcategory=row[
                                    "Подкатегория второго уровня"
                                ]
                            )
                        )

                        if not id_subcat_2:
                            create_subcat_2 = await session.sub_subcategory_repository.add_one(  # noqa
                                data=SubSubCategory(
                                    name=row.get("Подкатегория второго уровня"),
                                    id_sub_category=id_subcat_1,
                                )
                            )
                            id_subcat_2 = create_subcat_2

                    if str(row.get("Бренд")) not in (None, "nan"):
                        id_brand = await session.brand_repository.find_by_name(
                            name_brand_to_find=row.get("Бренд"),
                        )

                        if not id_brand:
                            create_brand = (
                                await session.brand_repository.add_one(
                                    data=Brand(name_brand=row.get("Бренд"))
                                )
                            )
                            id_brand = create_brand

                    # Создание марок, моделей, бренда
                    if str(row.get("Марка")) not in (None, "nan"):
                        id_mark = await session.mark_repository.find_by_name(
                            name_mark=row.get("Марка")
                        )

                        if not id_mark:
                            create_mark = await session.mark_repository.add_one(
                                data=Mark(name_mark=row.get("Марка"))
                            )

                            id_mark = create_mark

                    if str(row.get("Модель")) not in (None, "nan"):
                        await AdminPanelService.add_new_model(
                            line=row.get("Модель"),
                            engine=session,
                            id_mark=id_mark,
                        )

                    # replace type of object
                    weight_product = float(
                        str(row["Объемный вес, кг"]).replace("'", "")
                    )
                    quantity_product = int(
                        row["Доступно к продаже по схеме FBS, шт."]
                    )
                    price_product = float(
                        row["Цена до скидки (перечеркнутая цена), ₽"]
                    )
                    price_with_discount = float(
                        row["Текущая цена с учетом скидки, ₽"]
                    )

                    res_to_add = await session.product_repository.add_one(
                        Product(
                            article_product=row["Артикул"],
                            title_product=row["Наименование товара"],
                            brand=id_brand,
                            weight_product=weight_product,
                            id_s_sub_category=id_subcat_2,
                            explanation_product=(
                                row["Описание"]
                                if str(row["Описание"]) not in (None, "nan")
                                else "Неопределен"
                            ),
                            brand_mark=id_mark,
                            photo_product=(
                                row["Фото"]
                                if str(row["Фото"]) not in (None, "nan")
                                else "Неопределен"
                            ),
                            quantity_product=quantity_product,
                            price_product=price_product,
                            price_with_discount=price_with_discount,
                            product_discount=0,
                        )
                    )
                    if res_to_add:

                        # Создание моделей продукта
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
        """
        Добавление новых категорий
        """

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
        """
        Добавление новых подкатегорий
        """

        cnt_to_add: int = 0
        cnt_row: int = 0

        async with session:
            session: EngineRepository = session
            try:
                for index, row in file.iterrows():
                    res_to_add = await session.subcategory_repository.add_one(
                        SubCategory(
                            name=row.get("Подкатегория"),
                            level=row.get("Уровень"),
                            id_category=row.get("Категория"),
                            id_sub_category=row.get("П. подкатегории"),
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
        """
        Добавление новой модели
        """

        for line_data in line.split(";"):
            find_model = await engine.model_repository.find_by_name(
                name_model=line_data
            )

            if not find_model:
                new_model = await engine.model_repository.add_one(
                    data=Model(name_model=line_data, id_mark=id_mark)
                )
                print("#" * 30)
                print(line_data, new_model, find_model, id_mark)
                print("#" * 30)

                if new_model:
                    cls.lst_to_add_product_models.append(new_model)

    @classmethod
    async def add_product_model(cls, engine: EngineRepository) -> None:
        """
        Добавление новой модели для продукта
        """

        for el in cls.lst_to_add_product_models:
            await engine.product_models_repository.add_one(
                data=ProductModels(id_product=cls.id_product, id_model=el)
            )

        cls.lst_to_add_product_models.clear()
        cls.id_product = None

    @staticmethod
    async def add_mark(name_mark: str, engine: EngineRepository) -> None:
        """
        Добавление новой марки
        """

        return await engine.mark_repository.add_one(
            data=Mark(name_mark=name_mark)
        ).id

    @staticmethod
    async def update_product(
        request, engine: EngineRepository, file: pandas.DataFrame
    ):
        """
        Обновление данных в файле
        """

        cnt_to_update: int = 0
        cnt_result_update: int = 0

        async with engine:
            for index, row in file.iterrows():
                # Поиск товара по названию
                product_data = (
                    await engine.product_repository.find_product_by_name(
                        name_product=row["Наименование товара"]
                    )
                )
                if product_data:
                    product_data = product_data[0].id
                    # Обновление данных
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
        """
        Добавление новых категорий
        """

        cnt_to_update: int = 0
        cnt_row: int = 0

        async with session:
            session: EngineRepository = session
            try:
                for index, row in file.itertuples():
                    name_category, image = row["Категория"], row["Фото"]

                    # Поиск категории
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
