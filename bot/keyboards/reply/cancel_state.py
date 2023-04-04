from aiogram import types


async def cancel():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Вернуться к боту")
    return markup
