from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import select

from bot.base import bot, dp
from bot.filter.admin import IsAdmin
from bot.utils import send_message_media_types
from database.base import session
from database.models import User


users = (session.execute(select(User.tg_id).where(User.is_life.__eq__(True)))).all()


class Form(StatesGroup):
    text = State()
    media = State()


@dp.message_handler(IsAdmin(), commands="shout")
async def cmd_shout(message: types.Message):
    await Form.text.set()
    await message.reply("Отправь текст рассылки")


@dp.message_handler(content_types=["text"], state=Form.text)
async def process_text(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Вернуться к боту")

    async with state.proxy() as data:
        data["text"] = message.parse_entities()
        await Form.next()
        await message.reply(
            "Отправьте медиафайл и дождитесь отправки",
            reply_markup=markup
        )


@dp.message_handler(content_types=["photo", "video", "animation"],  state=Form.media)
async def process_media(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == "photo":
            file_id=message.photo[0].file_id
        elif message.content_type == "video":
            file_id=message.video.file_id
        elif message.content_type == "animation":
            file_id=message.animation.file_id

        for user_id in users:
            chat = user_id[0]
            await send_message_media_types(
                bot=bot,
                content_type=message.content_type,
                chat_id=chat,
                text=data["text"],
                file_id=file_id
            )

    await bot.send_message(message.from_user.id, "Все сообщения были успешно отправлены")
    await state.finish()
