from aiogram import types
from sqlalchemy import select, func

from bot.base import bot, dp
from bot.utils import anti_flood
from bot.filter.admin import IsAdmin
from database.base import session
from database.models import User


@dp.message_handler(IsAdmin(), commands="stats")
@dp.throttled(anti_flood, rate=1)
async def stats_of_users(message: types.Message):
    life_users = (session.execute(select(func.count(User.id)).where(User.is_life.__eq__(True)))).scalar()
    die_users = (session.execute(select(func.count(User.id)).where(User.is_life.__eq__(False)))).scalar()

    await bot.send_message(
        message.chat.id,
        f"<b>Статистика пользователей</b>\n\n"
        f"<b>Активные пользователи:</b> <code>{life_users}</code>\n"
        f"<b>Не активные пользователи:</b> <code>{die_users}</code>\n"
        f"<b>Общее количество:</b> <code>{life_users + die_users}</code>\n",
        parse_mode="HTML"
    )
