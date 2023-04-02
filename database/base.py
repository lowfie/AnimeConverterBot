from loguru import logger
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session

from database.models import Base, Subscribe, User, ChatMessage

from settings.config import (
    USER_POSTGRES,
    PASSWORD_POSTGRES,
    HOST_POSTGRES,
    PORT_POSTGRES,
    DATABASE_POSTGRES
)


CONNECTION_URL = f"postgresql://{USER_POSTGRES}:{PASSWORD_POSTGRES}@{HOST_POSTGRES}:{PORT_POSTGRES}/{DATABASE_POSTGRES}"
engine = create_engine(CONNECTION_URL)
session = scoped_session(sessionmaker(bind=engine))


def table_exist(table_name: str) -> bool:
    return inspect(engine).has_table(table_name)


async def create_tables_if_not_exist() -> None:
    """Автоматическое создание моделей при запуске"""
    models = [Subscribe, User, ChatMessage]
    existing_tables = [table_exist(name.__tablename__) for name in models]
    if not all(existing_tables):
        logger.info("Таблицы созданы, так как их не было в базе данных!")
        Base.metadata.create_all(bind=engine)

