import json
import aio_pika


async def publish(data: dict):
    message_body = json.dumps(data).encode()

    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")

    async with connection:
        routing_key = "messages"

        # Creating channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(routing_key, auto_delete=False)

        # Sending message
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body),
            routing_key=routing_key
        )

    print(" [x] Sent %r" % message_body)
