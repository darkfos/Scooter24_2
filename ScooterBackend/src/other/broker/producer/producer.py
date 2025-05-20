from src.other.broker.rabbit import broker
from src.other.broker.dto.email_dto import EmailData, TypeEmailSendMessage
from src.database.models.order import Order


async def send_message_registration_on_email(email_data: EmailData):
    """
    Отправка данных в очередь
    :param email_data:
    """

    await broker.connect()
    await broker.publish(message={
        "email_data": email_data,
        "type": TypeEmailSendMessage.CREATE
    }, queue="email")


async def send_message_update_password_on_email(email_data: EmailData) -> None:
    """
    Отправка данных в очередь для обновления пароля
    :param email_data:
    """

    await broker.connect()
    await broker.publish(message={
        "email_data": email_data,
        "type": TypeEmailSendMessage.UPDATE
    }, queue="email")


async def send_transaction_operation(order_data: Order):
    """
    Отправка данных о заказе, для отмены при неоплате
    :param order_data:
    """

    await broker.connect()
    await broker.publish(message=order_data.read_model(), queue="transaction_send")