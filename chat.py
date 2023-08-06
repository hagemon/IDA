from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chats"  # table name in the database

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
    )
    title = Column(String)
    create_datetime = Column(TIMESTAMP, default=func.now())
    url = Column(String)

    contents = relationship(
        "ChatContent", back_populates="chat", order_by="ChatContent.num.desc()"
    )

    def __repr__(self) -> str:
        return f"Title: {self.title} Create Time: {self.create_datetime}"


class ChatContent(Base):
    __tablename__ = "chat_contents"  # table name in the database

    id = Column(UUID, ForeignKey("chats.id"), primary_key=True)
    num = Column(Integer, primary_key=True)
    content = Column(String)
    operation = Column(String)

    chat = relationship("Chat", back_populates="contents")
