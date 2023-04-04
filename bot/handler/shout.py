from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import select

from bot.base import bot
from bot.utils import send_message_media_types, validation_button
from bot.keyboards.reply.cancel_state import cancel
from database.base import session
from database.models import User

users = (session.execute(select(User.tg_id).where(User.is_life.__eq__(True)))).all()


class FormShout(StatesGroup):
    text = State()
    button = State()
    media = State()


async def cmd_shout(message: types.Message):
    await FormShout.text.set()
    markup = await cancel()
    await message.reply("Отправь текст рассылки", reply_markup=markup)


async def process_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.parse_entities()

    await FormShout.next()
    await message.reply("Введите через пробел сначала текст, после ссылку кнопки для добавления")


async def process_pin_button_to_shout(message: types.Message, state: FSMContext):
    button = validation_button(message)
    async with state.proxy() as data:
        data["btn_text"], data["btn_url"] = button
    await message.answer("Кнопка не была добавлена" if None in button else "Кнопка была добавлена")

    await FormShout.next()
    await message.reply("Отправьте медиафайл и дождитесь отправки")


async def process_media(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == "photo":
            file_id = message.photo[0].file_id
        elif message.content_type == "video":
            file_id = message.video.file_id
        elif message.content_type == "animation":
            file_id = message.animation.file_id

        for user_id in users:
            chat = user_id[0]
            await send_message_media_types(
                bot=bot,
                content_type=message.content_type,
                chat_id=chat,
                text=data["text"],
                file_id=file_id,
                button_text=data["btn_text"],
                button_url=data["btn_url"]
            )

    await bot.send_message(message.from_user.id, "Все сообщения были успешно отправлены")
    await state.finish()
