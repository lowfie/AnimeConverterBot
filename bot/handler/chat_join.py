import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime, timedelta

from bot.base import bot
from bot.utils import send_message_media_types, validation_button
from database.service import (
    init_chat_message,
    update_chat_message,
    select_chat_message,
    add_user
)


class FormJoinMessage(StatesGroup):
    button = State()
    message = State()


async def text_join_to_chat(message: types.Message, state: FSMContext = None):
    await init_chat_message("join_chat")
    await FormJoinMessage.button.set()
    async with state.proxy() as data:
        data["text_type"] = "join_chat"
    await message.reply("Введите через пробел сначала текст, после ссылку кнопки для добавления")


async def text_after_join_chat(message: types.Message, state: FSMContext = None):
    await init_chat_message("after_join")
    await FormJoinMessage.button.set()
    async with state.proxy() as data:
        data["text_type"] = "after_join"
    await message.reply("Введите через пробел сначала текст, после ссылку кнопки для добавления")


async def process_join_chat_pin_button(message: types.Message, state: FSMContext):
    button = validation_button(message)
    async with state.proxy() as data:
        data["btn_text"], data["btn_url"] = button
    await message.answer("Кнопка не была добавлена" if None in button else "Кнопка была добавлена")

    await FormJoinMessage.next()
    if data["text_type"] == "join_chat":
        await message.reply("Отправь сообщение уведомления при входе в группу (с медиафайлом)")
    elif data["text_type"] == "after_join":
        await message.reply("Отправь сообщение уведомления при входе после 15 минут (с медиафайлом)")


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
    await message.reply("Данные были обновлены")
    await state.finish()


async def approve_member(chat_join: types.ChatJoinRequest):
    join_content_type, join_text, join_file_id, join_btn_text, join_btn_url = await select_chat_message("join_chat")
    after_content_type, after_text, after_file_id, after_btn_text, after_btn_url = await select_chat_message("after_join")

    await add_user(chat_join.from_user.id)
    await send_message_media_types(
        bot=bot,
        content_type=join_content_type,
        chat_id=chat_join.from_user.id,
        text=join_text,
        file_id=join_file_id,
        button_text=join_btn_text,
        button_url=join_btn_url
    )
    await chat_join.approve()

    send_date = datetime.now() + timedelta(minutes=15)
    while datetime.now() <= send_date:
        await asyncio.sleep(1)
        if datetime.now() >= send_date:
            await send_message_media_types(
                bot=bot,
                content_type=after_content_type,
                chat_id=chat_join.from_user.id,
                text=after_text,
                file_id=after_file_id,
                button_text=after_btn_text,
                button_url=after_btn_url
            )
            break
