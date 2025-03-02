# Other libraries
import smtplib as smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

# Local
from src.settings.engine_settings import Settings
from src.settings.other_settings.email_transfer_settings import (
    EmailTransferSettings,
)


class EmailTransfer:

    def __init__(self):
        self.__email_data: EmailTransferSettings = Settings.email_tr_settings
        self.__email_from: str = self.__email_data.email
        self.__password: str = self.__email_data.password

    async def _connect(self) -> None:
        self.smtp_server = smtp.SMTP("smtp.gmail.com", 587)
        self.smtp_server.starttls()
        self.smtp_server.login(self.__email_from, self.__password)

    async def send_message(
        self,
        text_to_message: str,
        whom_email: str,
        title_message: str = "Сообщение от Scooters24 📧",
    ) -> None:
        """
        Отправка сообщения по почте
        :text_to_message:
        :whom_email:
        :title_message:
        """

        # Connect
        await self._connect()
        new_message = MIMEMultipart()
        new_message["From"] = self.__email_from
        new_message["To"] = whom_email
        new_message["Subject"] = title_message

        # Текст для сообщения
        new_message.attach(MIMEText(text_to_message, "plain"))

        # Logging
        logging.info(
            msg="Email отправка сообщения {} по почте"
            "".format(text_to_message)
        )

        # Отправка
        self.smtp_server.send_message(new_message)
        self.smtp_server.quit()


email_transfer: EmailTransfer = EmailTransfer()
