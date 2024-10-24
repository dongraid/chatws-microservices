from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
