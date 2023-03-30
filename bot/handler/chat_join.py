from aiogram import types, filters

from bot.base import bot, dp
from config import JOIN_CHAT_TEXT


@dp.chat_join_request_handler()
async def approve_member(chat_join: types.ChatJoinRequest):
    await bot.send_message(
        chat_id=chat_join.from_user.id,
        text=JOIN_CHAT_TEXT
    )
    await chat_join.approve()
