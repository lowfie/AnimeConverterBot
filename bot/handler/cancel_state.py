from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.base import bot, dp


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="вернуться к боту", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Ваши действия были отменены", reply_markup=types.ReplyKeyboardRemove())
