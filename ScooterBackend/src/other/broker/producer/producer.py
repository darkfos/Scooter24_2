from src.other.broker.rabbit import broker
from src.other.broker.dto.email_dto import EmailData, TypeEmailSendMessage, EmailQueueMessage
from src.database.models.order import Order


async def send_message_registration_on_email(email_data: EmailData):
    """
    Отправка данных в очередь
    :param email_data:
    """

    await broker.connect()
    await broker.publish(EmailQueueMessage(
        email_data=email_data, type=TypeEmailSendMessage.CREATE
    ), queue="email")


async def send_message_update_password_on_email(email_data: EmailData) -> None:
    """
    Отправка данных в очередь для обновления пароля
    :param email_data:
    """

    await broker.connect()
    await broker.publish(EmailQueueMessage(
        email_data=email_data, type=TypeEmailSendMessage.CREATE
    ), queue="email")


async def send_transaction_operation(order_data: Order):
    """
    Отправка данных о заказе, для отмены при неоплате
    :param order_data:
    """

    await broker.connect()

    schema_order = order_data.read_model_orm()
    await broker.publish(message=schema_order, queue="transaction_send")