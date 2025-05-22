import asyncio
import datetime
import aiohttp
import logging as logger

from faststream.rabbit import RabbitQueue, RabbitBroker
from faststream import FastStream
from dotenv import load_dotenv
from sqlalchemy import text

from src.api.core.order_app.schemas.order_dto import OrderIsBuy
from src.database.db_worker import db_work
from src.other.broker.dto.email_dto import EmailQueueMessage
from src.other.email.data_email_transfer import EmailTransfer
from src.settings.engine_settings import Settings


load_dotenv()


logging = logger.getLogger(__name__)

broker: RabbitBroker = RabbitBroker(
    url=f"amqp://{Settings.broker_settings.RABBIT_USER}:{Settings.broker_settings.RABBIT_PASSWORD}@{Settings.broker_settings.RABBIT_QUEUE_HOST}:5672/",  # noqa
)
faststream_app: FastStream = FastStream(broker=broker)


@broker.subscriber("email")
async def email_queue(message: EmailQueueMessage) -> None:
    """
    Отправка сообщения по почте
    :param message:
    """

    print(message)

    if message.type.value == "регистрация":
        print(423423)
        await EmailTransfer().send_message(
            text_to_message=f"Ваш секретный ключ для подтверждения аккаунта: {message.email_data.secret_key}\n"  # noqa
            f"Пожалуйста никому не сообщайте его",  # noqa
            whom_email=message.email_data.email,
        )
    else:
        print(843954)
        await EmailTransfer().send_message(
            text_to_message=f"Ваш секретный ключ для обновления пароля: {message.email_data.secret_key}\n"
                            f"Пожалуйста никому не сообщайте его",
            whom_email=message.email_data.email
        )


@broker.subscriber("transaction_send")
async def transaction_queue(message: dict):
    """
    Отмены покупок если время прошло
    :param message:
    """

    await asyncio.sleep(360)

    try:
        if (datetime.datetime.now() - datetime.datetime.fromisoformat(message["date_buy"])).total_seconds() > 350:
            # Проверка данных о товаре
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://backend_scooter:8000/api/v1/order/check_buy/{message['id']}") as req:
                    if req.status == 200:
                        data: OrderIsBuy = await req.json()
                        if not data["is_buy"]:
                            async with db_work.async_session.begin() as db:
                                await db.execute(text('DELETE FROM "Order" WHERE id = :id'), {"id": int(message["id"])})
    except Exception:
        logging.exception(
            msg="Не удалось удалить неоплаченный заказа id_order = " + str(message["id"])
        )


@faststream_app.after_startup
async def start_faststream():
    await broker.connect()
    await broker.declare_queue(queue=RabbitQueue(name="email"))
    await broker.declare_queue(queue=RabbitQueue(name="transaction_send"))


if __name__ == "__main__":
    asyncio.run(faststream_app.run())
