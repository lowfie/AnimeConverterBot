from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class Subscribe(Base):
    __tablename__ = "Subscribe"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, default="Button")
    chat_id = Column(String, nullable=False)
    invited_link = Column(String, nullable=False)
