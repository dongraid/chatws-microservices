import redis
import pickle
from fastapi import FastAPI
from database import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Message


app = FastAPI()
r = redis.Redis(host="redis", port=6379)


@app.get("/last_messages")
async def messages(session: AsyncSession = Depends(get_async_session)):
    cache_key = 'last_messages'
    cached_messages = r.get(cache_key)

    if cached_messages is not None:
        print("Data from cache")
        return pickle.loads(cached_messages)

    query = select(Message).order_by(Message.id.desc()).limit(10)
    messages = await session.execute(query)
    messages = messages.scalars().all()

    r.set(cache_key, pickle.dumps(messages))

    return messages

