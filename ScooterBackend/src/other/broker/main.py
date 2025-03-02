from faststream import FastStream
from faststream.rabbit import RabbitBroker
from os import getenv
from dotenv import load_dotenv


load_dotenv()


broker: RabbitBroker = RabbitBroker(
    url=f"amqp://{getenv('RABBIT_USER')}:{getenv('RABBIT_PASS')}@localhost:5672/"
)
faststream_app: FastStream = FastStream(broker=broker)
