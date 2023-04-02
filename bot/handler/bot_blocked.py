from aiogram import types

from database.service import set_life_user


async def user_blocked_bot(my_chat_member: types.ChatMemberUpdated):
    if my_chat_member.new_chat_member.status == types.ChatMemberStatus.KICKED:
        await set_life_user(life_status=False, tg_id=my_chat_member.from_user.id)

    if my_chat_member.new_chat_member.status == types.ChatMemberStatus.MEMBER:
        await set_life_user(life_status=True, tg_id=my_chat_member.from_user.id)
