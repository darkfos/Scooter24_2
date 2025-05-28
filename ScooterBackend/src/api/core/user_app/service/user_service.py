from typing import Union, Type, Callable

from src.api.authentication.secret.secret_upd_key import SecretKey
from src.api.core.order_app.schemas.order_dto import OrderBase

from src.api.core.user_app.schemas.user_dto import (
    AddUser,
    InformationAboutUser,
    AllDataUser,
    UserReviewData,
    UserFavouritesData,
    UserOrdersData,
    UserIsUpdated,
    DataToUpdate,
    UserIsDeleted,
    BuyingOrders,
)
from src.api.core.auth_app.schemas.auth_dto import UpdateUserPassword
from src.api.core.auth_app.schemas.auth_dto import RegistrationUser
from src.database.models.user import User
from src.api.core.user_app.error.http_user_exception import UserHttpError
from src.api.authentication.hash_service.hashing import CryptographyScooter
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository
from src.other.enums.auth_enum import AuthenticationEnum
from src.other.enums.user_type_enum import UserTypeEnum
import logging as logger

from src.store.tools import RedisTools

from src.other.broker.producer.producer import (
    send_message_update_password_on_email,
)
from src.other.broker.dto.email_dto import EmailData

redis: Type[RedisTools] = RedisTools()
auth: Authentication = Authentication()
logging = logger.getLogger(__name__)


