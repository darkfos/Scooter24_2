import asyncio
from faststream.rabbit import RabbitQueue, RabbitBroker
from faststream import FastStream
from dotenv import load_dotenv

from src.other.broker.dto.email_dto import EmailData
from src.other.email.data_email_transfer import EmailTransfer
from src.settings.engine_settings import Settings


load_dotenv()


broker: RabbitBroker = RabbitBroker(
    url=f"amqp://{Settings.broker_settings.RABBIT_USER}:{Settings.broker_settings.RABBIT_PASSWORD}@{Settings.broker_settings.RABBIT_QUEUE_HOST}:5672/", # noqa
)
faststream_app: FastStream = FastStream(broker=broker)


@broker.subscriber("email")
async def email_queue(message: EmailData) -> None:
    """
    Отправка сообщения по почте
    :param message:
    """

    await EmailTransfer().send_message(
        text_to_message=f"Ваш секретный ключ для подтверждения аккаунта: {message.secret_key}\n" # noqa
        f"Пожалуйста никому не сообщайте его", # noqa
        whom_email=message.email,
    )


@faststream_app.after_startup
async def start_faststream():
    await broker.connect()
    await broker.declare_queue(queue=RabbitQueue(name="email"))


if __name__ == "__main__":
    asyncio.run(faststream_app.run())
