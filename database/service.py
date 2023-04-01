from sqlalchemy import select, update

from database.models import User, JoinChatMessage
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
        print("Ошибка добавления пользователей", err)
        session.rollback()


async def init_join_chat_message(text_type: str):
    is_text_type = (session.execute(
            select(JoinChatMessage.text_type)
            .where(JoinChatMessage.text_type.__eq__(text_type))
        )).first()

    if not is_text_type:
        join_chat = JoinChatMessage(text_type=text_type)
        session.add(join_chat)
        session.commit()


async def update_join_chat_message(text_type: str, content_type: str, text: str, file_id):
    session.execute(
        update(JoinChatMessage)
        .values(
            content_type=content_type,
            text=text,
            file_id=file_id
        )
        .where(JoinChatMessage.text_type.__eq__(text_type))
    )
    session.commit()


async def select_join_chat_message(text_type: str):
    join_chat_message = (session.execute(
        select(
            JoinChatMessage.content_type,
            JoinChatMessage.text,
            JoinChatMessage.file_id
        )
        .where(JoinChatMessage.text_type.__eq__(text_type))
    )).first()
    return join_chat_message

