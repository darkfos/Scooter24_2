from api.authentication.secure.authentication_service import (
    Authentication,
    AuthenticationEnum,
)
from api.dep.dependencies import IEngineRepository
from api.core.user_app.service.user_service import (
    UserService,
    UserHttpError,
)
from other.email.data_email_transfer import email_transfer
from api.authentication.secret.secret_upd_key import SecretKey
from api.core.user_app.schemas.user_dto import AddUser
from other.broker.producer.producer import send_message_email
from other.broker.dto.email_dto import EmailData
import logging

logging.getLogger()


auth: Authentication = Authentication()


class EmailService:
    @staticmethod
    async def send_secret_key_for_register(
        engine: IEngineRepository, new_user: AddUser
    ) -> None:
        """
        Метод сервиса EmailService - отправка ссылки на почту
        """

        logging.info(
            msg=f"{EmailService.__name__} Отправка ссылки"
            f" на подтверждение регистрации"
        )
        secret_key: str = SecretKey().generate_password()

        async with engine:
            user_data = (
                await engine.user_repository.find_user_by_email_and_password(
                    email=new_user.email_user
                )
            )
            if user_data:
                is_updated = await engine.user_repository.update_one(
                    other_id=user_data.id,
                    data_to_update={"secret_create_key": secret_key},
                )
                if is_updated:
                    await send_message_email(email_data=EmailData(
                        email=new_user.email_user,
                        secret_key=secret_key
                    ))

    @staticmethod
    async def access_user_account(
        engine: IEngineRepository, user_email: str, secret_key: str
    ) -> None:
        """
        Метод сервиса EmailService - подтверждение аккаунта пользователя
        """

        async with engine:
            user_data = (
                await engine.user_repository.find_user_by_email_and_password(
                    email=user_email
                )
            )
            if user_data and user_data.secret_create_key == secret_key:
                is_updated = await engine.user_repository.update_one(
                    other_id=user_data.id,
                    data_to_update={"secret_create_key": "", "is_active": True},
                )
                if is_updated:
                    return
                await UserHttpError().http_failed_to_update_user_information()
            await UserHttpError().http_user_not_found()

    @auth(worker=AuthenticationEnum.DECODE_TOKEN.value)
    @staticmethod
    async def send_secret_key_by_update_password(
        engine: IEngineRepository,
        email: str,
        token: str,
        token_data: dict = dict(),
    ) -> None:
        """
        Отправка секретного ключа для обновления пароля
        :email:
        """

        logging.info(
            msg=f"{EmailService.__name__} Отправка секретного"
            f" ключа для обновления пароля"
        )
        sctr_key: str = SecretKey().generate_password()

        await email_transfer.send_message(
            text_to_message="Ваш секретный ключ для обновления"
            " пароля: {}\nПожалуйсте ни кому не передавайте"
            " его.".format(sctr_key),
            whom_email=email,
        )

        async with engine:
            is_updated: bool = await engine.user_repository.update_one(
                other_id=token_data.get("sub"),
                data_to_update={"secret_update_key": sctr_key},
            )

            if is_updated:
                return
            logging.critical(
                msg=f"{UserService.__name__} "
                f"Не удалось отправить секретный ключ"
            )
            await UserHttpError().http_failed_to_update_user_information()
