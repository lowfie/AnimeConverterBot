from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.utils import validation_button
from bot.keyboards.reply.cancel_state import cancel
from database.service import (
    init_chat_message,
    update_chat_message
)


class FormJoinMessage(StatesGroup):
    button = State()
    message = State()


async def text_join_to_chat(message: types.Message, state: FSMContext = None):
    await init_chat_message("join_chat")
    await FormJoinMessage.button.set()
    markup = await cancel()
    async with state.proxy() as data:
        data["text_type"] = "join_chat"
    await message.reply(
        "<b>Уведомление входа в чат</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<code>— Отправьте через пробел текст и ссылку кнопки</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
        reply_markup=markup,
        parse_mode="HTML"
    )


async def text_after_join_chat(message: types.Message, state: FSMContext = None):
    await init_chat_message("after_join")
    await FormJoinMessage.button.set()
    markup = await cancel()
    async with state.proxy() as data:
        data["text_type"] = "after_join"
    await message.reply(
        "<b>Уведомление через 15 минут после входа в чат</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<code>— Отправьте через пробел текст и ссылку кнопки</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
        reply_markup=markup,
        parse_mode="HTML"
    )


async def process_join_chat_pin_button(message: types.Message, state: FSMContext):
    button = validation_button(message)
    async with state.proxy() as data:
        data["btn_text"], data["btn_url"] = button
    await message.answer("❗️Кнопка не была добавлена" if None in button else "❗️Кнопка была добавлена")

    await FormJoinMessage.next()
    if data["text_type"] == "join_chat":
        await message.reply(
            "<b>Уведомление входа в чат</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "<code>— Отправьте медиафайл с сообщением для рассылки</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            parse_mode="HTML"
        )
    elif data["text_type"] == "after_join":
        await message.reply(
            "<b>Уведомление через 15 минут после входа в чат</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "<code>— Отправьте медиафайл с сообщением для рассылки</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
            parse_mode="HTML"
        )


async def process_media_join_chat(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == "text":
            await update_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=None,
                button_text=data["btn_text"],
                button_url=data["btn_url"]
            )
        elif message.content_type == "photo":
            await update_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=message.photo[0].file_id,
                button_text=data["btn_text"],
                button_url=data["btn_url"]
            )
        elif message.content_type == "video":
            await update_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=message.video.file_id,
                button_text=data["btn_text"],
                button_url=data["btn_url"]
            )
        elif message.content_type == "animation":
            await update_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=message.animation.file_id,
                button_text=data["btn_text"],
                button_url=data["btn_url"]
            )
    await message.reply("❗️Данные обновлены успешно")
    await state.finish()
