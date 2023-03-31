from sqlalchemy import select

from database.models import User
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
