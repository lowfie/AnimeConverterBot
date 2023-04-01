import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime, timedelta

from bot.base import dp, bot
from bot.filter.admin import IsAdmin
from bot.utils import send_message_media_types
from database.service import (
    init_join_chat_message,
    update_join_chat_message,
    select_join_chat_message,
    add_user
)


class Form(StatesGroup):
    message = State()


@dp.message_handler(IsAdmin(), commands=["text_join_chat", "tjc"])
async def cmd_text_a(message: types.Message, state: FSMContext = None):
    await init_join_chat_message("join_chat")
    await Form.message.set()
    async with state.proxy() as data:
        data["text_type"] = "join_chat"
    await message.reply("Отправь сообщение уведомления при входе в группу (с медиафайлом)")


@dp.message_handler(IsAdmin(), commands=["text_after_join", "taj"])
async def cmd_text_b(message: types.Message, state: FSMContext = None):
    await init_join_chat_message("after_join")
    await Form.message.set()
    async with state.proxy() as data:
        data["text_type"] = "after_join"
    await message.reply("Отправь сообщение уведомления при входе после 15 минут (с медиафайлом)")


@dp.message_handler(content_types=["text", "photo", "video", "animation"], state=Form.message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == "text":
            await update_join_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=None
            )
        elif message.content_type == "photo":
            await update_join_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=message.photo[0].file_id
            )
        elif message.content_type == "video":
            await update_join_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=message.video.file_id
            )
        elif message.content_type == "animation":
            await update_join_chat_message(
                text_type=data["text_type"],
                content_type=message.content_type,
                text=message.parse_entities(),
                file_id=message.animation.file_id
            )
    await message.reply("Данные были обновлены")
    await state.finish()


@dp.chat_join_request_handler()
async def approve_member(chat_join: types.ChatJoinRequest):
    join_msg_content_type, join_msg_text, join_msg_file_id = await select_join_chat_message("join_chat")
    after_msg_content_type, after_msg_text, after_msg_file_id = await select_join_chat_message("after_join")

    await add_user(chat_join.from_user.id)
    await send_message_media_types(
        bot=bot,
        content_type=join_msg_content_type,
        chat_id=chat_join.from_user.id,
        text=join_msg_text,
        file_id=join_msg_file_id
    )
    await chat_join.approve()

    send_date = datetime.now() + timedelta(minutes=15)
    while datetime.now() <= send_date:
        await asyncio.sleep(1)
        if datetime.now() >= send_date:
            await send_message_media_types(
                bot=bot,
                content_type=after_msg_content_type,
                chat_id=chat_join.from_user.id,
                text=after_msg_text,
                file_id=after_msg_file_id
            )
            break
