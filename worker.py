import asyncio
import aio_pika
import aiohttp
import json
import os
from utils.logger import get_logger

logger = get_logger("Worker")

async def execute_http_call(task_data):
    """Executes the HTTP Target."""
    async with aiohttp.ClientSession() as session:
        try:
            url = task_data.get("url")
            method = task_data.get("method", "GET")
            headers = task_data.get("headers", {})
            body = task_data.get("body_template")

            logger.info(f"Worker processing task: {url}")
            async with session.request(method, url, headers=headers, json=body) as response:
                result = await response.text()
                logger.info(f"Task completed. Status: {response.status}")
        except Exception as e:
            logger.error(f"HTTP Execution failed: {e}")

async def process_message(message: aio_pika.IncomingMessage):
    """Handles the RabbitMQ message lifecycle."""
    # 'async with message.process()' automatically handles 'Ack' (removal from queue)
    # If this block crashes, the message is 'Nack'd' and put back in the queue.
    async with message.process():
        task_data = json.loads(message.body.decode())
        await execute_http_call(task_data)

async def main():
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
    
    # Robust connection with retry logic
    connection = await aio_pika.connect_robust(rabbitmq_url)
    channel = await connection.channel()
    
    # CRITICAL: Prefetch 1 ensures tasks are distributed evenly across your 4 workers
    await channel.set_qos(prefetch_count=1)
    
    queue = await channel.declare_queue("scheduler_tasks", durable=True)
    
    logger.info("Worker instance is online and listening...")
    await queue.consume(process_message)
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())