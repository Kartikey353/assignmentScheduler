import aio_pika
import json
import os
from utils.logger import get_logger

logger = get_logger("RabbitMQManager")

class RabbitMQManager:
    _connection: aio_pika.abc.AbstractRobustConnection = None
    _channel: aio_pika.abc.AbstractRobustChannel = None
    _queue_name: str = "scheduler_tasks"

    @classmethod
    async def connect(cls):
        """
        Initializes a robust connection to RabbitMQ.
        If the connection drops, aio-pika will automatically try to reconnect.
        """
        if cls._connection and not cls._connection.is_closed:
            return

        try:
            rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
            cls._connection = await aio_pika.connect_robust(rabbitmq_url)
            cls._channel = await cls._connection.channel()
            
            # durable=True ensures the queue survives a RabbitMQ restart
            await cls._channel.declare_queue(cls._queue_name, durable=True)
            
            logger.info(f"Successfully connected to RabbitMQ and declared queue: {cls._queue_name}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    @classmethod
    async def publish_task(cls, payload: dict):
        """
        Publishes a JSON payload to the scheduler queue.
        Ensures the message is persistent so it isn't lost if RabbitMQ crashes.
        """
        if not cls._channel or cls._channel.is_closed:
            await cls.connect()

        try:
            message_body = json.dumps(payload, default=str).encode()
            
            await cls._channel.default_exchange.publish(
                aio_pika.Message(
                    body=message_body,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    content_type="application/json"
                ),
                routing_key=cls._queue_name,
            )
            logger.info(f"Task published to RabbitMQ: {payload.get('name', 'Unnamed Task')}")
        except Exception as e:
            logger.error(f"Error publishing message to RabbitMQ: {e}")
            raise

    @classmethod
    async def close(cls):
        """Gracefully closes the connection during app shutdown."""
        if cls._connection and not cls._connection.is_closed:
            await cls._connection.close()
            logger.info("RabbitMQ connection closed.")