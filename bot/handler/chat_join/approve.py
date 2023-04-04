import asyncio

from aiogram import types
from datetime import datetime, timedelta
from loguru import logger

from bot.base import bot
from bot.utils import send_message_media_types
from database.service import select_chat_message, add_user


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
    try:
        await chat_join.approve()
    except Exception as _ex:
        logger.info("Пользователь уже добавлен в чат", _ex)

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
