from loguru import logger
from sqlalchemy import select, update

from database.models import User, ChatMessage
from database.base import session


async def add_user(tg_id):
    user = User(tg_id=tg_id)
    is_user = (session.execute(select(User.tg_id).where(User.tg_id.__eq__(tg_id)))).scalar()
    if is_user:
        return
    session.add(user)
    try:
        session.commit()
    except Exception as err:
        logger.warning("Ошибка добавления пользователей", err)
        session.rollback()


async def init_chat_message(text_type: str):
    is_text_type = (session.execute(
            select(ChatMessage.text_type)
            .where(ChatMessage.text_type.__eq__(text_type))
        )).first()

    if not is_text_type:
        join_chat = ChatMessage(text_type=text_type)
        session.add(join_chat)
        session.commit()


async def update_chat_message(text_type: str, content_type: str, text: str, file_id):
    session.execute(
        update(ChatMessage)
        .values(
            content_type=content_type,
            text=text,
            file_id=file_id
        )
        .where(ChatMessage.text_type.__eq__(text_type))
    )
    session.commit()


async def select_chat_message(text_type: str):
    join_chat_message = (session.execute(
        select(
            ChatMessage.content_type,
            ChatMessage.text,
            ChatMessage.file_id
        )
        .where(ChatMessage.text_type.__eq__(text_type))
    )).first()
    return join_chat_message


async def set_life_user(life_status: bool, tg_id):
    session.execute(
        update(User)
        .values(is_life=life_status)
        .where(User.tg_id.__eq__(tg_id))
    )
    session.commit()
    if life_status:
        logger.info(f"Пользователь с ID {tg_id} разблокировал бота")
    else:
        logger.info(f"Пользователь с ID {tg_id} заблокировал бота")
