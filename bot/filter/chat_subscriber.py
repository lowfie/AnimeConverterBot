from aiogram import types
from aiogram.dispatcher.filters import Filter
from sqlalchemy import select

from bot.base import bot
from database.base import session
from database.models import Subscribe


class IsSubscriber(Filter):
    async def check(self, message: types.Message):
        is_subs = True
        keyboard = types.InlineKeyboardMarkup()

        chats_db = (session.execute(select(Subscribe.chat_id, Subscribe.title, Subscribe.invited_link))).all()
        for channel in chats_db:
            chat_id, text, invited_link = channel

            try:
                chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
            except Exception as _ex:
                print("WARNING:", _ex)
                return

            if chat_member.status == types.ChatMemberStatus.LEFT:
                sub_channel_button = types.InlineKeyboardButton(text=text, url=invited_link)
                keyboard.add(sub_channel_button)
                is_subs = False

        if not is_subs:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="⚠️ Чтобы пользоваться ботом необходимо подписаться на каналы спонсоров",
                reply_markup=keyboard
            )

        return is_subs



