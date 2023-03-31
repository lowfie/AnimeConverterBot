from aiogram import executor

from bot.base import dp


async def on_startup(dispatcher):
    from database.base import create_database_if_not_exists
    await create_database_if_not_exists()
    from bot.handler import start, shout, converter, chat_join, subscriber, stats, bot_blocked
    print("bot was started")


async def on_shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
