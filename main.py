from aiogram import executor

from bot.base import dp


async def on_startup(dispatcher):
    from bot.handler import start, converter, chat_join
    print("bot was started")


async def on_shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)