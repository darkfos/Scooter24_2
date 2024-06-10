#Other libraries
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession

#Local
from ScooterBackend.api.dto.user_dto import (
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
    UserIsDeleted
)
from ScooterBackend.api.dto.auth_dto import RegistrationUser
from ScooterBackend.database.repository.user_repository import UserRepository
from ScooterBackend.database.models.user import User
from ScooterBackend.api.exception.http_user_exception import UserHttpError
from ScooterBackend.api.authentication.hashing import CryptographyScooter
from ScooterBackend.api.authentication.authentication_service import Authentication
from ScooterBackend.database.repository.admin_repository import AdminRepository


class UserService:

    @staticmethod
    async def create_a_new_user(session: AsyncSession, new_user: AddUser) -> RegistrationUser:
        """
        Метод сервиса для создания пользователя
        :param session:
        :param new_user:
        :return:
        """

        #Hash password
        hashed_password = CryptographyScooter().hashed_password(password=new_user.password_user)

        #Create a new user
        res_to_add_new_user: bool = await UserRepository(session=session).add_one(
            data=User(
                email_user=new_user.email_user,
                password_user=hashed_password,
                name_user=new_user.name_user,
                surname_user=new_user.surname_user,
                main_name_user=new_user.main_name_user))
        if res_to_add_new_user is True:
            return RegistrationUser(is_registry=res_to_add_new_user)
        await UserHttpError().http_failed_to_create_a_new_user()

    @staticmethod
    async def get_information_about_me(session: AsyncSession, token: str) -> InformationAboutUser:
        """
        Метож сервиса для получения информации о пользователе по токену
        :param session:
        :param token:
        :return:
        """

        #Getting user id
        jwt_data: dict = await Authentication().decode_jwt_token(token=token, type_token="access")
        user_data: Union[User, None] = (await UserRepository(session=session).find_one(other_id=jwt_data.get("id_user")))[0]
        if user_data:
            return InformationAboutUser(
                email_user=user_data.email_user,
                name_user=user_data.name_user,
                surname_user=user_data.surname_user,
                main_name_user=user_data.main_name_user
            )

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_information_about_user(session: AsyncSession, user_id: int, token: str) -> InformationAboutUser:
        """
        Метод сервиса для получения информации о пользователе по токену
        :param session:
        :param token:
        :return:
        """

        #Получение данных токена
        jwt_data: dict = await Authentication().decode_jwt_token(token=token, type_token="access")

        #Проверка на администратора
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(email=jwt_data.get("email"))

        if is_admin:
            user_data: Union[None, User] = await UserRepository(session=session).find_one(other_id=user_id)
            if user_data:
                return InformationAboutUser(
                    email_user=user_data[0].email_user,
                    name_user=user_data[0].name_user,
                    surname_user=user_data[0].surname_user,
                    main_name_user=user_data[0].main_name_user
                )

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_information_about_me_and_review(session: AsyncSession, token: str) -> UserReviewData:
        """
        Метод сервиса для получения информации о пользователе + его отзывы
        :param session:
        :param token:
        :return:
        """

        #Getting user_id
        jwt_data = await Authentication().decode_jwt_token(token=token, type_token="access")
        user_data: Union[User, None] = await UserRepository(session=session).find_user_and_get_reviews(user_id=jwt_data.get("id_user"))

        if user_data:
            return UserReviewData(
                email_user=user_data.email_user,
                name_user=user_data.name_user,
                surname_user=user_data.surname_user,
                main_name_user=user_data.main_name_user,
                reviews=user_data.reviews
            )

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_information_about_me_and_favourite(session: AsyncSession, token: str) -> UserFavouritesData:
        """
        Метод сервиса для получения информации о пользователе + его товары в избранном
        :param session:
        :param token:
        :return:
        """

        #Getting user_id
        jwt_data = await Authentication().decode_jwt_token(token=token, type_token="access")
        user_data: Union[User, None] = await UserRepository(session=session).find_user_and_get_favourites(user_id=jwt_data.get("id_user"))

        if user_data:
            return UserFavouritesData(
                email_user=user_data.email_user,
                name_user=user_data.name_user,
                surname_user=user_data.surname_user,
                main_name_user=user_data.main_name_user,
                favourites=user_data.favourites_user
            )

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_information_about_me_and_orders(session: AsyncSession, token: str) -> UserOrdersData:
        """
        Метод сервиса для получения информации о пользователе + его заказы
        :param session:
        :param token:
        :return:
        """

        #Getting user_id
        jwt_data = await Authentication().decode_jwt_token(token=token, type_token="access")
        user_data: Union[User, None] = await UserRepository(session=session).find_user_and_get_orders(user_id=jwt_data.get("id_user"))

        if user_data:
            return UserOrdersData(
                email_user=user_data.email_user,
                name_user=user_data.name_user,
                surname_user=user_data.surname_user,
                main_name_user=user_data.main_name_user,
                orders=user_data.orders_user
            )

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_information_about_me_and_history(session: AsyncSession, token: str) -> UserHistoryData:
        """
        Метод сервиса для получения информации о пользователе + история заказов
        :param session:
        :param token:
        :return:
        """

        #Getting user_id
        jwt_data = await Authentication().decode_jwt_token(token=token, type_token="access")
        user_data: Union[User, None] = await UserRepository(session=session).find_user_and_get_history(user_id=jwt_data.get("id_user"))

        if user_data:
            return UserHistoryData(
                email_user=user_data.email_user,
                name_user=user_data.name_user,
                surname_user=user_data.surname_user,
                main_name_user=user_data.main_name_user,
                history=user_data.history_buy_user
            )

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_full_information(session: AsyncSession, token: str) -> AllDataUser:
        """
        Метод сервиса для получения полной информации о пользователе
        :param session:
        :param token:
        :return:
        """

        #Getting user id
        user_id: int = (await Authentication().decode_jwt_token(token=token, type_token="access")).get("id_user")
        user_all_information: Union[User, None] = await UserRepository(session=session).find_user_and_get_full_information(user_id=user_id)
        print(user_all_information)

        if user_all_information:
            return AllDataUser(
                email_user=user_all_information.email_user,
                name_user=user_all_information.name_user,
                surname_user=user_all_information.surname_user,
                main_name_user=user_all_information.main_name_user,
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
                ]
            )

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def get_full_information_other_user(session: AsyncSession, user_id: int, token: str) -> AllDataUser:
        """
        Метод сервиса для получения полной информации о других пользователях
        :param session:
        :param user_id:
        :param admin_password:
        :return:
        """

        # Получение данных токена
        jwt_data: dict = await Authentication().decode_jwt_token(token=token, type_token="access")

        # Проверка на администратора
        is_admin: bool = await AdminRepository(session=session).find_admin_by_email_and_password(
            email=jwt_data.get("email"))

        if is_admin:
            user_all_information: Union[None, User] = await UserRepository(session=session).find_user_and_get_full_information(user_id=user_id)

            if user_all_information:
                return AllDataUser(
                    email_user=user_all_information.email_user,
                    name_user=user_all_information.name_user,
                    surname_user=user_all_information.surname_user,
                    main_name_user=user_all_information.main_name_user,
                    orders=user_all_information.orders_user,
                    favourite=user_all_information.favourites_user,
                    history=user_all_information.history_buy_user,
                    reviews=user_all_information.reviews
                )

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def user_is_created(session: AsyncSession, email: str, password: str) -> bool:
        """
        Метод сервися для нахождения пользователя с указанной почтой и паролем
        :param session:
        :param email:
        :return:
        """

        result_find_user: Union[bool, User] = await UserRepository(session=session).find_user_by_email_and_password(
            email=email
        )

        if result_find_user:
            #verify password
            check_password = CryptographyScooter().verify_password(
                password=password, hashed_password=result_find_user.password_user)

        return result_find_user

    @staticmethod
    async def update_user_information(session: AsyncSession, token: str, to_update: DataToUpdate) -> UserIsUpdated:
        """
        Метод сервиса для обновления данных о пользователе
        :param session:
        :param token:
        :param to_update:
        :return:
        """

        #Getting id
        jwt_data = await Authentication().decode_jwt_token(token=token, type_token="access")
        return UserIsUpdated(
            is_updated = await UserRepository(session=session).update_one(
                other_id=jwt_data.get("id_user"),
                data_to_update=to_update.model_dump())
        )

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def update_user_password(session: AsyncSession, token: str, to_update: DataToUpdateUserPassword) -> UserIsUpdated:
        """
        Метод сервиса для обновления пароля пользователя
        :param session:
        :param token:
        :param to_update:
        :return:
        """

        #Getting user_id
        auth = Authentication()
        crypt = CryptographyScooter()
        jwt_data: dict = await auth.decode_jwt_token(token=token, type_token="access")

        #Проверка на совпадение пароля
        get_user_data: Union[User, None] = await UserRepository(session=session).find_one(other_id=jwt_data.get("id_user"))
        if get_user_data:
            check_password = crypt.verify_password(password=to_update.user_old_password, hashed_password=get_user_data[0].password_user)
            if check_password:
                hash_password = crypt.hashed_password(password=to_update.new_password)
                return UserIsUpdated(
                    is_updated=await UserRepository(session=session).update_one(
                        other_id=jwt_data.get("id_user"),
                        data_to_update={"password_user": hash_password}
                    )
                )
            await UserHttpError().http_failed_to_update_user_information()

        await UserHttpError().http_user_not_found()

    @staticmethod
    async def delete_user(session: AsyncSession, token: str) -> UserIsDeleted:
        """
        Метод сервиса для удаления всех данных пользователя
        :param session:
        :param token:
        :return:
        """

        #Getting user_id
        auth = Authentication()
        jwt_data: dict = await auth.decode_jwt_token(token=token, type_token="access")

        res_del = await UserRepository(session=session).delete_one(other_id=jwt_data.get("id_user"))
        if res_del:
            return UserIsDeleted(
                is_deleted=res_del
            )

        await UserHttpError().http_failed_to_delete_user()