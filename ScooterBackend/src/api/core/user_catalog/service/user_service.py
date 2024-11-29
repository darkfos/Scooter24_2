# Other libraries
from typing import Union, Type, Callable

from fastapi import BackgroundTasks

# Local
from src.api.core.user_catalog.schemas.user_dto import (
    AddUser,
    InformationAboutUser,
    AllDataUser,
    UserReviewData,
    UserFavouritesData,
    UserOrdersData,
    UserHistoryData,
    UserIsUpdated,
    DataToUpdate,
    DataToUpdateUserPassword,
    UserIsDeleted,
    UpdateAddressDate,
)
from src.api.core.auth_catalog.schemas.auth_dto import RegistrationUser
from src.database.models.user import User
from src.api.core.user_catalog.error.http_user_exception import UserHttpError
from src.api.authentication.hash_service.hashing import CryptographyScooter
from src.api.authentication.secure.authentication_service import Authentication
from src.api.dep.dependencies import IEngineRepository
from src.other.enums.auth_enum import AuthenticationEnum
from src.other.enums.user_type_enum import UserTypeEnum
import logging as logger

# Redis
from src.store.tools import RedisTools

redis: Type[RedisTools] = RedisTools()
auth: Authentication = Authentication()
logging = logger.getLogger(__name__)


