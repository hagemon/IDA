from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, Integer, Boolean
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
        "ChatContent", back_populates="chat", order_by="ChatContent.num.asc()"
    )

    @property
    def empty(self):
        return len(self.contents) == 0

    @property
    def general(self):
        return self.contents[0] if not self.empty else None

    @property
    def n_contents(self):
        return len(self.contents)

    def __repr__(self) -> str:
        return f"Title: {self.title} Create Time: {self.create_datetime}"


class ChatContent(Base):
    __tablename__ = "chat_contents"  # table name in the database

    id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), primary_key=True)
    num = Column(Integer, primary_key=True, default=0)
    content = Column(String)
    transform_op = Column(String)
    draw_op = Column(String)
    is_general = Column(Boolean, default=False)
    title = Column(String)

    chat = relationship("Chat", back_populates="contents")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.chat:
            self.num = len(self.chat.contents) + 1

    def __repr__(self) -> str:
        return f"id: {self.id} num: {self.num} operation: {self.transform_op}"
