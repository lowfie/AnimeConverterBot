from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from database.models import Base

engine = create_engine("sqlite:///bot.db")
session = scoped_session(sessionmaker(bind=engine))


async def create_database_if_not_exists():
    try:
        Base.metadata.create_all(engine)
        print('Database created')
    except Exception as ex_:
        print(ex_)