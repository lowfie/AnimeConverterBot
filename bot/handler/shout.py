from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import select

from bot.base import bot, dp
from database.base import session
from database.models import User


users = (session.execute(select(User.tg_id).where(User.is_life.__eq__(True)))).all()


# States
class Form(StatesGroup):
    text = State()
    media = State()


@dp.message_handler(commands="shout")
async def cmd_shout(message: types.Message):
    await Form.text.set()
    await message.reply("Отправь текст рассылки (HTML формат)")


@dp.message_handler(state=Form.text)
async def process_text(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Вернуться к боту")

    async with state.proxy() as data:
        data["text"] = message.parse_entities()
        await Form.next()
        await message.reply(
            "Отправьте медиафайл и дождитесь отправки\n"
            "Вам придёт уведомление, когда все сообщения будут отправлены\n"
            "И нажмите кнопку отмена, либо нажмите сразу, но отправка прекратиться",
            reply_markup=markup
        )


@dp.message_handler(content_types=["photo", "video", "animation"],  state=Form.media)
async def process_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == "photo":
            for user_id in users:
                chat = user_id[0]
                await bot.send_photo(
                    chat_id=chat,
                    photo=message.photo[0].file_id,
                    caption=data["text"],
                    parse_mode="HTML"
                )
        elif message.content_type == "video":
            for user_id in users:
                chat = user_id[0]
                await bot.send_video(
                    chat_id=chat,
                    video=message.video.file_id,
                    caption=data["text"],
                    parse_mode="HTML"
                )
        elif message.content_type == "animation":
            for user_id in users:
                chat = user_id[0]
                await bot.send_animation(
                    chat_id=chat,
                    animation=message.animation.file_id,
                    caption=data["text"],
                    parse_mode="HTML"
                )
    await bot.send_message(message.from_user.id, "Все сообщения были успешно отправлены")


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="вернуться к боту", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Отменено", reply_markup=types.ReplyKeyboardRemove())
