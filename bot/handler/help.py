from aiogram import types

from bot.base import bot, dp
from bot.utils import anti_flood


@dp.throttled(anti_flood, rate=1)
async def admin_help(message: types.Message):
    await bot.send_message(
        message.chat.id,
        text="<b>Помощь</b>\n\n"
             "<code>/tjc /text_join_chat</code> - <b>уведомление при входе в канал</b>\n"
             "<code>/taj /text_after_join</code> - <b>уведомление через 15 минут после входа в канал</b>\n"
             "<code>/tap /text_after_photo</code> - <b>уведомление после обработки фото</b>\n"
             "<code>/shout</code> - <b>рассылка сообщения</b>\n"
             "<code>/stats</code> - <b>статистика активных пользователей</b>\n"             "<code>/shout</code> - <b>рассылка сообщения</b>\n"
             "<code>/subs</code> - <b>просмотр спонсоров</b>\n"
             "<code>/add_sub</code> - <b>добавление спонсоров</b>\n"
             "<code>/remove_sub</code> - <b>удаление спонсоров</b>\n",
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove()
    )
