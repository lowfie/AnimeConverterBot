from aiogram import executor
from loguru import logger

from bot.base import dp
from bot.register import register_bot_handlers
from database.base import create_tables_if_not_exist


async def on_startup(dispatcher):
    await create_tables_if_not_exist()
    await register_bot_handlers(dispatcher)
    logger.info("bot was started")


async def on_shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
