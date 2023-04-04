from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Text


Base = declarative_base()


class Subscribe(Base):
    __tablename__ = "Subscribe"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, default="Button")
    chat_id = Column(String, nullable=False)
    invited_link = Column(String, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    tg_id = Column(BigInteger, unique=True)
    is_life = Column(Boolean, default=True)


class ChatMessage(Base):
    __tablename__ = 'chat_message'
    id = Column(Integer, primary_key=True, nullable=False)
    text_type = Column(String, nullable=False)
    content_type = Column(String, nullable=False, default="text")
    text = Column(String, nullable=False, default="Some Text")
    file_id = Column(String, nullable=True)
    button_text = Column(Text, nullable=True)
    button_url = Column(Text, nullable=True)


