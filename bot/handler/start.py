from aiogram import types

from bot.base import bot, dp
from bot.utils import anti_flood


@dp.message_handler(commands="start")
@dp.throttled(anti_flood, rate=1)
async def start(message: types.Message):
    await bot.send_message(
        message.chat.id,
        f"👋 Привет, {message.chat.first_name}\n\n"
        "📸 Отправь сюда <b>любое фото</b>, и я преобразую его в аниме стиль с помощью нейросетей\n\n"
        "🧸 Также можешь добавить бота в чат и развлекаться вместе с друзьями👇",
        parse_mode="HTML"
        )
