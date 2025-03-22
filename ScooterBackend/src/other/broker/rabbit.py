import asyncio
from faststream.rabbit import RabbitQueue, RabbitBroker
from src.other.broker.dto.email_dto import EmailData
from src.other.email.data_email_transfer import EmailTransfer
from faststream import FastStream
from os import getenv
from dotenv import load_dotenv


load_dotenv()


broker: RabbitBroker = RabbitBroker(
    url=f"amqp://{getenv("RABBIT_USER")}:{getenv("RABBIT_PASSWORD")}@broker_rabbit:5672/"
)
faststream_app: FastStream = FastStream(broker=broker)


@broker.subscriber("email")
async def email_queue(message: EmailData) -> None:
    """
    Отправка сообщения по почте
    :param message:
    """

    await EmailTransfer().send_message(
        text_to_message=f"Ваш секретный ключ для подтверждения аккаунта: {message.secret_key}\n"
                        f"Пожалуйста никому не сообщайте его",
        whom_email=message.email
    )


@faststream_app.after_startup
async def start_faststream():
    await broker.connect()
    await broker.declare_queue(queue=RabbitQueue(name="email"))


if __name__ == "__main__":
    asyncio.run(faststream_app.run())