from aiogram import types
from aiogram.dispatcher.filters import Filter

from settings.config import ADMINS


class IsAdmin(Filter):
    async def check(self, message: types.Message) -> bool:
        user = message.from_user.id
        return user in ADMINS
