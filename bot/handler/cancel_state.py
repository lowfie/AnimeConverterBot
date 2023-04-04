from aiogram import types
from aiogram.dispatcher import FSMContext


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply(
        "❗️Ваши действия были отменены",
        reply_markup=types.ReplyKeyboardRemove()
    )
