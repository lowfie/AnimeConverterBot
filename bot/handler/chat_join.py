from aiogram import types

from bot.base import bot, dp
from config import JOIN_CHAT_TEXT, JOIN_CHAT_FILE_ID


@dp.chat_join_request_handler()
async def approve_member(chat_join: types.ChatJoinRequest):
    await bot.send_animation(
        chat_join.from_user.id,
        animation=JOIN_CHAT_FILE_ID,
        caption=JOIN_CHAT_TEXT,
        parse_mode="HTML"
    )
    await chat_join.approve()
