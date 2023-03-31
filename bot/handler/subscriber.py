from aiogram import types
from sqlalchemy import delete, select

from bot.base import bot, dp
from bot.utils import anti_flood
from bot.filter.admin import IsAdmin
from database.base import session
from database.models import Subscribe


@dp.message_handler(IsAdmin(), commands="add_sub")
@dp.throttled(anti_flood, rate=1)
async def add_subscribe(message: types.Message):
    if len(message.text.split()) == 4:
        _, title, chat_id, invited_link = message.text.split()
        sub = Subscribe(title=title, chat_id=chat_id, invited_link=invited_link)
        session.add(sub)
        await bot.send_message(
            message.chat.id,
            "<b>Вы добавили подписку</b>\n\n"
            f"<b>Название:</b> <code>{title}</code>\n"
            f"<b>ID чата:</b> <code>{chat_id}</code>\n"
            f"<b>Пригласительная ссылка:</b> <code>{invited_link}</code>",
            parse_mode="HTML"
        )
    session.commit()


@dp.message_handler(IsAdmin(), commands="remove_sub")
@dp.throttled(anti_flood, rate=1)
async def remove_subscribe(message: types.Message):
    if len(message.text.split()) == 2:
        _, chat_id = message.text.split()

        session.execute(delete(Subscribe).where(Subscribe.chat_id.__eq__(chat_id)))
        await bot.send_message(
            message.chat.id,
            f"Канал с ID <code>{chat_id}</code> был удалён из списка подписок",
            parse_mode="HTML"
        )
    session.commit()


@dp.message_handler(IsAdmin(), commands="subs")
@dp.throttled(anti_flood, rate=1)
async def get_all_subscriber(message: types.Message):
    subs = (session.execute(select(Subscribe.title, Subscribe.chat_id, Subscribe.invited_link))).all()

    text = ""

    for chat in subs:
        title, chat_id, invited_link = chat
        text += f"<b>Название:</b> <code>{title}</code>\n" \
                f"<b>ID чата:</b> <code>{chat_id}</code>\n" \
                f"<b>Пригласительная ссылка:</b> <code>{invited_link}</code>\n\n"

    await bot.send_message(
        message.chat.id,
        f"<b>Подписки</b>\n\n{text}",
        parse_mode="HTML"
    )
