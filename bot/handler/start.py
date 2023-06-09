from aiogram import types

from bot.base import bot, dp
from bot.utils import anti_flood
from database.service import add_user
from settings.config import START_FILE_ID


@dp.throttled(anti_flood, rate=1)
async def start(message: types.Message):
    await add_user(message.from_user.id)
    await bot.send_photo(
        message.chat.id,
        photo=START_FILE_ID,
        caption=f"👋 Привет, {message.chat.first_name}\n\n"
        "📸 Отправь сюда <b>любое фото</b>, и я преобразую его в аниме стиль с помощью нейросетей\n\n"
        "🧸 Также можешь добавить бота в чат и развлекаться вместе с друзьями👇",
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove()
    )
