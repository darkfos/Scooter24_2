from faststream.rabbit import RabbitBroker
from src.other.broker.rabbit import broker
from src.other.broker.dto.email_dto import EmailData


async def send_message_email(email_data: EmailData):
    """
    Отправка данных в очередь
    :param email_data:
    """

    await broker.connect()
    await broker.publish(message=email_data, queue="email")