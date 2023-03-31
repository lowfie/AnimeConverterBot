from aiogram import types
from sqlalchemy import update

from bot.base import bot, dp
from database.models import User
from database.base import session


@dp.my_chat_member_handler()
async def user_blocked_bot(my_chat_member: types.ChatMemberUpdated):
    if my_chat_member.new_chat_member.status == types.ChatMemberStatus.KICKED:
        session.execute(
            update(User)
            .values(is_life=False)
            .where(User.tg_id.__eq__(my_chat_member.from_user.id))
        )

    if my_chat_member.new_chat_member.status == types.ChatMemberStatus.MEMBER:
        session.execute(
            update(User)
            .values(is_life=True)
            .where(User.tg_id.__eq__(my_chat_member.from_user.id))
        )
    session.commit()