class UserService:

    @staticmethod
    async def create_a_new_user(
        engine: IEngineRepository,
        new_user: AddUser,
        bt: BackgroundTasks,
        func_to_bt: Callable,
    ) -> RegistrationUser:
        """
        Метод сервиса для создания пользователя
        :param engine:
        :param new_user:
        :return:
        """

        logging.info(msg=f"{UserService.__name__} Создание пользователя")
        # Hash password
        hashed_password: (
            CryptographyScooter
        ) = CryptographyScooter().hashed_password(
            password=new_user.password_user
        )

        async with engine:
            # Create a new user
            res_to_add_new_user = await engine.user_repository.add_one(
                User(
                    is_active=False,
                    id_type_user=UserTypeEnum.USER.value,
                    email_user=new_user.email_user,
                    password_user=hashed_password,
                    name_user=new_user.name_user,
                    surname_user=new_user.surname_user,
                    main_name_user=new_user.main_name_user,
                    date_registration=new_user.date_registration,
                    date_update=new_user.date_registration,
                )
            )
            if res_to_add_new_user:
                bt.add_task(func_to_bt, engine, new_user)
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
                    other_id=token_data.get("sub")
                )
            )[0]
            if user_data:
                information = InformationAboutUser(
                    email_user=user_data.email_user,
                    name_user=(
                        user_data.name_user if user_data.name_user else ""
                    ),
                    surname_user=(
                        user_data.surname_user if user_data.surname_user else ""
                    ),
                    main_name_user=user_data.main_name_user,
                    date_registration=user_data.date_registration,
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
            # Проверка на администратора
            is_admin: bool = await engine.user_repository.find_one(
                other_id=token_data.get("sub")
            )

            if is_admin and token_data.get("is_admin"):
                user_data: dict = is_admin[0]
                return InformationAboutUser(
                    email_user=user_data.email_user,
                    name_user=user_data.name_user,
                    surname_user=user_data.surname_user,
                    main_name_user=user_data.main_name_user,
                    date_registration=user_data.date_registration,
                )
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
                    user_id=token_data.get("sub")
                )
            )

            if user_data:
                return UserReviewData(
                    email_user=user_data.email_user,
                    name_user=user_data.name_user,
                    surname_user=user_data.surname_user,
                    main_name_user=user_data.main_name_user,
                    date_registration=user_data.date_registration,
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
                    user_id=token_data.get("sub")
                )
            )

            if user_data:
                return UserFavouritesData(
                    email_user=user_data.email_user,
                    name_user=user_data.name_user,
                    surname_user=user_data.surname_user,
                    main_name_user=user_data.main_name_user,
                    date_registration=user_data.date_registration,
                    favourites=user_data.favourites_user,
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
            user_data: Union[User, None] = (
                await engine.user_repository.find_user_and_get_orders(
                    user_id=token_data.get("sub")
                )
            )
            if user_data:
                return UserOrdersData(
                    email_user=user_data.email_user,
                    name_user=user_data.name_user,
                    surname_user=user_data.surname_user,
                    main_name_user=user_data.main_name_user,
                    date_registration=user_data.date_registration,
                    orders=[
                        {
                            "id_user": order.id_user,
                            "id_product": order.id_product,
                            "date_buy": order.date_buy,
                        }
                        for order in user_data.orders_user
                    ],
                )
            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось получить информацию"
                f" о пользователе"
                f" и его заказах, пользователь не"
                f" был найден"
            )
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @redis
    @staticmethod
    async def get_information_about_me_and_history(
        engine: IEngineRepository,
        token: str,
        redis_search_data: str,
        token_data: dict = dict(),
    ) -> UserHistoryData:
        """
        Метод сервиса для получения информации о пользователе + история заказов
        :param session:
        :param token:
        :return:
        """

        logging.info(
            msg=f"{UserService.__name__} Получение информации о "
            f"пользователе и его истории"
        )

        async with engine:
            user_data: Union[User, None] = (
                await engine.user_repository.find_user_and_get_history(
                    user_id=token_data.get("sub")
                )
            )

            if user_data:
                return UserHistoryData(
                    email_user=user_data.email_user,
                    name_user=user_data.name_user,
                    surname_user=user_data.surname_user,
                    main_name_user=user_data.main_name_user,
                    date_registration=user_data.date_registration,
                    history=user_data.history_buy_user,
                )
            logging.info(
                msg=f"{UserService.__name__} "
                f"Не удалось получить информацию"
                f" о пользователе и его истории,"
                f" пользователь не был найден"
            )
            await UserHttpError().http_user_not_found()

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

        # Getting user id
        user_id: int = token_data.get("sub")

        async with engine:
            user_all_information: Union[User, None] = (
                await engine.user_repository.find_user_and_get_full_information(
                    user_id=user_id
                )
            )

            if user_all_information:
                return AllDataUser(
                    email_user=user_all_information.email_user,
                    name_user=user_all_information.name_user,
                    surname_user=user_all_information.surname_user,
                    main_name_user=user_all_information.main_name_user,
                    date_registration=user_all_information.date_registration,
                    orders=[
                        order.read_model()
                        for order in user_all_information.orders_user
                    ],
                    favourite=[
                        fav.read_model()
                        for fav in user_all_information.favourites_user
                    ],
                    history=[
                        history.read_model()
                        for history in user_all_information.history_buy_user
                    ],
                    reviews=[
                        review.read_model()
                        for review in user_all_information.reviews
                    ],
                    address=UpdateAddressDate(
                        name_user_address=user_all_information.name_user_address,  # noqa
                        surname_user_address=user_all_information.surname_user_address,  # noqa
                        name_company_address=user_all_information.name_company_address,  # noqa
                        country_address=user_all_information.country_address,
                        address_street=user_all_information.address_street,
                        address_rl_et_home=user_all_information.address_rl_et_home,  # noqa
                        address_locality=user_all_information.address_locality,
                        address_area=user_all_information.address_area,
                        address_index=user_all_information.address_index,
                        address_phone_number=user_all_information.address_phone_number,  # noqa
                    ),
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
            # Проверка на администратора
            is_admin: bool = await engine.user_repository.find_one(
                other_id=token_data.get("sub")
            )

            if is_admin and token_data.get("is_admin"):
                user_all_information: Union[None, User] = (
                    await engine.user_repository.find_user_and_get_full_information(  # noqa
                        user_id=user_id
                    )
                )  # noqa

                if user_all_information:
                    return AllDataUser(
                        email_user=user_all_information.email_user,
                        name_user=user_all_information.name_user,
                        surname_user=user_all_information.surname_user,  # noqa
                        main_name_user=user_all_information.main_name_user,  # noqa
                        date_registration=user_all_information.date_registration,  # noqa
                        orders=user_all_information.orders_user,
                        favourite=user_all_information.favourites_user,  # noqa
                        history=user_all_information.history_buy_user,  # noqa
                        reviews=user_all_information.reviews,
                        address=UpdateAddressDate(
                            name_user_address=user_all_information.name_user_address,  # noqa
                            surname_user_address=user_all_information.surname_user_address,  # noqa
                            name_company_address=user_all_information.name_company_address,  # noqa
                            country_address=user_all_information.country_address,  # noqa
                            address_street=user_all_information.address_street,
                            address_rl_et_home=user_all_information.address_rl_et_home,  # noqa
                            address_locality=user_all_information.address_locality,  # noqa
                            address_area=user_all_information.address_area,
                            address_index=user_all_information.address_index,
                            address_phone_number=user_all_information.address_phone_number,  # noqa
                        ),
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
                # Проверка что пользователь создан
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
                    other_id=token_data.get("sub"),
                    data_to_update=to_update.model_dump(),
                )
            )

        logging.info(
            msg=f"{UserService.__name__} "
            f"Не удалось обновить данные"
            f" о пользователе, пользователь не был найден"
        )
        await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def update_user_password(
        engine: IEngineRepository,
        token: str,
        to_update: DataToUpdateUserPassword,
        token_data: dict = dict(),
    ) -> UserIsUpdated:
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
            # Проверка на совпадение пароля
            get_user_data: Union[User, None] = (
                await engine.user_repository.find_one(
                    other_id=token_data.get("id_user")
                )
            )
            if get_user_data:
                check_password = crypt.verify_password(
                    password=to_update.user_old_password,
                    hashed_password=get_user_data[0].password_user,
                )
                if check_password:
                    hash_password = crypt.hashed_password(
                        password=to_update.new_password
                    )
                    return UserIsUpdated(
                        is_updated=await engine.user_repository.update_one(
                            other_id=token_data.get("id_user"),
                            data_to_update={
                                "password_user": hash_password,
                                "date_update": to_update.date_update,
                            },
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
                other_id=token_data.get("id_user")
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

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def update_address_user_data(
        engine: IEngineRepository,
        token: str,
        data_update: UpdateAddressDate,
        token_data: dict = dict(),
    ) -> None:
        """
        Метод сервиса для обновления адресных данных пользователя
        :engine:
        :data_update:
        """
        logging.info(
            msg=f"{UserService.__name__} " f"Обновление данных пользователя"
        )

        async with engine:
            # Обновление данных
            is_updated: bool = await engine.user_repository.update_one(
                other_id=token_data.get("id_user"),
                data_to_update=data_update.model_dump(),
            )

            if is_updated:
                return True
            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось обновить данные пользователя"
            )
            await UserHttpError().http_failed_to_update_user_information()
