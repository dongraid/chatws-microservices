import asyncio
import datetime

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from database import async_session_maker
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from models import Message
from main import r as redis


async def on_message(message: AbstractIncomingMessage) -> None:
    print(" [x] Received message %r" % message)
    print("Decoded body is: %r" % message.body.decode("utf-8"))

    async with async_session_maker() as session:
        query = insert(Message).values(
            message=message.body.decode("utf-8"),
            user_id=1,
            timestamp=datetime.datetime.now()
        )
        await session.execute(query)
        try:
            await session.commit()
            redis.delete("last_messages")
        except SQLAlchemyError:
            await session.rollback()


async def main() -> None:
    connection = await connect("amqp://guest:guest@rabbitmq/")
    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue("messages")

        await queue.consume(on_message, no_ack=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
