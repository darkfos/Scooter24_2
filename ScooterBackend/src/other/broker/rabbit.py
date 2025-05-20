import asyncio
import datetime
import logging as logger

from faststream.rabbit import RabbitQueue, RabbitBroker
from faststream import FastStream
from dotenv import load_dotenv

from src.database.db_worker import db_work
from src.database.repository.order_repository import OrderRepository
from src.database.models.order import Order
from src.database.models.product import Product
from src.database.repository.product_repository import ProductRepository
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

    if message.type.value == "регистрация":
        await EmailTransfer().send_message(
            text_to_message=f"Ваш секретный ключ для подтверждения аккаунта: {message.secret_key}\n"  # noqa
            f"Пожалуйста никому не сообщайте его",  # noqa
            whom_email=message.email,
        )
    else:
        await EmailTransfer().send_message(
            text_to_message=f"Ваш секретный ключ для обновления пароля: {message.secret_key}\n"
                            f"Пожалуйста никому не сообщайте его",
            whom_email=message.email
        )


@broker.subscriber("transaction_send")
async def transaction_queue(message: Order):
    """
    Отмены покупок если время прошло
    :param message:
    """

    result: float = (datetime.datetime.now() - message.date_buy).total_seconds()

    await asyncio.sleep(350)

    print(result)

    if result > 350:
        try:

            async with db_work.async_session.begin() as session:

                # Возвращаем количество купленных товаров
                for product_data in message.product_list:

                    product_now_data: list[Product] = await ProductRepository(session).find_one(
                        other_id=product_data.id
                    )

                    if product_now_data:
                        await ProductRepository(session).update_one(
                            other_id=product_data.id,
                            data_to_update={
                                "quantity_product": product_now_data[0].quantity_product + product_data.count_product
                            }
                        )

                # Удаление заказа
                await OrderRepository(session).delete_one(
                    other_id=message.id
                )

        except Exception:
            logging.exception(
                msg="Не удалось удалить неоплаченный заказа id_order = " + message.id
            )


@faststream_app.after_startup
async def start_faststream():
    await broker.connect()
    await broker.declare_queue(queue=RabbitQueue(name="email"))


if __name__ == "__main__":
    asyncio.run(faststream_app.run())
