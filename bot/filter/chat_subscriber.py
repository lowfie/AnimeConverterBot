from aiogram import types
from aiogram.dispatcher.filters import Filter

from bot.base import bot
from config import chats


class IsSubscriber(Filter):
    async def check(self, message: types.Message):
        is_subs = True
        keyboard = types.InlineKeyboardMarkup()

        for channel in chats:
            text = channel["title"]
            chat_id = channel["chat_id"]
            invited_link = channel["invited_link"]
            chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)

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



