import asyncio
import aiohttp
import asyncpg
import logging as logger

from faststream.rabbit import RabbitQueue, RabbitBroker
from faststream import FastStream
from dotenv import load_dotenv
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
            text_to_message=f"Ваш секретный ключ для подтверждения аккаунта: {message.email_data.secret_key}\n" # noqa
            f"Пожалуйста никому не сообщайте его",  # noqa
            whom_email=message.email_data.email,
        )
    else:
        await EmailTransfer().send_message(
            text_to_message=f"Ваш секретный ключ для обновления пароля: {message.email_data.secret_key}\n" # noqa
            f"Пожалуйста никому не сообщайте его",
            whom_email=message.email_data.email,
        )


@broker.subscriber("transaction_send")
async def transaction_queue(message: dict):
    try:

        await asyncio.sleep(400)

        order_id = message.get("id")
        date_buy = message.get("date_buy")
        if not order_id or not date_buy:
            logging.error(f"Некорректное сообщение: {message}")
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://24скутер.рф/api/v1/order/check_buy/{order_id}"
            ) as req:

                if req.status == 200:
                    data = await req.json()
                    if not data.get("is_buy"):
                        connection = await asyncpg.connect(
                            user=Settings.database_settings.db_user,
                            password=Settings.database_settings.db_password,
                            database=Settings.database_settings.db_name,
                            host="database",
                            port=5432
                        )

                        await connection.execute(
                            'DELETE FROM "Order" WHERE id = $1',
                            int(order_id)
                        )

                        await connection.close()

    except Exception as e:
        logging.exception(f"Не удалось удалить неоплаченный заказ id_order = {order_id}: {e}") # noqa


@faststream_app.after_startup
async def start_faststream():
    await broker.connect()
    await broker.declare_queue(queue=RabbitQueue(name="email"))
    await broker.declare_queue(queue=RabbitQueue(name="transaction_send"))


if __name__ == "__main__":
    asyncio.run(faststream_app.run())