class UserService:

    @staticmethod
    async def create_a_new_user(
        engine: IEngineRepository,
        new_user: AddUser,
        bt: Callable,
        func_to_bt: Callable,
    ) -> RegistrationUser:
        """
        Метод сервиса для создания пользователя
        :param engine:
        :param new_user:
        :return:
        """

        logging.info(msg=f"{UserService.__name__} Создание пользователя")

        hashed_password: (
            CryptographyScooter
        ) = CryptographyScooter().hashed_password(
            password=new_user.password_user
        )

        async with engine:
            res_to_add_new_user: User = await engine.user_repository.add_one(
                User(
                    is_active=False,
                    id_type_user=UserTypeEnum.USER.value,
                    email_user=new_user.email_user,
                    password_user=hashed_password,
                    name_user=new_user.name_user,
                    main_name_user=new_user.main_name_user,
                    date_registration=new_user.date_registration,
                    date_update=new_user.date_registration,
                )
            )
            if res_to_add_new_user:

                secret_user_key: str | None = await func_to_bt(
                    engine=engine, new_user=new_user
                )

                if secret_user_key:
                    await bt(
                        EmailData(
                            email=new_user.email_user,
                            secret_key=secret_user_key,
                        )
                    )
                    return

            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось создать пользователя"
            )
            await UserHttpError().http_failed_to_create_a_new_user()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def get_information_about_me(
        engine: IEngineRepository, token: str, token_data: dict = dict()
    ) -> InformationAboutUser:
        """
        Метож сервиса для получения информации о пользователе по токену
        :param session:
        :param token:
        :return:
        """

        logging.info(
            msg=f"{UserService.__name__} " f"Получение информации пользователе"
        )

        async with engine:
            user_data: Union[User, None] = (
                await engine.user_repository.find_one(
                    other_id=int(token_data.get("sub"))
                )
            )[0]
            if user_data:
                information = InformationAboutUser(
                    email_user=user_data.email_user,
                    name_user=(
                        user_data.name_user if user_data.name_user else ""
                    ),
                    main_name_user=user_data.main_name_user,
                    date_registration=user_data.date_registration,
                    date_birthday=user_data.date_birthday,
                    telephone=user_data.telephone,
                    address_city=user_data.address_city,
                    address=user_data.address,
                )

                return information
            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось получить информацию"
                f" о пользователе, пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @redis
    @staticmethod
    async def get_information_about_user(
        engine: IEngineRepository,
        user_id: int,
        token: str,
        redis_search_data: str,
        token_data: dict = dict(),
    ) -> InformationAboutUser:
        """
        Метод сервиса для получения информации
        о пользователе по токену
        :param session:
        :param token:
        :return:
        """

        logging.info(
            msg=f"{UserService.__name__} "
            f"Получение информации о пользователе"
        )

        async with engine:

            if token_data.get("is_admin"):
                user_data: list[User] = await engine.user_repository.find_one(
                    other_id=user_id
                )

                if user_data:
                    user_data: User = user_data[0]

                    return InformationAboutUser(
                        email_user=user_data.email_user,
                        name_user=user_data.name_user,
                        main_name_user=user_data.main_name_user,
                        date_registration=user_data.date_registration,
                        address=user_data.address,
                        telephone=user_data.telephone,
                        date_birthday=user_data.date_birthday,
                    )

                await UserHttpError().http_user_not_found()

            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось получить информацию о"
                f" пользователе, пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @redis
    @staticmethod
    async def get_information_about_me_and_review(
        engine: IEngineRepository,
        token: str,
        redis_search_data: str,
        token_data: dict = dict(),
    ) -> UserReviewData:
        """
        Метод сервиса для получения информации о пользователе
        + его отзывы
        :param session:
        :param token:
        :return:
        """

        logging.info(
            msg=f"{UserService.__name__} "
            f"Получение информации о пользователе и его отзывах"
        )

        async with engine:
            user_data: Union[User, None] = (
                await engine.user_repository.find_user_and_get_reviews(
                    user_id=int(token_data.get("sub"))
                )
            )

            if user_data:
                return UserReviewData(
                    email_user=user_data.email_user,
                    name_user=user_data.name_user,
                    main_name_user=user_data.main_name_user,
                    date_registration=user_data.date_registration,
                    address=user_data.address,
                    telephone=user_data.telephone,
                    date_birthday=user_data.date_birthday,
                    reviews=[
                        review.read_model() for review in user_data.reviews
                    ],
                )
            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось получить информацию"
                f" о пользователе и его отзывах,"
                f" пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @redis
    @staticmethod
    async def get_information_about_me_and_favourite(
        engine: IEngineRepository,
        token: str,
        redis_search_data: str,
        token_data: dict = dict(),
    ) -> UserFavouritesData:
        """
        Метод сервиса для получения информации о пользователе
        + его товары в избранном
        :param session:
        :param token:
        :return:
        """

        logging.info(
            msg=f"{UserService.__name__} "
            f"Получение информации о пользователе"
            f" и его избранных товарах"
        )

        async with engine:
            user_data: Union[User, None] = (
                await engine.user_repository.find_user_and_get_favourites(
                    user_id=int(token_data.get("sub"))
                )
            )

            if user_data:
                return UserFavouritesData(
                    email_user=user_data.email_user,
                    name_user=user_data.name_user,
                    main_name_user=user_data.main_name_user,
                    date_registration=user_data.date_registration,
                    favourites=[
                        favourite.read_model()
                        for favourite in user_data.favourites_user
                    ],
                    date_birthday=user_data.date_birthday,
                    telephone=user_data.telephone,
                    address=user_data.address,
                )
            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось получить информацию"
                f" о пользователе"
                f" и его избранных товарах,"
                f" пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @redis
    @staticmethod
    async def get_information_about_me_and_orders(
        engine: IEngineRepository,
        token: str,
        redis_search_data: str,
        token_data: dict = dict(),
    ) -> UserOrdersData:
        """
        Метод сервиса для получения информации о пользователе + его заказы
        :param session:
        :param token:
        :return:
        """

        logging.info(
            msg=f"{UserService.__name__} "
            f"Получение информации о пользователе"
            f" и его заказах"
        )

        async with engine:
            orders: Union[list[tuple[User]], None] = (
                await engine.user_repository.find_user_and_get_orders(
                    user_id=int(token_data.get("sub"))
                )
            )

            if orders:
                return BuyingOrders(
                    orders=[
                        OrderBase(
                            product_data=[
                                {
                                    "id_product": product.id_product,
                                    "title_product": product.product_data.title_product,
                                    "quantity_buy": product.count_product,
                                    "price": product.price,
                                }
                                for product in order[0].product_list
                            ],
                            order_data={
                                "id": order[0].id,
                                "price": order[0].price_result,
                                "date_buy": order[0].date_buy,
                                "type_operation": order[0].type_operation,
                                "type_buy": order[0].type_buy,
                                "type_delivery": order[0].delivery_method,
                            },
                        )
                        for order in orders
                    ]
                )
            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось получить информацию"
                f" о пользователе"
                f" и его заказах, пользователь не"
                f" был найден"
            )

            return BuyingOrders(orders=[])

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def user_success_orders(
        engine: IEngineRepository, token: str, token_data: dict = {}
    ) -> BuyingOrders:
        """
        Метод сервиса для получения всех успешных (оплаченных)
        заказов пользователя
        :param engine:
        :param token:
        :param token_data:
        :return:
        """

        async with engine:
            user_orders = await engine.user_repository.success_user_orders(
                user_id=int(token_data.get("sub"))
            )

            if user_orders:
                return BuyingOrders(
                    orders=[
                        OrderBase(
                            product_data=[
                                {
                                    "id_product": product.id_product,
                                    "title_product": product.product_data.title_product,
                                    "quantity_buy": product.count_product,
                                    "price": product.price,
                                }
                                for product in order[0].product_list
                            ],
                            order_data={
                                "id": order[0].id,
                                "price": order[0].price_result,
                                "date_buy": order[0].date_buy,
                                "type_operation": order[0].type_operation,
                                "type_buy": order[0].type_buy,
                                "type_delivery": order[0].delivery_method,
                            },
                        )
                        for order in user_orders
                    ]
                )
            else:
                return BuyingOrders(orders=[])

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @redis
    @staticmethod
    async def get_full_information(
        engine: IEngineRepository,
        token: str,
        redis_search_data: str,
        token_data: dict = dict(),
    ) -> AllDataUser:
        """
        Метод сервиса для получения полной информации о пользователе
        :param session:
        :param token:
        :return:
        """

        logging.info(msg="Получение полной информации о пользователе")

        user_id: int = int(token_data.get("sub"))

        async with engine:
            user_all_information: Union[User, None] = (
                await engine.user_repository.find_user_and_get_full_information(
                    user_id=user_id
                )
            )

            if user_all_information:
                return AllDataUser(
                    general_user_info=InformationAboutUser(
                        email_user=user_all_information.email_user,
                        name_user=user_all_information.name_user,
                        main_name_user=user_all_information.main_name_user,
                        date_registration=user_all_information.date_registration,  # noqa
                        date_birthday=user_all_information.date_birthday,
                        address_city=user_all_information.address_city,
                        address=user_all_information.address,
                        telephone=user_all_information.telephone,
                    ),
                    orders=[
                        order.read_model()
                        for order in user_all_information.orders_user
                    ],
                    favourite=[
                        fav.read_model()
                        for fav in user_all_information.favourites_user
                    ],
                    reviews=[
                        review.read_model()
                        for review in user_all_information.reviews
                    ],
                )

            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось получить информацию"
                f" о пользователе, пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def get_full_information_other_user(
        engine: IEngineRepository,
        user_id: int,
        token: str,
        token_data: dict = dict(),
    ) -> AllDataUser:
        """
        Метод сервиса для получения полной информации о других пользователях
        :param session:
        :param user_id:
        :param admin_password:
        :return:
        """

        logging.info(
            msg=f"{UserService.__name__} "
            f"Получение полной информации о других пользователях"
        )

        async with engine:
            is_admin: bool = await engine.user_repository.find_admin(
                id_=int(token_data.get("sub"))
            )

            if is_admin and token_data.get("is_admin"):
                user_all_information: Union[None, User] = (
                    await engine.user_repository.find_user_and_get_full_information(  # noqa
                        user_id=user_id
                    )
                )  # noqa

                if user_all_information:
                    return AllDataUser(
                        general_user_info=InformationAboutUser(
                            address=user_all_information.address,
                            telephone=user_all_information.telephone,
                            date_birthday=user_all_information.date_birthday,
                            email_user=user_all_information.email_user,
                            name_user=user_all_information.name_user,
                            main_name_user=user_all_information.main_name_user,  # noqa
                            date_registration=user_all_information.date_registration,  # noqa
                        ),
                        orders=[
                            order.read_model()
                            for order in user_all_information.orders_user
                        ],
                        favourite=[
                            fav.read_model()
                            for fav in user_all_information.favourites_user
                        ],  # noqa
                        reviews=[
                            review.read_model()
                            for review in user_all_information.reviews
                        ],
                    )

            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось получить полную "
                f"информацию о других пользователях"
            )
            await UserHttpError().http_user_not_found()

    @staticmethod
    async def user_is_created(
        engine: IEngineRepository, email: str, password: str
    ) -> bool:
        """
        Метод сервиса для поиска пользователя с указанной почтой и паролем
        :param session:
        :param email:
        :return:
        """

        logging.info(
            msg=f"{UserService.__name__} Поиск пользователя"
            f" по почте и паролю"
        )
        async with engine:
            result_find_user: Union[bool, User] = (
                await engine.user_repository.find_user_by_email_and_password(
                    email=email
                )
            )

            if result_find_user:
                CryptographyScooter().verify_password(
                    password=password,
                    hashed_password=result_find_user.password_user,
                )

            return result_find_user

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def update_user_information(
        engine: IEngineRepository,
        token: str,
        to_update: DataToUpdate,
        token_data: dict = dict(),
    ) -> UserIsUpdated:
        """
        Метод сервиса для обновления данных о пользователе
        :param session:
        :param token:
        :param to_update:
        :return:
        """

        logging.info(
            msg=f"{UserService.__name__} " f"Обновление данных о пользователе"
        )

        async with engine:
            return UserIsUpdated(
                is_updated=await engine.user_repository.update_one(
                    other_id=int(token_data.get("sub")),
                    data_to_update={
                        k: v
                        for k, v in to_update.dict().items()
                        if v not in ("", None)
                    },
                )
            )

        logging.info(
            msg=f"{UserService.__name__} "
            f"Не удалось обновить данные"
            f" о пользователе, пользователь не был найден"
        )
        await UserHttpError().http_user_not_found()

    @staticmethod
    async def update_user_password(
        engine: IEngineRepository,
        to_update: UpdateUserPassword,
    ) -> None:
        """
        Метод сервиса для обновления пароля пользователя
        :param session:
        :param token:
        :param to_update:
        :return:
        """

        logging.info(
            msg=f"{UserService.__name__} " f"Обновление пароля пользователя"
        )
        crypt = CryptographyScooter()

        async with engine:
            user_data: Union[User, None] = (
                await engine.user_repository.find_user_by_email_and_password(
                    email=to_update.email
                )
            )

            if user_data:
                check_password = crypt.verify_password(
                    password=to_update.old_password,
                    hashed_password=user_data.password_user,
                )

                if check_password:

                    secret_update_code = SecretKey().generate_password()

                    if secret_update_code:
                        await engine.user_repository.update_one(
                            other_id=user_data.id,
                            data_to_update={
                                "secret_update_key": secret_update_code
                            },
                        )

                        return await send_message_update_password_on_email(
                            email_data=EmailData(
                                email=to_update.email,
                                secret_key=secret_update_code,
                            )
                        )

                logging.critical(
                    msg=f"{UserService.__name__} "
                    f"Не удалось обновить "
                    f"пароль пользователя"
                )
                await UserHttpError().http_failed_to_update_user_information()
            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось обновить пароль"
                f" пользователя, пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def delete_user(
        engine: IEngineRepository, token: str, token_data: dict = dict()
    ) -> UserIsDeleted:
        """
        Метод сервиса для удаления всех данных пользователя
        :param session:
        :param token:
        :return:
        """

        logging.info(msg=f"{UserService.__name__} Удаление пользователя")

        async with engine:
            res_del = await engine.user_repository.delete_one(
                other_id=int(token_data.get("sub"))
            )
            if res_del:
                return UserIsDeleted(is_deleted=res_del)
            logging.info(
                msg=f"{UserService.__name__} "
                f"Не удалось обновить пользователя"
            )
            await UserHttpError().http_failed_to_delete_user()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def check_secret_key(
        engine: IEngineRepository,
        secret_key: str,
        token: str,
        new_password: str,
        token_data: dict = dict(),
    ) -> None:
        """
        Проверка секретного ключа для обновления пароля
        :email:
        """

        logging.info(msg=f"{UserService.__name__} Проверка секретного ключа")

        async with engine:
            user_data: User = (
                await engine.user_repository.find_one(
                    other_id=token_data.get("id_user")
                )
            )[0]

            if user_data:
                if user_data.secret_update_key == secret_key:
                    is_updated: bool = await engine.user_repository.update_one(
                        other_id=token_data.get("id_user"),
                        data_to_update={"secret_update_key": ""},
                    )

                    if is_updated:
                        password_is_updated: bool = (
                            await engine.user_repository.update_one(
                                other_id=token_data.get("id_user"),
                                data_to_update={
                                    "password_user": (
                                        CryptographyScooter().hashed_password(
                                            new_password
                                        )
                                    )
                                },
                            )
                        )
                        if password_is_updated:
                            return
            logging.critical(
                msg=f"{UserService.__name__} Не удалось "
                f"обновить пароль пользователя"
            )
            await UserHttpError().http_failed_to_update_user_information()

    @staticmethod
    async def access_update_user_password(
        engine: IEngineRepository,
        update_data: UpdateUserPassword,
        secret_key: str,
    ) -> None:

        async with engine:
            user_data = (
                await engine.user_repository.find_user_by_email_and_password(
                    email=update_data.email
                )
            )

            logging.info(
                msg="Подверждение обновления пароля пользователя по email={}".format(
                    update_data.email
                )
            )

            if user_data:
                if user_data.secret_update_key == secret_key:
                    new_hashed_password = (
                        CryptographyScooter().hashed_password(
                            password=update_data.new_password
                        )
                    )
                    is_updated = await engine.user_repository.update_one(
                        other_id=user_data.id,
                        data_to_update={
                            "secret_update_key": "",
                            "password_user": new_hashed_password,
                        },
                    )

                    if is_updated:
                        return

            await UserHttpError().http_update_password_error()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def update_auth_user_password(
        engine: IEngineRepository,
        password_data: UpdateUserPassword,
        token: str,
        token_data: dict = {},
    ) -> None:

        async with engine:
            user_data: Union[list[User], None] = (
                await engine.user_repository.find_one(
                    other_id=int(token_data.get("sub"))
                )
            )

            if user_data:

                verify_password = CryptographyScooter().verify_password(
                    password=password_data.old_password,
                    hashed_password=user_data[0].password_user,
                )

                if verify_password:
                    hashed_new_password = (
                        CryptographyScooter().hashed_password(
                            password=password_data.new_password
                        )
                    )

                    is_updated = await engine.user_repository.update_one(
                        other_id=int(token_data.get("sub")),
                        data_to_update={"password_user": hashed_new_password},
                    )

                    if is_updated:
                        return

            await UserHttpError().http_update_password_error()
